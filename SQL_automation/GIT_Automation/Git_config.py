import os 
#  Credentials
USER_NAME = 'O48090'
MAIL_ID = ''
PASSWORD = 'Ajisedin@123'

# Deployment file patters
GIT_DEPLOYMENT_PATTERN_1 = os.path.join(os.getcwd(),'GIT_template_01.txt')
GIT_DEPLOYMENT_PATTERN_2 = os.path.join(os.getcwd(),'GIT_template_02.txt')


# Command to save the password permanently
# -- git config --global credential.helper "cache --timeout=7200"


# GIT_MASTER_PATH = 'G:\\Ajith\\Ramco-GIT\\GIT\\blgt'
GIT_MASTER_PATH = 'G:\\Ajith\\Ramco-GIT\\GIT\\190\\blgt'


# GIT_DEPLOYMENT_DEFAULT_PATH = 'G:\\Ajith\\Ramco-GIT\\GIT\\blgt\\01-Source\\<DEPLOYMENT_FOLDER>\\Rm\\<SUB_FOLDER>\\Appln'
GIT_DEPLOYMENT_DEFAULT_PATH = os.path.join(GIT_MASTER_PATH,'01-Source\\<DEPLOYMENT_FOLDER>\\Rm\\<SUB_FOLDER>\\Appln')

MANDATORY_PATCH_PATH = '01-Source\\Patches\\Patches_Mandatory\\Appln'
# GIT_DEPLOYMENT_MANDATORY_PATCH_PATH = 'G:\\Ajith\\Ramco-GIT\\GIT\\blgt\\01-Source\\Patches\\Patches_Mandatory\\Appln'
GIT_DEPLOYMENT_MANDATORY_PATCH_PATH = os.path.join(GIT_MASTER_PATH,MANDATORY_PATCH_PATH)

SP_PATH = 'Sproc'
VIEW_PATH = 'View'

GIT_FILE_LOOKUP ={
                'wma' :['WMACTIVITY']
                ,'wmm' :['WMS_MOBILE']
                ,'wms' :['WMS_MOBILE','WMACTIVITY','WMStockInquiry']
                ,'whr' :['LgtAdmin','WmSetup','LGT_Reports']
                ,'wm_' :['WmSetup'] # G:\Ajith\Ramco-GIT\GIT\blgt\01-Source\WmSetup\Rm\Sproc\Appln added on nov-03
                # ,'wmm' :'WMS_MOBILE'
                ,'bdu':['BulkDataUpload']
                    }
            #  first three letters of sp : Folder to deploy
            #  future cases
            # 'wm_' :''
#           ,'wms' :''

DEPLOYMENT_PATTERN_01= 'Test1.bat'
DEPLOYMENT_PATTERN_02= 'Test2.bat'


# GIT_AUTOMATION_LOG = 'GIT_AUTOMATION_LOG.txt'
GIT_AUTOMATION_LOG = 'G:\\Ajith\\OtherFiles\\GITAutomation\\GIT_AUTOMATION_LOG.txt'
GIT_AUTOMATION_FILE = 'Auto_git_commits_status.txt'


