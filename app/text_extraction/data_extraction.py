from .containers import *
from .checkmark_utils import *
from .prompt_response_mapping import *
from .utils import check_for_split_fields
import os
import re
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTPage, LAParams, LTText, LTFigure


def parse_text(text_field, prompts_dict, container, checkbox_container=None, customer_input = False):
    """
    Parses out the text and bounding box as a tuple : (x_min, y_min, x_max, y_max). 
    Append the text to the item_list which can be form input fields or data provided by
    the user.

    Args:
        text_field (LTTextBoxHorizontal): text field in the pdf document
    
    Returns:
        None
    """
    try:
        text = text_field.get_text().strip()
    except AttributeError:
        text = text_field.field.strip()
    except:
        return
    
    #Remove underscores from text
    text = text.strip('_')
    text_set = set(text.replace(':', "").split())

    try:
        if len(text) > 0 :
            x_min, y_min, x_max, y_max = text_field.bbox
            if customer_input:
                prompts_dict['single_input'].append(container(text, y_min, x_min))
            elif text_set.intersection(LONG_KEYWORDS):
                prompts_dict['long_prompts'].append(container(text, y_min, x_max))
            elif text_set.intersection(CHECKBOX_OPTIONS):
                prompts_dict['checkbox_prompts'].append(checkbox_container(text, x_min, y_min, x_max, y_max))
            else:
                prompts_dict['prompts'].append(container(text, y_min, x_max))
    except AttributeError:
        return


def check_for_vectorized_image(layout, customer_input_dict, entry_tuple, checkbox_tuple):
    """
    Checks if the layout contains the customer input as a vectorized image. If it does, then it extracts,
    and parses the customer inputs and store them in the customer_input_dict

    Args:

    Returns:
    """
    for lt_obj in layout:
        try:
            if "Xi" in lt_obj.name:
                for sub_item in lt_obj:
                    if isinstance(sub_item, LTText):
                        parse_text(text_field=sub_item, prompts_dict=customer_input_dict, \
                                container=entry_tuple, customer_input=True)
                    elif isinstance(sub_item, LTFigure):
                        parse_checkboxes(checkbox=sub_item, customer_input_dict=customer_input_dict, container=checkbox_tuple)
                return True
        except AttributeError:
            continue
    return False


def split_text(text_field, field_container):
    """
    Splits the following fields:

    Preferred name:, Email:
    Pasport number:, Passport expiration date:
    Gender, Weight:
    DOB:, Age safari:, Height:
    City:, State/Province:
    Zip:, Phone:
    """
    text = text_field.get_text().strip()
    clean_text = re.sub(pattern=PUNC_REGEX, repl='', string=text)
    text_set = set(clean_text.split())

    if text_set.intersection(LONG_KEYWORDS) or text_set.intersection(DIET_OPTIONS):
        return [text_field]
    
    #Match form fields:
    #Make mapping for gender and weight:
    field_pattern = re.compile(r'[^\s_][?,\'\"\w+\s+()/-]+:?\s{0,3}_{0,3}') #finds all the single input fields (email, passport, etc)
    field_pattern2 = re.compile(r'[^\s_]\w+\s[\w()]*\s?[\w]*\s?[\w)]*') #finds all the accomodation fields

    split_fields = field_pattern.findall(text)
    my_matches = list(field_pattern.finditer(text))
    
    res = []
    if len(split_fields) == 1:
        if len(split_fields[0]) > 80:
            sub_fields = field_pattern2.findall(text)
            x_min, y_min, x_max, y_max = text_field.bbox
            try:
                res.append(field_container(field=sub_fields[0].strip(), bbox=(x_min, y_min, x_min + 100, y_max)))
                res.append(field_container(field=sub_fields[1].strip(), bbox=(x_max-100, y_min, x_max, y_max)))
            except IndexError:
                return [text_field]
        else:
            return [text_field]
    elif len(split_fields) == 2:
        x_min, y_min, x_max, y_max = text_field.bbox
        
        #First field:
        text_span = my_matches[0].span()
        new_x_max = x_min + (text_span[1] - text_span[0]) * X_VALUE_PER_CHARACTER
        if 'Gender' in split_fields[0]:
            res.append(field_container(field=split_fields[0].strip(), bbox=(x_min, y_min, new_x_max + 120, y_max)))
        else:
            res.append(field_container(field=split_fields[0].strip(), bbox=(x_min, y_min, new_x_max, y_max)))

        #Second field:
        text_span = my_matches[1].span()
        new_x_min = x_max - (text_span[1] - text_span[0]) * X_VALUE_PER_CHARACTER
        if 'Weight' not in split_fields[1]:
            res.append(field_container(field=split_fields[1].strip(), bbox=(new_x_min, y_min, x_max, y_max)))
        else:
            res.append(field_container(field='Weight (lbs):', bbox=(new_x_min+150, y_min, x_max, y_max)))
    elif len(split_fields) == 3:
        x_min, y_min, x_max, y_max = text_field.bbox
        
        #First field:
        text_span = my_matches[0].span()
        new_x_max = x_min + (text_span[1] - text_span[0]) * X_VALUE_PER_CHARACTER
        res.append(field_container(field=split_fields[0].strip(), bbox=(x_min, y_min, new_x_max, y_max)))

        #Third field:
        text_span = my_matches[2].span()
        new_x_min = x_max - (text_span[1] - text_span[0]) * X_VALUE_PER_CHARACTER
        res.append(field_container(field=split_fields[2].strip(), bbox=(new_x_min, y_min, x_max, y_max)))

        #Second field:
        text_span = my_matches[1].span()
        res.append(field_container(field=split_fields[1].strip(), bbox=(new_x_max+60, y_min, new_x_min-50, y_max)))
    elif len(split_fields) == 4:
        x_min, y_min, x_max, y_max = text_field.bbox
        
        #First field:
        text_span = my_matches[0].span()
        new_x_max = x_min + (text_span[1] - text_span[0]) * X_VALUE_PER_CHARACTER + 15
        res.append(field_container(field=split_fields[0].strip(), bbox=(x_min, y_min, new_x_max, y_max)))

        #Fourth field:
        text_span = my_matches[3].span()
        new_x_min = x_max - (text_span[1] - text_span[0]) * X_VALUE_PER_CHARACTER
        res.append(field_container(field=split_fields[3].strip(), bbox=(new_x_min, y_min, x_max, y_max)))

        #Second field:
        x_middle = new_x_max + (new_x_min - new_x_max)/2
        res.append(field_container(field=split_fields[1].strip(), bbox=(new_x_max + 5, y_min, x_middle, y_max)))

        #Third field:
        res.append(field_container(field=split_fields[2].strip(), bbox=(x_middle + 5, y_min, new_x_min-5, y_max)))

    return res


