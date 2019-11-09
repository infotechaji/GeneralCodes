"""
    Description: This python file has functionalities to update the data in modelling tables and move the data from unicode to core_ui
    Version    : v1.1
    History    :
                 v1.0 - 23/05/2018 - Initial Version
                 v1.1 - 13/04/2019 - option "mod_table_schema" is added to change the schema for modelling tables 
    Pending :
             1.Cyber security signals ,qna and health indicators 

"""

import luigi
import time,os
from luigi.contrib.external_program import ExternalProgramTask
# import pymssql
import pyodbc
from StatusMail import *
#from Utilities import *
import datetime
import re
#Database Connection String
DB_HOST="xxx.db.windows.net"
DB_USERNAME="username"
DB_DATABASE="database"
DB_PASSWORD="pwd"
DEVELOPER_MODE=True
DB_PORT = 1433

class UpdateSignals(luigi.Task):
    tablesuffix=luigi.Parameter(default='')
    mod_tablesuffix=luigi.Parameter(default='')
    receivers=luigi.Parameter(default='')
    send_mail=luigi.BoolParameter(default=False)
    signals_to_update=luigi.Parameter(default='all')
    project_title=luigi.Parameter(default='')
    mod_table_schema=luigi.Parameter(default='core_ui')
    data_table_schema=luigi.Parameter(default='core_temp')
    signal_file_map={'regular_report':'Regular_report.sql','weekly_report':'weekly_report.sql'}
                     
    session_id=luigi.Parameter(default='SMBJuneRef')
    def requires(self):
        print ('Process Started')
        return None
    def output(self):
        if DEVELOPER_MODE: print ('UpdateSignals output started')
        return luigi.LocalTarget('UpdateSignals.txt')
    def run(self):
        # connection = pymssql.connect(user=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT, database=DB_DATABASE)
        connection = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+DB_HOST+';DATABASE='+DB_DATABASE+';UID='+DB_USERNAME+';PWD='+DB_PASSWORD)
        cursor = connection.cursor()
        print (cursor)
        print 'mod_tablesuffix',self.mod_tablesuffix
        if not self.project_title:
            self.on_failure('Project title is not specified, quitting the process')
            exit()
        signals_to_update_split=[]
        if ',' in self.signals_to_update:
            signals=self.signals_to_update.split(',')
            signals_to_update_split=signals
        elif ',' not in self.signals_to_update and self.signals_to_update!='all':
            signals_to_update_split.append(self.signals_to_update)
        elif ',' not in self.signals_to_update and self.signals_to_update=='all':
            signals_to_update_split=self.signal_file_map.keys()
            
            signals_to_update_split.pop(signals_to_update_split.index('blend'))
            signals_to_update_split.append('blend')
            signals_to_update_split.pop(signals_to_update_split.index('modl'))
            signals_to_update_split.append('modl')
        for signals in signals_to_update_split:
            # sql_file=open('SignalQueries.sql','r')
            if signals not in self.signal_file_map or (signals in self.signal_file_map and not os.path.exists(self.signal_file_map[signals])): continue
            sql_file=open(self.signal_file_map[signals],'r')
            fopen = open('queries_triggered_error.txt','a')
            for each_line in sql_file:
                if len(each_line)<=5 or 'modelling_signals_stats' in each_line: continue
                # if len(each_line)<=5: continue
                query_statement=each_line.strip('\n \t')
                if '<table_suffix>' in query_statement:
                    query_statement=query_statement.replace('<table_suffix>',self.tablesuffix)
                if '<mod_table_suffix>' in query_statement:
                    query_statement=query_statement.replace('<mod_table_suffix>',self.mod_tablesuffix)
                if ('unicode.post_feed' in query_statement or 'unicode.company_attributes' in query_statement or 'unicode.company_info' in query_statement or 'unicode.company_technology_data' in query_statement or 'unicode.company_reference_links' in query_statement or 'unicode.company_location_details' in query_statement or 'unicode.job_info' in query_statement or 'unicode.hiring_pages_classified' in query_statement or 'unicode.jobs_classification' in query_statement or 'unicode.company_technology_classification' in query_statement or 'unicode.job_classification_pre_calculation' in query_statement or 'unicode.news_classification' in query_statement):
                    query_statement=query_statement.replace('unicode',self.data_table_schema)
                if self.mod_table_schema!='core_ui':
                    print 'Modelling table name schema changed to :',self.mod_table_schema
                    query_statement=query_statement.replace('core_ui',self.mod_table_schema)
                    
                print ('query_statement(100 chars):' + query_statement[:100])
                
                try:
                    attribute_name_final=''
                    if 'set' in query_statement.lower():
                        query_statement_split=query_statement.lower().split()
                        set_index=query_statement_split.index('set')
                        attribute_name=query_statement_split[set_index+1]
                        attribute_name_list=[]
                        for each_char in attribute_name:
                            if '=' == each_char:
                                break
                            else:
                                attribute_name_list.append(each_char)
                                
                        attribute_name_final=''.join(attribute_name_list)
                    print 'Updating Attribute',attribute_name_final
                    
                    with open('queries_triggered.sql','a') as target:
                        target.write(query_statement+'\n')
                    
                    # raw_input()
                    cursor.execute("INSERT INTO core_ui.modelling_signals_stats(attribute_name, attribute_type, task_status) select '"+attribute_name_final+"','"+signals+"','Started'")
                    st=datetime.datetime.now()
                    cursor.execute(query_statement)
                    rows_affected=cursor.rowcount
                    timetk=datetime.datetime.now()-st
                    #query_statement
                    with open('row_affected.sql','a') as target:
                        final_text=str(str(datetime.datetime.now()).split('.')[0])+'\t'+str(attribute_name_final)+"\t"+str(rows_affected)+'\t'
                        final_text+=str(str(query_statement))
                        final_text+='\n'
                        target.write(final_text)
                    print (rows_affected,'rows affected','TimeTaken',str(timetk))
                    cursor.execute("INSERT INTO core_ui.modelling_signals_stats(attribute_name, attribute_type, task_status, affected_rows,project_title) select '"+attribute_name_final+"','"+signals+"','Completed',"+str(rows_affected)+",'"+str(self.project_title)+"'")
                    connection.commit()
                except Exception as e:
                    error_norm=re.sub(r'[^a-zA-Z0-9 ]','',str(e))                    
                    error_sql="INSERT INTO core_ui.modelling_signals_stats(attribute_name, attribute_type, task_status, comments,project_title) select '"+attribute_name_final+"','"+signals+"','Error','"+error_norm+"','"+str(self.project_title)+"'"
                    # print error_sql
                    # raw_input()
                    cursor.execute(error_sql)
                    fopen.write(query_statement+'\t'+str(e)+'\n')
                    self.on_failure(e)
            sql_file.close()            
        cursor.execute("SELECT TOP 1 attribute_name, task_status, signal_id from core_ui.modelling_signals_stats ORDER BY time_stamp desc")
        data = cursor.fetchone()
        if data:
            if data[0] == 'cloud_presence' and data[1] == 'Completed':
                self.output().open('w').close()
        else:
            self.output().open('w').close()            
        connection.commit()
        connection.close()
        #fopen.close()
    def on_success(self):
        print ('Modelling Signals Update : On success ')
        if self.send_mail : send_status_email(task=UpdateSignals(),receivers=self.receivers,success=True,test_mail=True)
    def on_failure(self,exception):
        print ('Modelling Signals Update : Failure ') 
        print ('Exception in Modelling Signals Update :',exception)
        if self.send_mail : send_status_email(task=UpdateSignals(),receivers=self.receivers,success=False,test_mail=True,exception=exception)

