import re
import string


TITLES = [
    'Name', 
    'Preferred name', 
    'Address & Phone numbers', 
	'Birth date', 
	'Age', 
	'Gender', 
	'Email',
    'Passport country and number', 
	'Place of issue', 
	'Date of issue', 
	'Expiration date',
    'Room type/Bed type', 
	'Roommate', 
	'Emergency contact', 
	'Diet preference', 
	'Exclude from diet',
    'Allergies', 
	'Life threatening allergies', 
	'Medications', 
	'Blood Type',
    'Other Medical Information', 
	'Fitness Level', 
	'Travel/Medical Insurance', 
	'Flying Doctors',
    'Special Occasion', 
	'Height', 
	'Weight', 
	'Shirt size', 
	'Additional Info'
]



###--------------------------------------------------------------------------###
###-----------------------------THRESHOLD VALUES-----------------------------###
###--------------------------------------------------------------------------###
SPLIT_THRESHOLD = 250
X_VALUE_PER_CHARACTER = 5
CHECKBOX_THRESHOLD = 10
PUNC_REGEX = re.compile('[{}]'.format(re.escape(string.punctuation)))


###--------------------------------------------------------------------------###
###-----------------------------ALLERGY KEYWORDS-----------------------------###
###--------------------------------------------------------------------------###
DESCRIBE_OPTIONS = ['Allergies ', 'Life threatening ', 'Antibiotics ']


###------------------------------------------------------------------------------###
###-----------------------------LONG PROMPT KEYWORDS-----------------------------###
###------------------------------------------------------------------------------###
LONG_KEYWORDS = {'members', 'exclude', 'yes', 'below', 'fitness', 'equipment', 'roommate', \
                'limitations', 'conditions', 'relation', 'celebrating'}


###---------------------------------------------------------------------------###
###-----------------------------CHECKBOX KEYWORDS-----------------------------###
###---------------------------------------------------------------------------###
CHECKBOX_OPTIONS = {'Regular', 'Other', 'No preference', 'Vegetarian', 'Vegan', 'Gluten-Free', 'Lactose-Free',\
                'Pescatarian', 'Kosher', 'Single', 'Shared', 'Tent', 'Twin', 'Double',\
                'Small', 'Med', 'Large', 'XL', 'XXL', 'Gender', 'Adult Small', 'Youth Small'}


###------------------------------------------------------------------------###
###-----------------------------GENDER OPTIONS-----------------------------###
###------------------------------------------------------------------------###
#pre-split locations (Gender and diets aren't split, but shirt sizes and accomodations are):
#need to be mindful of Gender-Weight vs Weight-Gender use x_min or x_max accordingly.
#Weight-Gender: 154.91845314 513.2799375239999
#Gender: Female: 325.73, Male: 384.29, Non-specified: 434.69

#Gender-Weight: 36 477.2799375239999
#Gender: Female: 207.73, Male: 265.29, Non-specified: 320
CHECK_MAP_GENDER = {'Male': 207.73, 'Female': 265.29, 'Non-specified': 320}
CHECK_MAP_GENDER_OLD = {'Female': 325.73, 'Male': 384.29, 'Non-specified': 434.69}


###----------------------------------------------------------------------###
###-----------------------------DIET OPTIONS-----------------------------###
###----------------------------------------------------------------------###
#Diets-old: 36.0 446.11218752399986
#Diets: No preference: 121.73, Vegetarian: 201.89, Vegan: 259.49, Gluten-Free: 343.97, Lactose-Free: 432.29

#Diets-old: 36.0 249.0778593959999
#Diets: Pescaterian: 109.25 , Other: 163.01, Please explain:
DIET_OPTIONS = {'No preference', 'Vegetarian', 'Vegan', 'Gluten-Free', 'Lactose-Free',\
                'Pescatarian', 'Kosher', 'Regular', 'Other'}
DIET_PREFERENCES = {'Regular': 88, 'Vegetarian': 239, 'Vegan': 369.49, 'Gluten-Free': 517, 
                        'Lactose-Free': 110, 'Pescaterian': 271 , 'Other': 534, 'Kosher': 403}
DIET_PREFERENCES_OLD = {'No preference': 121.73, 'Vegetarian': 201.89, 'Vegan': 259.49, 'Gluten-Free': 343.97, 
                        'Lactose-Free': 432.29, 'Pescaterian': 109.25 , 'Other': 163.01}


###----------------------------------------------------------------------###
###-----------------------------ROOM OPTIONS-----------------------------###
###----------------------------------------------------------------------###
ROOM_BED_OPTIONS = {'Single', 'Shared', 'Family Tent  ___', 'Single rooms',  'Twin (one per bed)', \
                    'Double (Shared)', 'Family Tent'}
ROOM_OPTIONS = {'Single', 'Shared', 'Family Tent  ___', 'Family Tent'}
ROOM_TYPE = {'Single': 555, 'Shared': 530, 'Family Tent  ___':505}
ROOM_TYPE_OLD = {'Single': 555, 'Shared': 530, 'Family Tent  ___':505}
ROOM_TYPE_OLD2 = {'Single': 109, 'Shared': 109, 'Family Tent  ___':110.11}


###---------------------------------------------------------------------###
###-----------------------------BED OPTIONS-----------------------------###
###---------------------------------------------------------------------###
BED_OPTIONS = {'Single rooms',  'Twin (one per bed)', 'Double (Shared)'}
BED_TYPE = {'Single rooms': 555,  'Twin (one per bed)': 530, 'Double (Shared)': 505}
BED_TYPE_OLD = {'Single rooms': 555,  'Twin (one per bed)': 530, 'Double (Shared)': 505}
BED_TYPE_OLD2 = {'Single rooms': 413,  'Twin (one per bed': 440.35, 'Double (Shared)': 428}


#Accommodations:
#Single: 109.73             89.47
#Single rooms: 413.47
#Shared: 109.73             94.75
#Family Tent: 110.69        110.11
#Twins: 439.49              440.35
#Double (Shared): 439.49    428.83
# ACCOMMODATION_OPTIONS_OLD = {'Single rooms': 413, 'Shared': 109, 'Twin (one per bed': 439.35,\
#                         'Family Tent  ___':110.69, 'Double (Shared)': 439}


###-----------------------------------------------------------------------###
###-----------------------------SHIRT OPTIONS-----------------------------###
###-----------------------------------------------------------------------###
#Y-coordinate:
SHIRT_OPTIONS = {'Adult Small', 'Youth Small', 'Med', 'Large', 'XL','XXL', 'Adult    Small'}
SHIRT_LOCATIONS = {'Small': 445, 'Med': 420, 'Large': 395, 'XL': 370,'XXL': 345}
SHIRT_LOCATIONS_OLD = {'Small': 445, 'Med': 420, 'Large': 395, 'XL': 370,'XXL': 345}

