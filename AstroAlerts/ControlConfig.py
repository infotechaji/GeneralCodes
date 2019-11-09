"""
    Content Type: Config Values
    Description: This config file has parameters used to connect to the database.
    Version    : v2.0
    History    :
                v1.0 - 03/30/2015 - Initial version
                v1.1 - 05/01/2015 - Process parameters for News is added.
                v1.2 - 05/06/2015 - Process parameters for Twitter is added.
                v1.3 - 05/19/2015 - Process parameters for Tending Topic is added.
                v1.4 - 06/01/2015 - Process Semaphore parameters for Tending Topic (PROCESS_NAME_TOPIC_UPLOAD_SUFFIX and PROCESS_NAME_TOPIC_PROCESS_SUFFIX) are added.
                v1.5 - 06/05/2015 - Bing API Key is added - BING_API_KEY. New Parameter PROCESS_TOPICS_TRENDING - will enable or disable running SP to move topics trending data from state to ui.
                                  - Added parameters FETCH_INDUSTRY_NEWS and INDUSTRY_NEWS_KEYWORD but disabled the same for future use.
                v1.6 - 06/16/2015  - Added new SPLIT_VAL_LIST for removing news sources from newsfeeds
                v1.7 - 06/17/2015  - Added new COMP_EXTENSIONS for removing company extensions in data_feed_identifier of post_feed for News
                v1.8 - 07/14/2015 - Variable INSTANCE_NAME is added for identification. Added API_HOST , API_PORT and MAIL_ADDRESS_PROCESS_NOTIFICATION
                v1.9 - 10/29/2015 - added TRACK_TIME_MODE
                v1.10 - 11/17/2015 - Added WRITE_TO_PSQL_NEWS_COLLECT and added variables for PICKLE FILEs
                v2.0  - 07/20/2016 - Retain the variable which are required for the checked-in modules
    Procedure to use: Import this config file into all python scripts where database operation is performed
    Open Issues: None.
    Pending :    None.
"""
#Leaving this place blank. If there is a need, then this file will be used.
