"""
Functionality : Script which send and /replies receives GMail 
Version    : v1.1
History    : 
                v1.0 - 02/20/2019  - initial version
                v1.1 - 04/23/2019  - receivers option is added 
Pending    :
Open issues   :
"""

import smtplib
import time
import imaplib
import email 
import re
import datetime
import os
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
#from DeleteFilesSupport import * 


class Gmail():
    def __init__(self,sender="fiindinsights@gmail.com",password='$11nd@dmin',developer_mode=True):
        self.sender=sender
        self.password=password
        self.developer_mode=developer_mode
        if 'gmail' in self.sender:
            self.server = "imap.gmail.com"
            self.port   = 993
    def __del__(self):
        print ("Gmail : object deleted")
    def send_mail(self,input_dict,receivers):
        msg = MIMEMultipart() 
        msg['From'] = self.sender
        if type(receivers)==list:
            msg['To'] = ','.join(receivers)
        elif type(receivers)==str:
            msg['To'] =receivers.strip(', \n\t')
        msg['Subject'] = input_dict['subject']
        body = "<p>"+input_dict['body']['greetings']+"</p>\n<br>"
        body += "<p>"+input_dict['body']['content']+"</p>\n<br>"
        try:
            if input_dict['body']['table_input']:
                headers=input_dict['body']['table_input']['headers']
                table_content_list=input_dict['body']['table_input']['table_content']
                #body += "<table align=\"left\" bgcolor='wheat' border=1 cell_spacing='2.0' >\n"
                body +='<table border="2" cellspacing="1" cellpadding="3">'
                body += "\n".join(['<tr><th align="center" style="padding:1px 4px" bgcolor="palegreen">{}</th></b><th align="center" style="padding:1px 4px" bgcolor="palegreen"><b>{}</th></b></tr>'.format(key.capitalize(),value.capitalize()) for key,value in headers.items()])
                for table_dict in table_content_list:
                    body += "\n".join(['<tr><td  align="left" style="padding:1px 4px" >{}</td><td  align="right" style="padding:1px 4px">{}</td></tr>'.format(key.capitalize(),value) for key,value in table_dict.items()])
                body += "\n</table><br><br><br>\n"
        except Exception as e:
            print 'Exception in getting table content :',e
        try:
            if input_dict['body']['bottom_content']:
                body += "<p>"+input_dict['body']['bottom_content']+"</p>\n<br>"
        except Exception as e:
            print 'Exception in getting bottom content :',e
        # attach the body with the msg instance 
        #msg.attach(MIMEText(body, 'plain')) 
        msg.attach(MIMEText(body, 'html')) 
        try:
            if input_dict['attachment']:
                for each_dict in input_dict['attachment']: # dictionaries of list 
                    #print 'each_dict:',each_dict
                    filename = each_dict['file_name']
                    full_file_path = each_dict['full_file_path']
                    if len(open(full_file_path).readlines())<2:
                        print 'Attachment Skipped , Not having data ',full_file_path
                        continue
                    attachment = open(full_file_path, "rb") 
                    p = MIMEBase('application', 'octet-stream') 
                    p.set_payload((attachment).read()) 
                    encoders.encode_base64(p) 
                    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
                    msg.attach(p) 
        except Exception as e : print 'Exception in attachment  :',e
        try:
            s = smtplib.SMTP('smtp.gmail.com', 587) 
            s.starttls()
            s.login(self.sender,self.password) 
            print 'Login Success '
            text = msg.as_string() 
            s.sendmail(self.sender,receivers, text) 
            print 'Mail sent'
            #s.quit()
            #s.close()
        except Exception as e:
            print 'Exception in sending Mail : ',e
            return False
        return True
    def wait_for_reply(input_dict,time_out_minutes=1,receivers=[],check_count=10):
        print 'waiting for reply...'
        print 'Time out minutes:',time_out_minutes
        time.sleep(int(time_out_minutes*60))
        subject=input_dict['subject']
        sensitive_data=input_dict['sensitive_data']
        return read_email_from_gmail(sensitive_data=sensitive_data,subject=subject,receivers=receivers,check_count=check_count)
        
    def read_email_from_gmail(self,subject='',sensitive_data='yes',check_count=50,receivers=[]):
        # try:
        if True:
            print 'read from mail starts........'
            mail = imaplib.IMAP4_SSL(self.server)
            print 'server connected !!'
            mail.login(self.sender,self.password)
            print "Reading mails..."
            current_count=0
            #while current_count<=check_count: # to read the latest mail
                #mail.select('inbox')
            mail.select('inbox')
            type, data = mail.search(None, 'ALL')
            mail_ids = data[0]
            id_list = mail_ids.split()   
            first_email_id = int(id_list[0])
            latest_email_id = int(id_list[-1])
            for current_mail in range(latest_email_id,latest_email_id-check_count, -1):
                typ, data = mail.fetch(current_mail, '(RFC822)')
                #print 'Time : ',datetime.datetime.now(),'latest_email_id :',latest_email_id
                print 'Total Mails :',len(id_list)
                print 'latest_email_id :',latest_email_id
                #print 'latest_email_id :',id_list[-2]
                for response_part in data:
                    print 'response_part :',response_part
                    if isinstance(response_part, tuple):
                        msg = email.message_from_string(response_part[1])
                        email_subject = msg['subject']
                        email_from = msg['from']
                        #message_body=msg.get_payload()
                        #message_body=msg['body']
                        if msg.is_multipart():
                            for part in msg.walk():
                                ctype = part.get_content_type()
                                cdispo = str(part.get('Content-Disposition'))
                                    # skip any text/plain (txt) attachments
                                if ctype == 'text/plain' and 'attachment' not in cdispo:
                                    body = part.get_payload(decode=True)  # decode
                                    break
                        # not multipart - i.e. plain text, no attachments, keeping fingers crossed
                        else:
                            body = msg.get_payload(decode=True)
                        #print 'body :',body
                        response_from_body=(body.lower()).split('from:')[0]
                        print 'response_from_body :',response_from_body
                        try:
                            #mail_id_temp=re.search(r'<\w.*>',email_from)#.group()[0]
                            #mail_id=mail_id.group(0)
                            mail_id = ((re.findall('\S+@\S+',email_from))[0]).strip('<>')
                            print 'try from_id:',mail_id
                            print 'extracted Mail ID :',mail_id
                            #print 'mail_id.group(0) :',mail_id.group(0)
                            #print 'mail_id.group(1) :',mail_id.group(1)
                        except:
                            mail_id=email_from
                            print 'exception in getting  Mail ID , hence :',mail_id
                            #print 'message_body:',message_body
                            pass
                        raw_input('Message body')
                        status = [True for each_mail in receivers if mail_id in each_mail.lower()]
                        print 'Mail ID Match !!',status
                        if status and subject.lower() in email_subject.lower() and sensitive_data.lower() in response_from_body:
                            print 'Subject also matched '
                            
                            return True
        return False

if __name__=="__main__":
    gm_obj=Gmail()
    #gm_obj.read_email_from_gmail()
    receivers='ajith@fiind.com'
    input_dict={}
    input_dict['subject']='Testing Mail Please Ignore !!'
    input_dict['body']={
                        'greetings':'Hi All ,',
                        'content':'Testing content please check out this mail .',
                        'bottom_content':'',
                        'table_input':{
                                        'headers':{'Title':'Value'},
                                        'table_content':[
                                                        {'key1':'value1'},
                                                        {'key2':'value2'}
                                                        
                                                        ]
                                        }
                        }
    input_dict['attachment']=[]
    # {'file_name':'Dummy_textFile.txt',
                                # 'full_file_path':'D:\\Ajith\\_code\\GeneralCodes\\Mail\\Dummy_textFile.txt'}
    
    subject='Periodic Memory Check done in the Machine "Ajith-Local" on 25_02_2019'
    receivers=['ajith@fiind.com']
    gm_obj.send_mail(input_dict=input_dict,receivers=receivers)
    #gm_obj.read_email_from_gmail(subject,receivers)