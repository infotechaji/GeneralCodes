USER_NAME = 'O48090'
GIT_SOURCE_LINK = 'https://ops.ramcouat.com/gitlab/users/sign_in'
PASSWORD = 'Ajisedin@123'

# NEW_MERGE_REQUEST_PATTERN = 'https://ops.ramcouat.com/gitlab/ramco-logistics/lgt/blgt/merge_requests/new?utf8=%E2%9C%93&merge_request%5Bsource_project_id%5D=438&merge_request%5Bsource_branch%5D=<source_branch>&merge_request%5Btarget_project_id%5D=438&merge_request%5Btarget_branch%5D=<destination_branch>'
# NEW_MERGE_REQUEST_PATTERN = 'https://ops.ramcouat.com/gitlab/ramco-logistics/lgt/blgt/merge_requests/new?utf8=%E2%9C%93&merge_request%5Bsource_project_id%5D=438&merge_request%5Bsource_branch%5D=dev-<epe_id>-V3.189-Controlled&merge_request%5Btarget_project_id%5D=438&merge_request%5Btarget_branch%5D=<destination_branch>'
NEW_MERGE_REQUEST_PATTERN = 'https://ops.ramcouat.com/gitlab/ramco-logistics/lgt/blgt/merge_requests/new?utf8=%E2%9C%93&merge_request%5Bsource_project_id%5D=438&merge_request%5Bsource_branch%5D=<source_branch>&merge_request%5Btarget_project_id%5D=438&merge_request%5Btarget_branch%5D=<destination_branch>'
EPE_TRACE_PATTERN = 'https://ops.ramcouat.com/gitlab/ramco-logistics/lgt/blgt/merge_requests?scope=all&utf8=%E2%9C%93&state=all&search=<epe_id>'

SUBMIT_TEXTS = ['submit merge request','submit']
CASES_TO_IGNORE = ['compare branches and continue']

MERGE_REQUEST_HEADERS= 'SOURCE_BRANCH\tDESTINATION_BRANCH\tBRANCH_PRESENCE\tCOMMIT_MESSAGE_MATCH\tMERGE_REQUEST_STATUS\tMERGE_REQUEST_ID\n'
AUTO_MERGE_REQUEST_LOG = 'G:\\Ajith\\OtherFiles\\GITAutomation\\AUTO_RAISED_MERGE_REQUEST_LOG.txt'
# AUTO_MERGE_REQUEST_LOG = 'AUTO_RAISED_MERGE_REQUEST_LOG.txt'

AUTO_MERGE_REQUEST_FILE = 'Auto_raised merge_requests.txt'

# AUTO_EPE_TRACE_LOG = 'AUTO_EPE_TRACE_LOG.txt'
AUTO_EPE_TRACE_LOG = 'G:\\Ajith\\OtherFiles\\GITAutomation\\AUTO_EPE_TRACE_LOG.txt'
AUTO_EPE_TRACE_FILE = 'Auto_epe_trace.txt'
EPE_TRACE_HEADERS ='NO\tTOTAL_RECORDS\tEPE-ID\tEPE_TITLE\tMERGE_REQ_ID\tAUTHOR\tTARGET_BRANCH\tSTATUS\tPERIOD\n'


COMMIT_MESSAGE_PATTERN = '[<epe_id>]'