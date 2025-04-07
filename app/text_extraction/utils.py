import os
from .constants import SPLIT_THRESHOLD
from docx.enum.section import WD_ORIENT


def get_files_in_directory(directory, ext='.pdf'):
        """
        Gets the list of files in the current directory.

        Args:
            directory (str | Path): path where the customer files are located
            extension (str): type of files containing customer data

        Returns:
            list: A list of file names in the directory with the matching file extension.
        """
        if not os.path.isdir(directory):
            return []
        return [f for f in os.listdir(directory) if f.endswith(ext)]


def change_orientation(document):
    """
    Changes the orientation of the document if there are more than 2 guests

    Args:
        document (Document): word document where guest data is stored
    
    Returns:
        None
    """
    #Select section of word document where table will go:
    current_section = document.sections[0]

    #Rotate document and swap height and width:
    current_section.orientation = WD_ORIENT.LANDSCAPE
    current_section.page_width = document.sections[0].page_height
    current_section.page_height = document.sections[0].page_width



def check_for_split_fields(layout):
    """
    Checks if the fields of the PDF are pre-split based on the average length of text in the 
    first page of the PDF. If the average text length is less than SPLIT_THRESHOLD (user defined global
    variable) then the fields are already split, otherwise we need to process each line and define the
    bounding boxes for the text.
    This check is required because extracting text using pdfminer.six with LaParams doesn't always
    result in proper text split.

    Args:
        layout (LTPage): page containing the elements of the pdf document.
    
    Returns:
        bool: True is the fields are split, False otherwise
    """
    num_items = len(layout._objs)
    total_width = 0

    for item in layout:
        total_width += item.width

    return True if (total_width / num_items < SPLIT_THRESHOLD) else False

