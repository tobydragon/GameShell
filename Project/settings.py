LOG_SELECTIONS = False  # Log each time a user selects or deselects a card
LOG_STAGE_EVALS = True  # Log each time a stage is evaluated
DOMAIN_FILE = "wfb_dataset.csv"
QUESTIONS_FILE = 'wfb_dataset.question_set.json'
DOMAIN_FIELD_TYPE_HEADER = True # Whether the domain file has a datatype header row
STAGES_PER_QUESTION = 2
RANDOM_SEED = 3#None # Sets the random seed. Used for testing&demonstration, if oyu want the same series of questions. Default is None
IMAGEPATH_TEMPLATE="images_insects/{}.jpg" # Path to images. Any "{}" is replaced with value from datafile. Default is None or ""

# DEV SETTINGS
SOFTWARE_VERSION = "0.1"