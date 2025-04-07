from collections import namedtuple


#Stores the prompts/questions in the forms:
prompts_tuple = namedtuple(typename='Prompts', field_names=['field', 'y_coord', 'x_coord'])

#Stores the checkbox prompts in the forms:
checkbox_prompt_tuple = namedtuple(typename='Checkbox_prompt', field_names=['field', 'x_min', 'y_min', 'x_max', 'y_max'])

#Stores the entries/responses by clients:
entry_tuple = namedtuple(typename='Entry', field_names=['text', 'y_coord', 'x_coord'])

#Stores the selections/checkmarks made by clients:
checkbox_tuple = namedtuple(typename='Checkbox', field_names=['y_avg', 'x_avg'])

#Stores
field_container = namedtuple(typename='Split_field', field_names=['field', 'bbox'])