class UnicodeToCoreUi(luigi.Task):
    tablesuffix=luigi.Parameter(default='')
    receivers=luigi.Parameter(default='')
    project=luigi.Parameter()
    logfile=luigi.Parameter(default='log_queries.txt')
    send_mail=luigi.BoolParameter(default=False)
    def requires(self):
        print ('Process Started')
        return None
    def output(self):
        if DEVELOPER_MODE: print ('unicode to core_ui output started')
        return luigi.LocalTarget('UnicodeCoreUi.txt')
    def run(self):
        connection = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+DB_HOST+';DATABASE='+DB_DATABASE+';UID='+DB_USERNAME+';PWD='+DB_PASSWORD)
        # connection = pymssql.connect(user=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT, database=DB_DATABASE)
        cursor = connection.cursor()
        #print (cursor)
        status_insert="INSERT INTO core_ui.unicode_core_ui_stats(attribute_name, task_status,project) select '<attribute_name>','Started','<project>'"
        #status_update="UPDATE core_ui.unicode_core_ui_stats set task_status ='<task_status>' where project ='<project>' and attribute_name ='<attribute_name>'"
        status_update="UPDATE core_ui.unicode_core_ui_stats set <update_key_value> where project ='<project>' and attribute_name ='<attribute_name>'"
        status_select="SELECT task_status from core_ui.unicode_core_ui_stats where project ='<project>' and attribute_name ='<attribute_name>'"
        sql_file=open('unicode_core_ui.sql','r').readlines()
        print ('table suffix :',self.tablesuffix)
        print ('Total Queries:',len(sql_file))
        q_count=0
        for each_query in sql_file:
            q_count+=1
            res= re.search('core_ui.\w+',each_query,re.I)
            if res:
                attribute_name=res.group(0)
            if attribute_name:
                print q_count,attribute_name
                temp_q=status_select.replace('<project>',str(self.project)).replace('<attribute_name>',str(attribute_name))
                print ("temp_q",temp_q)
                cursor.execute(temp_q)
                data = cursor.fetchone()
                rows_check=cursor.rowcount
                #print ('first check status data:',data)
                if data: print 'data length :',len(data)
                else: data=[]
                #print ('rows_affected:',rows_check)
                #raw_input('query over')
                if len(data)==0: # not yet started
                    print ('first if case len(data)==0 :')
                    temp_insert_q=status_insert.replace('<project>',str(self.project)).replace('<attribute_name>',str(attribute_name))
                    print ('Status Insert :',temp_insert_q)
                    cursor.execute(temp_insert_q)
                    cursor.commit()
                    print 'insert affected rows :'+str(cursor.rowcount)
                    print (attribute_name,'Status :','Started')
                    try:
                        cursor.execute(each_query.replace('<table_suffix>',str(self.tablesuffix)))
                        temp_update1=status_update.replace('<project>',str(self.project)).replace('<attribute_name>',str(attribute_name))
                        temp_update1=temp_update1.replace('<update_key_value>','task_status = \'Completed\' , rows_affected ='+str(cursor.rowcount))
                        print 'temp update query1 :',temp_update1
                        cursor.execute(temp_update1)
                        cursor.commit()
                        print attribute_name,'Status :','Completed'
                    except Exception as e:
                        print 'error msg :',e
                        error_msg=str(e).replace("\'","\\''").replace('\"','\\"')
                        print 'error msg after changing :',error_msg
                        error_update1=status_update.replace('<project>',str(self.project)).replace('<attribute_name>',str(attribute_name))
                        error_update1=error_update1.replace('<update_key_value>','task_status =\'Error\',comments =\''+str(error_msg)+'\'')
                        print 'Error query1 :',error_update1
                        cursor.execute(error_update1)
                        print (attribute_name,'Status :','Error',e)
                        cursor.commit()
                elif len(data)==1:
                    print ('Case 2 : len(data)==1')
                    status_from_db=str(data[0]).strip(' u\' \'')
                    #print 'status_from_db:',status_from_db
                    if  status_from_db.lower()=='completed':
                        print attribute_name,'Status:Skipped (previously completed) :'
                        continue
                    elif status_from_db.lower()=='error':
                        print (attribute_name,'Error')
                        try:
                            cursor.execute(each_query.replace('<table_suffix>',str(self.tablesuffix)))
                            temp_update2=status_update.replace('<project>',str(self.project)).replace('<attribute_name>',str(attribute_name))
                            temp_update2=temp_update2.replace('<update_key_value>','task_status = \'Completed\' , rows_affected ='+str(cursor.rowcount))
                            print 'temp update query2 :',temp_update2
                            cursor.execute(temp_update2)
                            cursor.commit()
                        except Exception as e:
                            error_msg=e
                            error_update2=status_update.replace('<project>',str(self.project)).replace('<attribute_name>',str(attribute_name))
                            error_update2=error_update2.replace('<update_key_value>','task_status =\'Error\',comments =\''+str(e)+'\'')
                            print 'Error query2:',error_update2
                            cursor.execute(error_update2)
                            cursor.commit()
                            print ('Exception in Moving data :',e)
                connection.commit()
        connection.close()
    def on_success(self):
        print ('Unicode To CoreUi : On success ')
        if self.send_mail : send_status_email(task=UnicodeToCoreUi(),receivers=self.receivers,success=True,test_mail=True)
    def on_failure(self,exception):
        print ('Unicode To CoreUi Failure ') 
        print ('Exception in Unicode To CoreUi :',exception)
        if self.send_mail : send_status_email(task=UnicodeToCoreUi(),receivers=self.receivers,success=False,test_mail=True,exception=exception)
if __name__ == '__main__':
    luigi.run()
    
    #python ModellingSignalsAutomation.py --scheduler-host localhost UnicodeToCoreUi  --tablesuffix _non_profit --send-mail --receivers kema@fiind.com --mod_tablesuffix