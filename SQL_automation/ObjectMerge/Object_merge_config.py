import os 
# To effectively handle the missing of single words in addition
SPL_SINGLE_WORD_CASES = ['end', '(', ')', 'begin', 'return', 'if']

# To detect the beginning of commented sections
START_BLOCK_CHARS = ['/*','--'] # '--', Future cases , code added on 29-sep-2020
START_BLOCK_WORDS = [' start', ' begin']

# To detect the compeltion of commented sections
END_BLOCK_CHARS = ['*/','--'] # '--', Future cases , code added on 29-sep-2020
END_BLOCK_WORDS = [' end']

SIMILARITY_THRESHOLD = 82
LINE_THRESHOLD_PERCENTAGE = 0.15    #  15 percentage

# Object merge logs
OBJECT_MERGE_FULL_LOG = 'OBJECT_MERGE_FULL_LOG.txt'

# GIT Automation input generation
GIT_AUTOMATION_DEFAULT_INPUT ='GITAutomation_auto_input.txt'
OBJECT_MERGE_GIT_INPUT_LOG = 'OBJECT_MERGE_GIT_INPUT_FULL_LOG.txt'
OBJECT_MERGE_DEEP_SP_LOG = 'OBJECT_MERGE_GIT_INPUT_SPS_LOG.txt'
OBJECT_MERGE_CONSOLIDATED_FILE = 'OBJECT_MERGE_CONSOLIDATED_FILE.txt'
OBJECT_MERGE_CONSOLIDATED_LOG = 'OBJECT_MERGE_CONSOLIDATED_LOG.txt'
GIT_MASTER_PATH = 'G:\\Ajith\\Ramco-GIT\\GIT\\blgt'

# GIT_DEPLOYMENT_MANDATORY_PATCH_PATH = 'G:\\Ajith\\Ramco-GIT\\GIT\\blgt\\01-Source\\Patches\\Patches_Mandatory\\Appln'
GIT_DEPLOYMENT_MANDATORY_PATCH_PATH = os.path.join(GIT_MASTER_PATH,'01-Source\\Patches\\Patches_Mandatory\\Appln')


