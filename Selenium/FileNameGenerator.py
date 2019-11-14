# @dsgersten_David_Gersten_Practice_Manager_-_Dynamic_Consulting
# @dsgersten David Gersten	Practice Manager,	Dynamic Consulting
import os,sys
import os.path
from os import path

temp_folder='dummy_files'
collected_path=os.path.join(os.getcwd(),temp_folder)
if not os.path.exists(collected_path):os.makedirs(collected_path)

def write_into_file(file_name,content='',mode='a'):
    try:
        with open(file_name,mode) as fp:
            try:fp.write(content)
            except:fp.write(content.encode('utf-8'))
        return True
    except Exception as e :
        print('Exception in writing write_into_file :',file_name,e)
        return False
def get_file_name(person_name,designation,company):
    person_name=person_name.strip()
    company=company.strip()
    designation=designation.strip(',').strip()
    spl_characters=[' ','/','\\','\n','\t']
    temp_string=person_name+' '+designation+' - '+company
    for each_char in spl_characters:
        temp_string=temp_string.replace(each_char,'_')
    return {'file_name':temp_string}
if __name__=="__main__":
    input_file_name=sys.argv[1]
    output_file_name=input_file_name.replace('.','._output')
    file_lines=open(input_file_name,'r').readlines()
    count=0
    for each_line in file_lines:
        count+=1
        try:
            splits=each_line.strip(' \t\r\n').split('\t')
            person_name=splits[0].strip(' \r\n')
            designation=splits[1].strip(' \r\n')
            company=splits[2].strip(' \r\n')
        except:continue
        file_name=get_file_name(person_name,designation,company)['file_name']
        each_line=each_line.strip('\r\n')
        try:content=str(each_line)+'\t'+str(file_name)+'\n'
        except:content=each_line+'\t'+file_name+'\n'
        # try:print 'generated file name :',file_name
        # except:print 'generated file name :',file_name.encode('utf-8')
        sys.stdout.write('count:'+str(count)+' \r')
        write_into_file(file_name='total_generated_names_18kfiles.txt',content=content)
        full_file_path=os.path.join(collected_path,file_name)
        if path.exists(full_file_path):continue
        try:
            with open(full_file_path,'w') as fp:
                pass
        except Exception as e:
            print 'Exception in file creation ',file_name,e
            pass
    print 'processed count',count
        
        
    
# Aaron_Arredondo_VP_of_Sales_-_Neal_Analytics_LLC
# Aaron_Barnes_Channel_Account_Manager_-_AppRiver
# Aaron_Bernstein_Chief_Idea_Guy_-_Simple_Concepts
# Aaron_Bratrude_Bratrude_Partner_Development_Manager_-_Microsoft_Surface
# Aaron_Cao_Partner_Marketing_Advisor_-_Microsoft
