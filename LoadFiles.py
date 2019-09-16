"""
Functionality : Code which normalise and load modelling output files to Tables
Version       : v1.4
History       :
                v1.0 - 12/11/2018 -p initial version 
                v1.1 - 02/13/2019 -Generalaised to load Any input file , Skip_replace option is added to the function get_modified_file()
                v1.2 - 05/05/2019 -function getBCP_command return results as a dict 
                v1.3 - 05/06/2019 -function GetRowsCopied is added to get the no of rows copied using BCP
                v1.4 - 05/09/2019 -function get_files_lines() is added for read files 
                
Pending       :
Issues        :
 
"""

import sys,os,re
import datetime

# DB_HOST="minicus.database.windows.net"
# DB_USERNAME="fiinduser"
# DB_PASSWORD="Welcome$11nd"
# DB_DATABASE="minicus_prod"

DB_HOST="ssci.database.windows.net"
DB_USERNAME="Fiinduser"
DB_PASSWORD="Welcome$11nd"
DB_DATABASE="ssci_stage_new"

DEVELOPER_MODE=True
def write_data_in_file(file_name='processed_accounts.txt',content='',mode='a'):
    with open(file_name,mode) as fp:
        if content:
            try:
                fp.write(content+'\n')
            except:
                fp.write(str(content)+'\n')
    return True
def get_files_lines(file_name,remove_empty_lines=True):
    try:
        file_lines=open(file_name).readlines()
    except Exception as e :
        print 'Error while reading output file :',e
        return '' # file not exists 
    # if remove_empty_lines:
        # new_list=[]
        # for each_line in file_lines:
            # if len(each_line.strip(' \r\n'))>0:
                # new_list.append(each_line)
        # file_lines=new_list
    return file_lines
def get_modified_file(input_filename,encode=True,remove_characters=['"'],replace_by='',delimiter='|^|',replace=False): # converts the input file 
        #file_lines=open(input_filename).readlines()
        file_lines=get_files_lines(input_filename)
        encode=True
        output_filename=input_filename.replace('.','_modified.')
        print 'Input file lines :',len(file_lines)
        if len(file_lines)<1:return {}
        try:
            if encode:
                fp=open(output_filename,'wb')
            else:
                fp=open(output_filename,'w')
            if DEVELOPER_MODE : print 'Input File :',input_filename
            if DEVELOPER_MODE : print 'Output File :',output_filename
            if DEVELOPER_MODE : print 'len(file_lines) :',len(file_lines)
            if DEVELOPER_MODE : print 'Encode status :',encode
            for each_line in file_lines:
                try:
                    if replace:
                        for each_char in remove_characters:
                            each_line=each_line.replace(each_char,replace_by)
                            each_line=each_line.replace(',',delimiter)
                    if encode:
                        each_line=encode_to_ucs2le(each_line)
                    else:each_line=each_line
                    fp.write(each_line)
                except:pass
            fp.close()
            return {'input_filename':input_filename,
                    'output_filename':output_filename,
                    'file_lines':len(file_lines),
                    'encoded':encode
                    }
        except Exception as e:
            print 'Exception in LoadFiles :\t get_modified_file():',e
            return {}

def encode_to_ucs2le(each_line):
        current_line=each_line
        if len(current_line.strip('\r\n\t'))>0:
            if '|^|' not in current_line and '\t' in current_line:
                current_line=current_line.replace('\t','|^|')
            if current_line.endswith('\r\n'):
                return current_line.decode('utf-8').encode('utf-16le')#.replace('\r\n','\n')
            elif current_line.endswith('\n'):
                current_line=current_line.replace('\n','\r\n')
                return current_line.decode('utf-8').encode('utf-16le')#.replace('\r\n','\n')
        else:
            return ''
def get_printable_time_stamp(get_exact_time=False,skip_formating=False):
    c_time= str(datetime.datetime.now())
    #print 'c_time before formatting :',c_time
    date_time=c_time.split('.')[0]
    #print 'date_time before formatting :',date_time
    if get_exact_time:
        if skip_formating: return c_time # returns 2018-05-22 12:21:22
        else : return get_replaced_content(c_time)
    return get_replaced_content(date_time)

