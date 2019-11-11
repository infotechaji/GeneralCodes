# -*- coding: utf-8 -*-
"""
    Content Type: Code
    Description: This python file will test the functionalities of Company Website search module
    Version    : v1.0
    History    :
                v1.0 - 07/11/2016 - Initial version.
                v1.1 - 07/20/2016 - Using base class
    Procedure to use: TBD
    Open Issues: None.
    Pending :    None.
"""
import sys
import time
sys.path.insert(0,'..\\common')
from InputOutput import *
from CompanyWebsite import *
if __name__ == '__main__':
    if len(sys.argv)<2:
        print 'Input file is not specified'
        exit()
    filename=sys.argv[1]
    website_list={'telstra  limited'}#'Lowe\'s Companies'}#'iLink Systems Pvt Ltd',
    input_file_name=filename
    ins_r=open(input_file_name,'r')
    ins_io=InputOutput('Feed')
    #ins_io.open()#'inputFile.txt')
    #company_list=ins_io.read(output_format='dict',column_structure=['company_name','country','company_id'])
    search_ins=CompanyWebsiteSearch(developer_mode=False,re_run_mode=False,use_deeper_analysis=True,search_method='DuckDuckGo',financial_domains_to_check=['wikipedia'])
    item_count =0 
    for each_line in ins_r:
        ins_io.open(each_line.strip('\n '))
        each_item=ins_io.read(output_format='dict',column_structure=['company_name','country','company_id'])
        each_item=each_item[0]
        if True:#len(each_item) > 2:
            item_count += 1
            # if item_count<=160: continue
            #print each_item
            #exit()
            try:
                print str(item_count) + '\t Processing:\t' + each_item['company_name']
            except:
                print str(item_count) + '\t Processing:\t' + repr(each_item['company_name'])
            if len(each_item['country']) == 0: each_item['country']=None
            func_result=search_ins.get_company_website(each_item['company_name'],country_name=each_item['country'],record_identifier=each_item['company_id'])
            print str(item_count) + '. WEBSITE IDENTIFIED:\t' + str(each_item) + ':\t' + str(func_result)
            time.sleep(2)
            #break
        # if item_count >= 100000: break
    print 'Process completed'
    ins_r.close()