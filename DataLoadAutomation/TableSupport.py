"""
Functionality : Contains file_pattern,table_name for all the code_key  
Version       : v1.0
History       : 
                v1.0 - 08/21/2018 initial version 
Issues        :
Pending       :
"""

TABLE_SUPPORT={'basic_details':[
                                {'file_pattern':'company_info','table_name':'company_info'},
                                {'file_pattern':'company_attributes','table_name':'company_attributes'},
                                {'file_pattern':'company_location_details','table_name':'company_location_details'},
                                {'file_pattern':'company_reference_links','table_name':'company_reference_links'},
                                {'file_pattern':'post_feed','table_name':'post_feed_PR'},
                                {'file_pattern':'people','table_name':'people_data'}
                                ],
                'tech':[
                        {'file_pattern':'v1_combined_tech_results','table_name':'company_technology_data'}
                        ,{'file_pattern':'technical_data_header.dat','table_name':'company_technology_headers'}
                        ],
                'indeed_jobs':[
                        {'file_pattern':'job_info','table_name':'job_info'}
                        #{'file_pattern':'job_classification','table_name':'job_info_classification'}
                        ],
                'newscode':[
                        {'file_pattern':'post','table_name':'post_feed'}
                        ],
                'fb_activity':[
                        {'file_pattern':'facebook_activity','table_name':'fb_activity'}
                        ],
                'fb_posts':[
                        {'file_pattern':'facebook_posts','table_name':'post_feed_social_media'}
                        ],
                'tw_activity':[
                        {'file_pattern':'twitter_activity','table_name':'tw_activity'}
                        ],
                'tw_posts':[
                        {'file_pattern':'twitter_post','table_name':'post_feed_social_media'}
                        ],
                'hpc':[
                        {'file_pattern':'home','table_name':'hiring_pages_classified'}
                        ],
                'mx':[
                        {'file_pattern':'mx','table_name':'dig_parsed_output'}
                        ]
                }
                
def getTablesList(code_key,table_suffix='',schema='unicode'):
        default_tables=TABLE_SUPPORT[code_key] # list contains file_pattern,table_name
        final_list=[]
        for each_dict in default_tables:
            if table_suffix:
                table_suffix=table_suffix.strip(' \t\r\n')
                table_name=each_dict['table_name']+str(table_suffix)
            else:
                table_name=each_dict['table_name']
            updated_line=each_dict['file_pattern']+'\t'+schema+'\t'+str(table_name)
            final_list.append(updated_line)
        return final_list
            
if __name__=='__main__':
    code_key_list=['basic_details','tech','tw_activity','hpc','tw_posts','fb_activity','fb_posts','newscode','indeed_jobs']
    schema='core_automation'
    for each_code in code_key_list:
        print 'Code :',each_code
        print getTablesList(code_key=each_code,schema=schema)
        print '--------'