def get_replaced_content(content,characters_list=['-',':',' ','.'],replace_by=''):
    if not content: return ''
    for each_char in characters_list:
        if each_char==' ':
            content=content.replace(each_char,'_')
        else:
            content=content.replace(each_char,replace_by)
    return content
def getBCP_command(file_name,table_name,schema_name,delimiter='|^|'):
    bcp_path='bcp_log'
    if not os.path.exists(bcp_path):
        os.makedirs(bcp_path)
    bcp_log_file='bcp_out_'+str(table_name.replace('.','_'))+'_'+str(get_printable_time_stamp(get_exact_time=True))+str('.txt')
    bcp_full_path=os.path.join(bcp_path,bcp_log_file)
    bcp_prefix='bcp '+ DB_DATABASE + '.' + schema_name + '.' + table_name + ' in ' 
    bcp_suffix=' -w -t "'+str(delimiter)+'" -S '+ DB_HOST +' -U '+ DB_USERNAME +' -P '+ DB_PASSWORD +' >>'+bcp_full_path
    command_line=bcp_prefix + ' "' + file_name + '"' + bcp_suffix + '\n'
    #return command_line
    return {'bcp_command_line':command_line,
            'bcp_log_file':bcp_full_path
            }

def LoadFile(file_name,table_name,schema_name='unicode',skip_modification=False,delimiter='|^|'):
    if skip_modification:
        output_filename=file_name
    else:
        result_dict =get_modified_file(file_name)
        #print 'result_dict :',result_dict
        output_filename=result_dict['output_filename']
    if DEVELOPER_MODE : print 'output_filename :',output_filename
    bcp_result_dict=getBCP_command(file_name=output_filename,table_name=table_name,schema_name=schema_name,delimiter=delimiter)
    bcp_command=bcp_result_dict['bcp_command_line']
    print ' BCP COMMAND:',bcp_command
    res=os.system(bcp_command.strip('\n'))
    print 'EXECUTED !!'
    write_data_in_file(file_name='bcp_log.txt',content=bcp_command)
    #print 'bcp_result_dict[bcp_log_file] :',bcp_result_dict['bcp_log_file']
    bcp_log_file=bcp_result_dict['bcp_log_file']
    rows_copied=GetRowsCopied(bcp_log_file)
    #print 'rows_copied :',rows_copied
    file_lines=len(get_files_lines(output_filename))
    if file_lines>0:
        file_lines=int(file_lines-1)
    try:
        if int(rows_copied)==int(file_lines): status ='Success'
        else: status='Count Mismatched'
    except:status='Count Mismatched'
    return {
           'input_file':file_name
           ,'modified_file_name':output_filename
           ,'bcp_command':bcp_result_dict['bcp_command_line']
           ,'bcp_log_file':bcp_result_dict['bcp_log_file']
           ,'rows_copied':rows_copied
           ,'file_lines':file_lines
           ,'table_name':table_name
           ,'schema_name':schema_name
           ,'status':status
            }
    
def GetRowsCopied(file_name):
    print 'GetRowsCopied : trying to hit',file_name
    if os.path.isfile(file_name):
        copied_rows = False
        for each_line in reversed(open (file_name).readlines()) :
            if 'rows copied.' in each_line :
                copied_rows = True
                copies = re.search( r'([0-9]+) rows copied.', each_line, re.M|re.I).group(1)
                return copies
    else : 
        print "File not present"
        return -2 # File missing 
    return -1
    
if __name__=="__main__":
    #print get_printable_time_stamp(get_exact_time=True,skip_formating=False)
    #print get_files_lines(sys.argv[1])
    if not True:
        input_filename=sys.argv[1]
        table_name='m365_scores_updated'
        schema_name='unicode'
        LoadFile(file_name=input_filename,table_name=table_name,schema_name=schema_name,delimiter='\t')
    #print get_printable_time_stamp()
    if not True:
        input_directory=sys.argv[1]
        #input_directory=os.getcwd()
        #input_directory='D:\\Ajith\\_data\\SSCI\\RefJan\\Output\\TwitterPosts'
        #input_file='_core_ui_twitter_posts2.psql'
        input_file=sys.argv[2]
        full_file_path=os.path.join(input_directory,input_file)
        table_name='post_feed'
        schema_name='unicode'
        result_dict=LoadFile(file_name=full_file_path,table_name=table_name,schema_name=schema_name)
