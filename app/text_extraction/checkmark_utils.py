from .constants import *


def check_selection(checkbox_prompt, customer_checkmark):
    """
    Verifies whether a customer's checkmark is inside a given checkbox prompt.

    Args:
        checkbox_prompt: The prompt defining the checkbox area.
        customer_checkmark: The detected checkmark location.

    Returns:
        A tuple containing the category and selected value if a match is found, otherwise (field, False).
    """
    if not is_checkmark_inside_checkbox(checkbox_prompt, customer_checkmark):
        return checkbox_prompt.field, False
    
    clean_prompt = checkbox_prompt.field.split(':')[0].strip()
    
    if 'Gender' in checkbox_prompt.field:
        return check_gender_selection(checkbox_prompt, customer_checkmark)
    
    if clean_prompt in DIET_OPTIONS:
        return check_diet_preference(customer_checkmark)
    
    if clean_prompt in SHIRT_OPTIONS:
        return check_shirt_size_selection(customer_checkmark, clean_prompt)
    
    if clean_prompt in ROOM_OPTIONS:
        return check_room_type_selection(customer_checkmark)
    
    if clean_prompt in BED_OPTIONS:
        return check_bed_type_selection(customer_checkmark)
    
    return checkbox_prompt.field.strip(), True


def parse_checkboxes(checkbox, customer_input_dict, container):
    """
    Gets a figure and extract the bounding box coordinates and calculates the average x
    and y coordinates. Appends the coordinates to checkbox_list for further processing, i.e.
    mapping the coordinate to a choice on the form.

    Args:
        checkbox (LTFigure): check mark showing the customer's choice
        customer_input_dict (dict): list containing checkbox coordinates
    
    Returns:
        None
    """
    try:
        x_min, y_min, x_max, y_max = checkbox.bbox
        x_avg = (x_min + x_max) / 2
        y_avg = (y_min + y_max) / 2
        customer_input_dict['checkmarks'].append(container(y_avg, x_avg))
    except AttributeError:
        return


def is_checkmark_inside_checkbox(checkbox_prompt, customer_checkmark):
    """Checks if the checkmark coordinates fall within the checkbox boundaries."""
    return (
        checkbox_prompt.y_min < customer_checkmark.y_avg < checkbox_prompt.y_max and
        checkbox_prompt.x_min < customer_checkmark.x_avg < checkbox_prompt.x_max
    )


def check_gender_selection(checkbox_prompt, customer_checkmark):
    """Determines the gender selection based on the checkmark position."""
    check_map = CHECK_MAP_GENDER if checkbox_prompt.x_min >= 45 else CHECK_MAP_GENDER_OLD
    for key, value in check_map.items():
        if abs(value - customer_checkmark.x_avg) <= CHECKBOX_THRESHOLD:
            return 'gender', key
    return 'gender', None


def check_diet_preference(customer_checkmark):
    """Determines the diet preference selection."""
    for key, value in {**DIET_PREFERENCES, **DIET_PREFERENCES_OLD}.items():
        if abs(value - customer_checkmark.x_avg) <= CHECKBOX_THRESHOLD:
            return 'diet preference', key
    return 'diet preference', None


def check_shirt_size_selection(customer_checkmark, clean_prompt):
    """Determines the selected shirt size category."""
    size_category = " (Adult)" if customer_checkmark.x_avg < 250 else " (Youth)"
    return 'shirt size', clean_prompt + size_category


def check_room_type_selection(customer_checkmark):
    """Determines the selected room type."""
    for key, value in ROOM_TYPE.items():
        if abs(value - customer_checkmark.y_avg) <= CHECKBOX_THRESHOLD:
            return 'room type', key
    return 'room type', None


def check_bed_type_selection(customer_checkmark):
    """Determines the selected bed type."""
    for key, value in BED_TYPE.items():
        if abs(value - customer_checkmark.y_avg) <= CHECKBOX_THRESHOLD:
            return 'bed type', key
    return 'bed type', None