def extract_prompts(layout, form_fields_dict, prompts_tuple, checkbox_prompt_tuple, field_container, presplit_fields):
    """
    """
    for lt_obj in layout:
        # Handle built-in form fields
        if isinstance(lt_obj, LTText):
            if presplit_fields:
                parse_text(text_field=lt_obj, prompts_dict=form_fields_dict, container=prompts_tuple, \
                            checkbox_container=checkbox_prompt_tuple)
            else:
                text_lst = split_text(text_field=lt_obj, field_container=field_container)
                for text_item in text_lst:
                    parse_text(text_field=text_item, prompts_dict=form_fields_dict, container=prompts_tuple, \
                                checkbox_container=checkbox_prompt_tuple)


def parse_layout(layout: LTPage, prompts_to_inputs_mapping, presplit_fields) -> None:
    """
    Parses the content of a PDF page layout and creates a mapping of the user's inputs to the 
    prompts of the form. It creates this mapping by matching the closest prompts and inputs in the form.

    Args:
        layout (LTPage): The layout object representing the PDF page containing text, images, and containers.
        my_page (dict): The list to store the extracted data (text with bounding boxes and image data).

    Returns:
        None
    """
    form_fields_dict = {'prompts':[], 'long_prompts':[], 'checkbox_prompts':[]}
    customer_input_dict = {'single_input':[], 'checkmarks':[]}
    
    #Look for customer input in vectorized image:
    customer_input_found = check_for_vectorized_image(layout, customer_input_dict, entry_tuple, checkbox_tuple)

    if customer_input_found:
        extract_prompts(layout, form_fields_dict, prompts_tuple, checkbox_prompt_tuple, field_container, presplit_fields)
        create_field_entry_mapping(form_fields_dict, customer_input_dict, prompts_to_inputs_mapping, layout.pageid)
    else:
        pair_text(layout, prompts_to_inputs_mapping, y_delta = 10.0, x_delta = 25.0)

    return None


def parse_page(doc_pages, client_info) -> None:
    """
    Iterates through the pages of a document and parses each page's content.

    Args:
        doc_pages (iterable): An iterable of pages extracted from a PDF document.
        client_info (dict): A mapping of the parsed data for each page.

    Returns:
        None: The function modifies the provided `client_info` list, adding data for each parsed page.
    """
    for page in doc_pages:
        if page.pageid == 1:
            splitted_fields = check_for_split_fields(page)
        parse_layout(layout=page, prompts_to_inputs_mapping=client_info, presplit_fields=splitted_fields)
    return None


def extract_customer_data(pdf_file_path: str, customer_data: dict) -> None:
    """
    Extracts customer-specific data from a PDF form, parsing multiple pages if needed.

    Args:
        pdf_file_path (str): The path to the PDF file containing the customer's form.
        customer_data (dict): Dictionary that will contain the mapping between prompts 
        and responses

    Returns:
        None
    """
    #Parameters used to extract fields from the PDF guest form:
    laparams = LAParams(line_overlap=0.5, char_margin=2, line_margin=0.5, 
                        word_margin=0.1, boxes_flow=0.25, detect_vertical=False, all_texts=True)
    
    #Extract pages from client's forms
    pages = extract_pages(pdf_file_path, maxpages=4, page_numbers=[0, 1, 2, 3], laparams=laparams)
    
    #Parse form pages:
    parse_page(pages, customer_data)
    
    return


if __name__=="__main__":
    #Debugging:
    customer_files = []
    for f in os.listdir('./guest_data/'):
        # if f == 'guest_name_in_folder OB Paperwork.pdf':
        if f.endswith('pdf'):
            customer_files.append(f)
            print(f)
    
    for customer in customer_files:
        print(f"------------------{customer}-------------------")
        pdf_path = f'./guest_data/{customer}'
        prompt_input_mapping = {}
        extract_customer_data(pdf_path, prompt_input_mapping)

        for prompt, response in prompt_input_mapping.items():
            print(prompt, response)
        print("\n\n\n")
