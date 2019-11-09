"""
Functionality : Check Queue count 
Version : v1.2
History :
          v1.1 - 12/24/2018 - initial version 
          v1.2 - 01/07/2018 - function delete_queue() is added 
"""
import os,time,datetime,copy
from azure.storage.queue import QueueService
from SQLConnection import * 
import datetime
from CustomEmail import *
class CheckQueue(object):
    def __init__(self,account_name='fiindmllabs',account_key='odsS8z/XCVaE+ccTHaaLULfvHfnDS/3tNmd/Otf99CFR7P5ckqEeFKzxPE08p5auBNQZ04GZ7vC1jxY2QCc6IQ==',queue_name='',send_mail_to_list=[],minimum_run_count=10,developer_mode=False):
        self.account_name=account_name
        self.account_key=account_key
        self.queue_name=queue_name
        self.last_time_stamp_file='q_last_time_stamp__'
        self.queue_history_file='q_history__'
        self.html_output_file='q_length_data.html'
        self.send_mail_to_list=send_mail_to_list
        self.minimum_run_count = minimum_run_count
        self.output_table=[]
        try:
            self.queue_service = QueueService(account_name=self.account_name,account_key=self.account_key)
        except Exception as e:
            print 'Exception in creating Queue service ',e
    def __del__(object):       
        print 'CheckQueue object deleted !!'
    def delete_queue(self,queuename):
        #queue_service = QueueService(account_name=self.account_name,account_key=self.account_key)
        try:
            self.queue_service.delete_queue(queuename)
            status=True
        except Exception as e:
            print 'Error in deleting Queue :',queuename
            print 'Exception raised :',e
            status=False
        return status
    def get_queue_length(self,queue_name=''):
        if queue_name:
            self.queue_name=queue_name
        if not self.queue_name:
            print '**Queue name should be specified !!**'
            exit()
        try:
            #print 'queue name :',self.queue_name
            #queue_service = QueueService(account_name=self.account_name,account_key=self.account_key)
            metadata = self.queue_service.get_queue_metadata(self.queue_name)
            #print 'metadata :',metadata
            try:
                message_count = metadata.approximate_message_count
            except :
                message_count = metadata['x-ms-approximate-messages-count']
            #print 'message_count:',message_count
            return message_count
        except Exception as e:
            print('Error in CheckQueue:' + str(e))
            return -1
    def run(self):
        q_length=self.get_queue_length()
        print('Number of record in queue(' + self.queue_name +') is ' + str(q_length))
        self.add_to_queue_history(q_length)
        q_history=self.get_queue_history()
        q_count_msg='NoQueue'
        q_count_status = -3
        send_mail_flag=False
        if q_history and len(q_history) > 2:
            if int(q_history[1][2]) == 0:
                q_count_msg = 'Empty'
                q_count_status = int(q_history[1][2])
                if int(q_history[2][2]) >0:
                    send_mail_flag = True
            else:
                q_count_status = int(q_history[2][2]) - int(q_history[1][2])
                if q_count_status == 0:
                    q_count_msg = 'NoChange'
                    q_count_status=int(q_history[1][2])
                    send_mail_flag = True
                elif q_count_status < 0:
                    q_count_msg = 'Increase'
                    q_count_status = abs(q_count_status)
                    if int(q_history[2][2]) == 0:
                        send_mail_flag = True
                else:
                    if q_count_status <= self.minimum_run_count:
                        send_mail_flag = True
                    q_count_msg = 'Decrease'
        elif q_history and len(q_history) == 2:
            q_count_msg = 'Started'
            q_count_status = int(q_history[1][2])
            send_mail_flag = True
        elif q_history:
            q_count_msg = 'NoData'
            q_count_status = -2
        self.add_to_output(self.get_table_html('Q Status',[['Q Status','Q Count'],[q_count_msg,q_count_status]]))
        self.add_to_output(self.get_table_html('Queue History',q_history))
        self.save_default_html()
        if send_mail_flag:
            self.send_mail()
        return True
    def get_table_html(self, table_subject, table_data_list):
        html_table_string=''
        if table_data_list:
            header_length=len(table_data_list[0])
            ### Write Table Heading Name 
            html_table_string = '<table border="2" cellspacing="1" cellpadding="3"> <tr> <td align="center" colspan="' + str(header_length) + '"> ' + table_subject + '</td></tr>'
            ### Write Column Name in <th> tag
            html_table_string += '<tr>'
            html_table_string += ''.join(['<th align="center" style="padding:1px 4px" bgcolor="palegreen">' + '<b><i>' + str(each_cell) + '</i></b>' + '</th>' for each_cell in table_data_list[0]])
            html_table_string += '</tr>'
            ### Write Data through record Iteration
            for each_record in table_data_list[1:]:
                current_record_string = '<tr>'
                current_record_string = current_record_string + ''.join(['<td align="right" style="padding:1px 4px">' + str(each_cell) + '</td>' for each_cell in each_record])  
                current_record_string += '</tr>' 
                html_table_string+= current_record_string
            html_table_string += '</td></tr></table>' + '<div style="width:100%;height:10px;background-color:#FFFFFF"></div>'
        else:
            html_table_string = '<table border="2" cellspacing="1" cellpadding="3"> <tr> <td align="center" colspan="1"> ' + table_subject + '</td></tr> <tr> <td> No data found </td></tr></table>'
        return html_table_string
    def add_to_output(self,table_string):
        if table_string and len(table_string)>8:
            self.output_table.append(table_string)
            return True
        return False
    ### It send the report to given mail address
    def frame_html(self):
        html_string='<html><body>'
        if self.output_table:
            for each_table in self.output_table:
                html_string = html_string + '<div class="tbl">' + each_table + '</div>'
        else:
            html_string = html_string + '<div class="tbl">' + '<table> <tr><td>No data to show</td></tr></table>' + '</div>'
        html_string = html_string + '</body></html>'
        return html_string
    def save_html(self,html_string):
        w=open(self.html_output_file,'w')
        w.write(html_string)
        w.close()
    def save_default_html(self):
        w=open(self.html_output_file,'w')
        w.write(self.frame_html())
        w.close()
    def clear_queue_history(self):
        w=open(self.queue_history_file,'w')
        w.close()
    def is_new_queue(self):
        if not os.path.isfile(self.queue_history_file):
            return True
        r=open(self.queue_history_file,'r')
        output_data=[]
        for each_line in r:
            each_line=each_line.strip('\n ')
            if each_line.startswith(self.queue_name):
                r.close()
                return False
            else:
                r.close()
                return True
        return True
    def add_to_queue_history(self,queue_count):
        if self.is_new_queue(): self.clear_queue_history()
        w=open(self.queue_history_file,'a')
        w.write(self.queue_name + '\t' + datetime.datetime.now().strftime('%Y%m%d %H:%M:%S') + '\t' + str(queue_count) + '\n')
        w.close()
    def get_queue_history(self):
        if not os.path.isfile(self.queue_history_file):
            return []
        r=open(self.queue_history_file,'r')
        output_data=[]
        for each_line in r:
            each_line=each_line.strip('\n ')
            output_data.insert(0,each_line.split('\t'))
        r.close()
        output_data.insert(0,['Queue Name','TimeStamp','Queue Length'])
        return copy.deepcopy(output_data)
    def send_mail(self):
        if (not self.send_mail_to_list) or len(self.send_mail_to_list) == 0:
            print('No send address is provided. Maill will not be sent')
            return 'No Mail Sent'
        rf=open(self.html_output_file,'r')
        file_content=rf.read()
        rf.close()
        try:
            mail_subject='Queue Status:' + self.account_name + ':' + self.queue_name
            send_custom_mail(self.send_mail_to_list,mail_subject,{'query_table':{'type':'html','content':file_content}})
            self.touch_timestamp()
        except Exception as e:
            return 'Mail Sent failed. Error:' + str(e)
        return 'Mail Sent'
    def touch_timestamp(self):
        o=open(self.last_time_stamp_file,'w')
        o.write(str(time.time()))
        o.close()
    def get_timestamp(self):
        if not os.path.exists(self.last_time_stamp_file): return -1
        o=open(self.last_time_stamp_file,'r')
        ct=float(o.read().strip('\r\n '))
        o.close()
        return ct
    def seconds_since_last_mail(self):
        lt=self.get_timestamp()
        if lt <= 0:
            return -1
        else:
            return float(time.time()) - lt
    def get_queue_list(self,limit=5):
        queues = list(self.queue_service.list_queues())
        #print 'queues :',queues
        name_list=[each_q.name for each_q in queues]
        return name_list
    def check_and_update_count(self,queue_name,table_name='queue_status',schema='core_stage'):
         check_query="select count(*) from "+str(schema)+"."+str(table_name)+" where queue_name='"+str(queue_name)+"'"
         print 'check_query :',check_query
         results=execute_query(check_query)
         #print results['records'][0][0]
         #print 'rowcount :',results['row_count']
         # print 'results :',results
         # print 'results[0] :',results[0]
         # print 'results[0][0] :',results[0][0]
         try:
            presence_count=int(results['records'][0][0])
         except:
            presence_count=int(results[0][0])
         print 'presence_count:',presence_count
         #raw_input('raw')
         current_queue_count=self.get_queue_length(queue_name)
         if current_queue_count<=0: return False
         if presence_count==0:
            print 'current_queue_count :',queue_name,current_queue_count
            insert_key={'queue_name':queue_name,'initial_count':current_queue_count,'current_count':current_queue_count,'azure_account_name':self.account_name}
            insert_command=get_insert_command(insert_key,table_name=table_name,table_schema=schema)
            insert_results=execute_query(insert_command)
            print 'inserted !'
         elif presence_count==1:
            values={'current_count':current_queue_count}
            conditions={'queue_name':queue_name}
            #get_update_command(values=values,conditions=conditions)
            update_results=execute_query(get_update_command(values=values,conditions=conditions,table_name=table_name,schema=schema))
            print 'updated'
    def get_queue_expiration_time(self,queue_name):
        ExpirationTime
