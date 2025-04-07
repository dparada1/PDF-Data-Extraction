from .checkmark_utils import check_selection



def check_allergy_information(field):
    """
    Check the allergy explain more field and returns the appropriate prompt.

    Args:
        field (Prompts): contains the prompt field and x,y coordinates.
    Returns:
        str: key to be used in prompt/response mapping
    """
    if field.y_coord > 220:
        return 'Any allergies'
    elif field.y_coord < 100:
        return 'Antibiotic allergies'
    else:
        return 'Life threatening allergies'


def neighbors(field, response, y_delta = 10.0, x_delta = 25.0, multiline=False):
    """
    Checks if a field and response are neighbors by checking that they're on the same
    line, i.e. less than y_delta apart, and within an x_delta distance from one another.

    Args:
        field (namedtuple): contains the field text, y coordinate and x coordinate for a 
                            prompt in the form
        response (namedtuple): contains the text, y coordinate and x coordinate for a 
                            user's response
        y_delta (float): maximum y distance between prompt and user reponse
        x_delta (float): maximum x distance between prompt and user reponse
    
    Returns:
        bool: True is prompt and reponse are within delta distance of one another
    """
    if not multiline:
        return (abs(field.y_coord - response.y_coord) < y_delta) and \
                (abs(response.x_coord - field.x_coord) < x_delta)
    
    if 'members' in field.field:
        vertical_dist = field.y_coord - response.y_coord
        return  vertical_dist < (y_delta)*11 and vertical_dist > 0
    elif 'fitness' in field.field:
        vertical_dist = abs(field.y_coord - response.y_coord)
        return  vertical_dist < (y_delta)*3
    else:
        vertical_dist = field.y_coord - response.y_coord
        return  vertical_dist < (y_delta)*6 and vertical_dist > 0



def create_field_entry_mapping(form_fields, customer_inputs, mapping, page_num):
    """
    This creates a dictionary to organize form data using form fields as the keys
    and customer input, including checkboex, as the values

    Args:
    
    Returns:
    """
    if page_num == 1:
        mapping['family members'] = ""
        mapping['roommate'] = ''
        mapping['diet exclusions'] = ''
        mapping['medications'] = ''
        mapping['equipment'] = ''
        mapping['physical limitations'] = ''

    # Mapping short prompts to response
    count = 0
    for field in form_fields['prompts']:
        for customer_input in customer_inputs['single_input']:
            if neighbors(field, customer_input):
                if 'Please describe' in field.field:
                    key = check_allergy_information(field)
                    mapping[key.lower()] = customer_input.text
                    count += 1
                else:
                    if page_num > 1 and 'Email' in field.field:
                        mapping['emergency ' + field.field.lower()] = customer_input.text
                    else:
                        mapping[field.field.lower()] = customer_input.text
                # break
    
    # Mapping long prompts to response
    for long_field in form_fields['long_prompts']:
        for customer_input in customer_inputs['single_input']:
            if neighbors(long_field, customer_input, multiline=True):
                if 'roommate' in long_field.field:
                    mapping['roommate'] = customer_input.text
                elif 'exclude' in long_field.field:
                    mapping['diet exclusions'] += ' ' + customer_input.text
                elif 'medications' in long_field.field or 'need this' in long_field.field:
                    mapping['medications'] += ' ' + customer_input.text
                elif 'equipment' in long_field.field:
                    mapping['equipment'] += ' ' + customer_input.text
                elif 'physical limitations' in long_field.field:
                    mapping['physical limitations'] += ' ' + customer_input.text
                elif 'family' in long_field.field:
                    mapping['family members'] += ' ' + customer_input.text
                elif 'fitness' in long_field.field:
                        mapping['fitness'] = customer_input.text
                elif 'celebrating' in long_field.field:
                        mapping['celebrating'] = customer_input.text
    
    # Mapping choice prompts (checkbox) to response
    for checkbox_promp in form_fields['checkbox_prompts']:
        for customer_checkmark in customer_inputs['checkmarks']:
            prompt, selection = check_selection(checkbox_promp, customer_checkmark)
            if selection:
                mapping[prompt.lower()] = selection
                break
    return


def pair_text(layout, prompts_to_inputs_mapping, y_delta = 10.0, x_delta = 25.0):
    for prompt in layout:
        for response in layout:
            if (prompt != response) and\
                abs(prompt.bbox[2] - response.bbox[0]) < x_delta and \
                abs(prompt.bbox[1] - response.bbox[1]) < y_delta:
                try:
                    prompt = prompt.get_text().strip()
                    response = response.get_text().strip()
                except AttributeError:
                    pass
                if layout.pageid > 1 and 'Email' in prompt:
                    prompts_to_inputs_mapping['Emergency ' + prompt] = response
                else:
                    prompts_to_inputs_mapping[prompt] = response
                break
