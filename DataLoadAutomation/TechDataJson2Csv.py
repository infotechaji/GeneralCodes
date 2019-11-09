"""
    Description: This module combine all the json files of technical data into a flat file compatible with BCP.
    Version    : v2.0
    History    :
                v1.0 - 12/22/2016 - Initial version
                v1.1 - 06/27/2016 - Output columns are ordered
                v2.0 - 09/11/2018 - redirected domain is captured as "actual_domain " in tech_results file
    Open Issues: None.
    Pending :    None.
"""
import sys
from JSONFlatten import *
from FileHandling import *
from Utilities import *
from WebsiteCodesSupport import * 

# with open('TechnologyClassification.json') as target:
    # cluster_details=json.load(target)
# output_directory='E:\\_data\\JulyRefresh\\technewjune\\wwwsmb_new\\target'
# if not os.path.isdir(output_directory):
#     try:
#         os.makedirs(output_directory)
#     except OSError as exc: # Python >2.5
#         if exc.errno == errno.EEXIST and os.path.isdir(output_directory):
#             pass
#         else: raise
        
        
def cluster_technology(category,name): # checks and returns the cluster
    cluster_details=''
    with open('TechnologyClassification.json') as target:
        cluster_details=json.load(target)
    for each_cluster in cluster_details:
        if category.lower() in cluster_details[each_cluster] and name.lower() in cluster_details[each_cluster][category.lower()]:
            return each_cluster.title()
    return ''

def get_all_json(input_directory): # returns all the json in the given directory
    f_h_ins=FileHandling()
    all_files_list=f_h_ins.get_all_files(directory_is=input_directory,pattern='*.json',full_path=True,recursive=False)
    return all_files_list
