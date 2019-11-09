import os,sys
from fuzzywuzzy import fuzz
def calculate_match_percent(original_company_name,job_company_name): # calculates the match percent based on the company name .
        if isinstance(original_company_name,unicode):
            original_company_name=original_company_name.encode('utf-8')
        if isinstance(job_company_name,unicode):   
            job_company_name=job_company_name.encode('utf-8')
        partial_ratio = fuzz.partial_ratio(original_company_name.lower(), str(job_company_name).lower()) # 100 % , if it matches slightly or partially
        set_ratio = fuzz.token_set_ratio(original_company_name.lower(), str(job_company_name).lower())
        sort_ratio = fuzz.token_sort_ratio(original_company_name.lower(), str(job_company_name).lower())
        partial_value = round(partial_ratio, 2)
        token_set_value = round(set_ratio, 2)
        token_sort_value = round(sort_ratio, 2)
        total_value = round((partial_value + token_set_value + token_sort_value) / 3)
        return total_value

if __name__=="__main__":
    input_match_companies=open(sys.argv[1]).readlines()
    source_companies=open(sys.argv[2]).readlines()
    temp_list=[]
    # for each_line in input_match_companies:
    #     temp_dict={'company_id':0,'domain_name':''}
    #     line_split=each_line.strip(' \r\n').split('\t')
    #     if len(line_split)==2:
    #         temp_dict['company_id']=line_split[0]
    #         temp_dict['domain_name']=line_split[1].strip('\r\n')
    #         temp_list.append(temp_dict)
    for each_source_line in source_companies:
        source_line_split=each_source_line.strip(' \r\n').split('\t')
        if len(source_line_split)==2:
            for each_input_domain in input_match_companies:
                each_input_domain1=each_input_domain.strip(' \t\r\n')
                each_input_domain=str('.')+each_input_domain1
                if each_input_domain.lower() in source_line_split[1].lower():
                    #each_input_domain=str('.')+each_input_domain
                    match_percent=calculate_match_percent(each_input_domain,source_line_split[1])
                    #print each_input_domain,source_line_split,' match_percent:',match_percent
                    if match_percent>=75.0:
                        print each_input_domain,source_line_split[1],' match_percent:',match_percent
                        final_text=str(source_line_split[0])+'\t'+str(source_line_split[1])+'\t'+str(each_input_domain1)+'\t'
                        final_text+=str(match_percent)
                        final_text+='\n'
                        with open('consolidate_results.txt','a') as fp:
                            fp.write(final_text)
                        #raw_input('next')
            print '.'
    #print 'second for over'
