"""
Functionality : Script whics execute sql queries 
Version : v1.3
History :
          v1.0  - 02/27/2019 - initial version 
          v1.1  - 02/28/2019 - get select command added 
          v1.2  - 03/13/2019 - option "what_to_select" is added to get_select_command()
          v1.3  - 03/13/2019 - input option is changed from list to dict "get_insert_command()"
Pending :
Open issues :
"""
import pymssql
import argparse
import pyodbc 
import time,datetime

DB_HOST="xxx.xxxx.windows.net"
DB_DATABASE="xxxx"
DB_USERNAME="xxxx"
DB_PASSWORD="Password"
PORT=1433

def execute_query(SQLCommand,fetch_all=True,connection_type='pyodbc'):
    
    user_name_temp=DB_USERNAME+'@'+str(DB_HOST).split('.')[0]
    
    #user_name_temp=DB_USERNAME+'@'+DB_HOST
    #print 'user_name_temp:',user_name_temp
    try:
        if connection_type=='pymssql':
            conn = pymssql.connect(server=DB_HOST,port=PORT,user=user_name_temp,password=DB_PASSWORD,database=DB_DATABASE,as_dict=True)
        elif connection_type=='pyodbc':
            #conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+DB_HOST+';DATABASE='+DB_DATABASE+';UID='+user_name_temp+';PWD='+ DB_PASSWORD+';Trusted_Connection=yes;')
            conn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+DB_HOST+';DATABASE='+DB_DATABASE+';UID='+user_name_temp+';PWD='+ DB_PASSWORD+';as_dict=True')#+';Trusted_Connection=yes;'
        cursor = conn.cursor()
        connection_status=True
        #print 'Connection Succeed !!'
        result_status=cursor.execute(SQLCommand)
        #print 'result_status :',result_status
        if (SQLCommand.lower()).startswith('insert') or (SQLCommand.lower()).startswith('update'):
            conn.commit()
            print 'Connection commited '
        if fetch_all:
            row = cursor.fetchall()
        else:
            row = cursor.fetchone()
        comments =len(row)
        query_status='Success'
        conn.close()
        return row
    except Exception as e:
        print 'Exception while executing the query :',e
        comments=str(e)
        query_status='Success(select & Insert statements)'
        if len(str(e))>=65:
            print 'Code will be executed , Skipping monitor  '
            query_status='Errored'
            return False
        pass
         
    with open('Queries_Log.txt','a') as w:
        w.write(str(get_printable_time_stamp())+'\t'+str(SQLCommand)+'\t'+str(query_status)+'\t'+str(comments)+'\n')
    return False
def getNormlaisedDict(input_dict,separator=','):
    combined_statement=''
    for each_key in input_dict:
        combined_statement+=" "+str(each_key)+"='"+str(input_dict[each_key])+"' "
        combined_statement+=separator
    combined_statement=combined_statement.strip(' ')
    combined_statement=combined_statement.strip(separator)
    print 'combined_statement :',combined_statement
    return combined_statement

def get_update_command(values={},conditions={},table_name="code_execution_status",schema='core_stage'):
    set_values=getNormlaisedDict(values,separator=',')
    where_conditions=getNormlaisedDict(conditions,separator='and')
    update_command="Update A set "
    update_command+=str(set_values)
    update_command+=" from "+str(schema)+'.'+str(table_name)+" A"
    update_command+=" where  "+str(where_conditions)
    print 'update_command :',update_command
    return update_command

def get_insert_command(each_dict,table_name='code_execution_status',table_schema='core_stage'):
    key_text=''
    value_text=''
    for each_key in each_dict:
        key_text+=str(each_key)+','
        value_text+="'"+str(each_dict[each_key])+"'"+','
    key_text=key_text.strip(',')
    value_text=value_text.strip(',')
    SQLCommand ="INSERT INTO "+table_schema+"."+table_name+"("
    SQLCommand +=key_text
    SQLCommand +=") VALUES ("
    SQLCommand +=value_text
    SQLCommand +=")"
    print 'SQLCommand :',SQLCommand
    return SQLCommand
def get_select_command(input_dict,schema='core_stage',table_name='code_execution_status',what_to_select='count(*)'):
    select_query="select "+str(what_to_select)+" from "+str(schema)+"."+str(table_name)+" where "
    for key in input_dict:
        select_query+=str(key)+"='"+str(input_dict[key])+"' and "
    select_query=select_query.strip('and ')
    return select_query
def get_printable_time_stamp(get_exact_time=False,skip_seconds=False):
    c_time= str(datetime.datetime.now())
    date_time=c_time.split('.')[0]
    if skip_seconds:
        date_time=date_time.split()[0]
    if get_exact_time:
        return date_time # returns 2018-05-22 12:21:22
    return get_replaced_content(date_time)

def get_replaced_content(content,characters_list=['-',':',' '],replace_by=''):
    if not content: return ''
    for each_char in characters_list:
        if each_char==' ':
            content=content.replace(each_char,'_')
        else:
            content=content.replace(each_char,replace_by)
    return content

if __name__=="__main__":
    domain_name='livevox.com'
    # inserting
    insert_command="INSERT INTO core_stage.code_execution_status(total_instances,vm_name,code,code_execution_status,total_accounts,pending_count,owner,ip_address,active_instances,queue,input_type,project,host_name,blob) VALUES ('3','ovhjob3.fiindlabs.com','tech','Running','9','9','Ajith','169.254.51.92','0','techmissing4k-test','Queue','Testing_2','ns534636','techmissing4k-test')"
    #tech_command='select * from core_stage.code_execution_status'
    #execute_query(insert_command)
    # update 
    values={'vm_name':'yummy',
            'ip_address':'jummy'}
    conditions={'project':'Testing22',
    'code':'tech'}
    #update_command=get_update_command(values=values,conditions=conditions)
    #print execute_query(update_command)
    test_command ='select top 10 * from core_stage.code_execution_status'
    #print execute_query(test_command)
    input_dict={'vm_name':'xxx.xxx.xxx','try_count':15}
    print execute_query(get_select_command(input_dict))