def JsonToFile(input_directory,output_directory=''):
    if input_directory and not output_directory:
        output_directory=os.path.join(input_directory,'combined')
    if not os.path.isdir(output_directory):
        try:
            os.makedirs(output_directory)
        except OSError as exc: # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(output_directory):
                pass
            else: raise
    # with open('TechnologyClassification.json') as target:
    #     cluster_details=json.load(target)
    jf=JSONFlatten(print_instance=None,field_separator='.',list_separator_style='dot',debug_mode=True,max_debug_record_count=0,select_record_is=0)
    jf_data=JSONFlatten(print_instance=None,field_separator='.',list_separator_style='dot',debug_mode=True,max_debug_record_count=0,select_record_is=0)
    json_flatten_data=JSONFlatten(print_instance=None,field_separator='.',list_separator_style='dot',debug_mode=True,max_debug_record_count=0,select_record_is=0)
    # Just creates three objects.
    flattenJSON_collection=[]
    flattenJSON_data_collection=[]
    flattenJSON_data_collection_list=[]
    all_files_list=get_all_json(input_directory) # get all files in the given directory
    output_file_prefix='v1'
    file_count=0
    for each_file in all_files_list:
        file_count += 1
        print 'File count:' + str(file_count) #+ '\t File Name:' + repr(each_file)
        f_h_c=open(each_file,'r')
        current_content=f_h_c.read()
        if jf.is_JSON(current_content): # return True if input is JSON
            json_object=jf.get_JSON(current_content) # returns the JSON(content)
            if 'output_json' in json_object:
                if 'list_of_companies' in json_object['output_json'][0]:
                    for each_record in json_object['output_json'][0]['list_of_companies']:
                        temp_one_time_dict={}
                        if 'Domain_name' in each_record:
                            temp_one_time_dict['Domain_name']=each_record['Domain_name']
                            #temp_one_time_dict['actual_domain']=each_record['Domain_name']
                        else:
                            print 'Domain_name is not in json_object[\'output_json\'][\'list_of_companies\']'
                            continue
                        if 'Domain_Identifier' in each_record:
                            temp_one_time_dict['Domain_Identifier']=each_record['Domain_Identifier']
                        else:
                            temp_one_time_dict['Domain_Identifier']=''
                        if 'site_info' in each_record:
                            temp_one_time_dict.update(each_record['site_info'])
                            #print 'site_info  record:',each_record
                            temp_one_time_dict['website']=each_record['site_info']['url']
                            #print 'website updated !! : ',temp_one_time_dict['website']
                        if 'url' in temp_one_time_dict:
                            temp_one_time_dict['result_url']=temp_one_time_dict.pop('url')
                        else:
                            temp_one_time_dict['result_url']=''
                        if 'statistics_info' in each_record:
                            temp_one_time_dict.update(each_record['statistics_info'])
                        if 'urls' in temp_one_time_dict:
                            temp_one_time_dict['urls_count']=temp_one_time_dict.pop('urls')
                        if 'data' in each_record:
                            temp_one_time_dict['temp_status']='Records:' + str(len(each_record['data']))
                            flattenJSON_Result=jf.get_Flatten_JSON(temp_one_time_dict.copy())
                            if 'flattenJSON' in flattenJSON_Result:
                                flattenJSON_collection.append(flattenJSON_Result['flattenJSON'].copy())
                            flattenJSON_Result.clear()
                            redirected_url=''
                            for each_data_record in each_record['data']:
                                if each_data_record['category'] =='Redirect':
                                    redirected_url=each_data_record['url']
                                    break
                            for each_data_record in each_record['data']:
                                new_temp_dict_recursive={}
                                data_dict={}
                                new_temp_dict_recursive.update(each_data_record.copy())
                                data_dict.update(each_data_record.copy())
                                new_temp_dict_recursive['result_url']=temp_one_time_dict['result_url']
                                new_temp_dict_recursive['Domain_name']=temp_one_time_dict['Domain_name']
                                if redirected_url and temp_one_time_dict['Domain_name'].strip(' \t\r\n').lower()!=redirected_url.strip(' \r\t\n').lower():
                                    new_temp_dict_recursive['actual_domain']=redirected_url#temp_one_time_dict['Domain_name']
                                else:
                                    new_temp_dict_recursive['actual_domain']=temp_one_time_dict['Domain_name']
                                    
                                new_temp_dict_recursive['Domain_Identifier']=temp_one_time_dict['Domain_Identifier']
                                new_temp_dict_recursive['website']=temp_one_time_dict['website']
                                if 'category' in new_temp_dict_recursive:
                                    # if new_temp_dict_recursive['category'] =='Redirect':
                                        # print ('Redirected URL : Found')
                                        # print ('Actual domain before  :',new_temp_dict_recursive['actual_domain'])
                                        # new_temp_dict_recursive['actual_domain']=new_temp_dict_recursive['url']
                                        # print ('Actual domain Changed !!:',new_temp_dict_recursive['actual_domain'])
                                    if new_temp_dict_recursive['category'] == 'CDN' and 'cdnhost' in new_temp_dict_recursive and 'cdnurl' in new_temp_dict_recursive:
                                        new_temp_dict_recursive['name']=new_temp_dict_recursive.pop('cdnhost')
                                        new_temp_dict_recursive['link']=new_temp_dict_recursive.pop('cdnurl')
                                        data_dict['technology_name']=data_dict.pop('cdnhost')
                                        data_dict['link']=data_dict.pop('cdnurl')
                                    if new_temp_dict_recursive['category'] == 'Interesting' and 'url' in new_temp_dict_recursive:
                                        new_temp_dict_recursive['link']=new_temp_dict_recursive.pop('url')
                                        data_dict['link']=data_dict.pop('url')
                                #list_of_result_collection.append(new_temp_dict_recursive.copy())
                                    if 'name' in new_temp_dict_recursive:
                                        new_temp_dict_recursive['cluster']=cluster_technology(new_temp_dict_recursive['category'],new_temp_dict_recursive['name'])
                                    else:
                                        new_temp_dict_recursive['cluster']=''
                                
                                flattenJSON_Result=jf_data.get_Flatten_JSON(new_temp_dict_recursive.copy())
                                if 'flattenJSON' in flattenJSON_Result:
                                    flattenJSON_data_collection.append(flattenJSON_Result['flattenJSON'].copy())
                                data_dict['lookup_domain']=temp_one_time_dict['Domain_name']
                                data_dict['result_domain']=new_temp_dict_recursive['actual_domain']
                                new_temp_dict_recursive.clear()
                                flattenJSON_Result.clear()
                                if 'link' in data_dict: data_dict['technology_url']=data_dict['link']
                                if 'name' in data_dict: data_dict['technology_name']=data_dict['name']
                                if 'category' in data_dict:
                                    if data_dict['category'] =='subdomain':
                                        data_dict['technology_name']=data_dict['title']
                                    elif data_dict['category'] =='Interesting':
                                        data_dict['technology_name']=data_dict['note']
                                    elif data_dict['category'] !='NameServer' and data_dict['category'] !='SSL' and  data_dict['category'] !=' Hosting' and  data_dict['category'] !='CDN' and  data_dict['category'] !='Redirect' and data_dict['category'] !='Website IP':
                                         if 'version' in  data_dict:
                                             data_dict['technology_version']=data_dict['version']
                                    if data_dict['category'] == 'Website IP':
                                        data_dict['technology_name']=temp_one_time_dict['ip']
                                        data_dict['technology_version']=temp_one_time_dict['urls_count']
                                        data_dict['description']=temp_one_time_dict['cookies']
                                    if data_dict['category'] == 'Tool':
                                         data_dict['description'] = data_dict['used_for']
                                    if data_dict['category'] =='subdomain':
                                        if 'hostname' in data_dict:
                                            data_dict['result_domain']=data_dict['hostname']
                                        # if data_dict['category'] != 'Redirect':
                                            # ins = WebURLParse(temp_one_time_dict['result_url'])
                                            # website_domain = ins.get_website_domain_name()
                                            # data_dict['result_domain']=website_domain
                                        if True:
                                            data_dict['technology_url'] =temp_one_time_dict['result_url']
                                            ins = WebURLParse(temp_one_time_dict['result_url'])
                                            website_domain = ins.get_website_domain_name()
                                            data_dict['result_domain']=website_domain
                                flattenJSON_Result=json_flatten_data.get_Flatten_JSON(data_dict.copy())
                                if 'flattenJSON' in flattenJSON_Result:
                                    flattenJSON_data_collection_list.append(flattenJSON_Result['flattenJSON'].copy())
                                data_dict.clear()
                                flattenJSON_Result.clear()
                        else:
                            #print 'No Data information'
                            temp_one_time_dict['temp_status']='No Data'
                            #list_of_result_collection.append(temp_one_time_dict.copy())
                            flattenJSON_Result=jf.get_Flatten_JSON(temp_one_time_dict.copy())
                            if 'flattenJSON' in flattenJSON_Result:
                                flattenJSON_collection.append(flattenJSON_Result['flattenJSON'].copy())
                            flattenJSON_Result.clear()
                        temp_one_time_dict.clear()
                else:
                    print 'list_of_companies is not in json_object[\'output_json\']'
            else:
                print 'output_json is not in json_object'
        else:
            print ('Not a JSON:' + current_content)
            custom_exit()
    result_is=[]
    flattenJSON_keys=['Domain_name','ip','result_url','raw_url','temp_status','urls_count','cookies','start_time','run_time','fingerprints','error','rawurl']
    jf.write_delimited_file(file_name=os.path.join(output_directory,output_file_prefix + '_' + 'technical_data_header.dat'),list_of_JSON=flattenJSON_collection,list_of_keys=flattenJSON_keys,column_separator='|^|',encode=True)
    flattenJSON_data_keys=['Domain_Identifier','Domain_name','actual_domain','category','name','version','result_url','hostname','title','used_for','ip','note','link','num','category_type','cluster']
    #flattenJSON_data_keys=[]
    jf_data.write_delimited_file(file_name=os.path.join(output_directory,output_file_prefix + '_' + 'combined_tech_results.dat'),list_of_JSON=flattenJSON_data_collection,list_of_keys=flattenJSON_data_keys,column_separator='|^|',encode=True)
    flattenJSONdatakeys=['lookup_domain','category','technology_name','technology_version','result_domain','technology_url','description']
    json_flatten_data.write_delimited_file(file_name=os.path.join(output_directory,output_file_prefix + '_' + 'technical_data_detail_core_ui.dat'),list_of_JSON=flattenJSON_data_collection_list,list_of_keys=flattenJSONdatakeys,column_separator='|^|')
    return True
if __name__ == '__main__':
    input_directory='E:\\Ajith\\_code\\_code\\Tech_flatten\\JSONDirectory\\full_test'
    output_directory=os.path.join(input_directory,'combined')
    results =JsonToFile(input_directory=input_directory)
    