if __name__ == '__main__':
    if True:
        queue_list=['hgnewdomainsset1']#,'hgusset1'
        receivers=['ajith@fiind.com']
        for each_queue in queue_list:
            obj=CheckQueue(queue_name=each_queue,account_name='fiindmllabs',account_key='odsS8z/XCVaE+ccTHaaLULfvHfnDS/3tNmd/Otf99CFR7P5ckqEeFKzxPE08p5auBNQZ04GZ7vC1jxY2QCc6IQ==',send_mail_to_list=receivers)
            obj.run()   
    if not True:
        queue_name='basichome92k'
        obj=CheckQueue()
        print obj.get_queue_length(queue_name)
    if not True:
        obj=CheckQueue()
        total_queue_list=obj.get_queue_list(limit=10)
        print len(total_queue_list)
        for i in total_queue_list:
            print i
    if not True:
      queue_name='techmissing4k'
      #queue_name='testing_queue'
      time_limit_minutes=5
      obj=CheckQueue()
      print 'queue_name :',queue_name
      print 'periodic check timings minutes :',time_limit_minutes
      while True:
          try:
            print obj.check_and_update_count(queue_name=queue_name)
          except Exception as e :
            print 'Exception in getting/updating  queue count ',e
            break
          print datetime.datetime.now(),'waiting for ',time_limit_minutes,' minutes '
          time.sleep(int(time_limit_minutes*60))          
          
            