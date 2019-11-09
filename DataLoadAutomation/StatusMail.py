import os
import smtplib
import datetime
import json
import requests
#from email.message import EmailMessage # python 3 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SLACK_URL='https://hooks.slack.com/services/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'

def send_status_email(task,receivers='',success=True,test_mail=True,subject_prefix=None,exception=''): #task: luigi.Task
    developer_mode=False
    if developer_mode: print 'send_success_email called !!!'
    #local_smtp = 'smtp.office365.com:587'
    #default_email_address = "ajith@fiind.com"#["@".join(('ajith','fiind.com'))] # E-mail addresses are username@domain.com locally. Pick the user running it, if none provided
    default_email_address ="fiindinsights@gmail.com"
    password='Enter123'
    if not receivers:
        print 'No receivers found !'
        exit()
    elif receivers:
        receiver_list=receivers.split(',')
        print 'Number of receivers :',len(receiver_list)
	print 'Status mail receiver_list :',receiver_list	
    name_task_class = 'testing task class'#task.task_family
    if subject_prefix is None:
        subject = list()
        if test_mail:
            subject.append('Test Mail Please Ignore !')
    else:
        subject = [subject_prefix + ":"]
    if success:
        message_header="task finished successfully at"
        subject_title="ran successfully on"
    else:
        message_header="failure occured at "
        subject_title="terminated at "
    subject.extend([name_task_class,subject_title,os.environ["COMPUTERNAME"],])
    msg = MIMEMultipart()
    msg['Subject'] = " ".join(subject) # should be given in a list
    msg['From'] = default_email_address # password should be provided
    msg["To"] = receivers#",".join(receiver_list)
    msg["Cc"] = ""#"ajith@fiind.com"
    body = "<p>\n"

    body += " ".join((name_task_class,message_header, datetime.datetime.now().strftime("%H:%M:%S on %Y-%m-%d"),))
    # if developer_mode:
        # print 'task.task_id :',task.task_id
        # print "task.get_params() :",task.get_params()
        # print "task.requires() :",task.requires()
        # print "task.input() :",task.input()
        # print "task.output() : ",task.output()
    body += "\n</p>\n"
    body += "<table align=\"left\" border=1>\n"
    body += "\n".join([
        "<tr><td>{}</td><td>{}</td></tr>".format(key, value)
        for key, value in (
            ("Task ID",12345), #
            ("Task Class Name", name_task_class),
            ("Computer Name", os.environ["COMPUTERNAME"]),
            ("User Name", os.environ["USERNAME"]),
            ("Parameter(s)", 'parameter'),#task.get_params()), #
            ("Requirement(s)",'requires'),#, 'requires'task.requires()), # task.requires()
            ("Output(s)", 'output')#task.output()), #task.output()
            )
        ])
    body += "\n</table>\n"
    if exception:
        body+="\n<br><h2 align=\"left\">Exception:</h2>\n<p>"+str(exception)+"</p>"

    if developer_mode: print "body :", body
    mimepart = MIMEText(body, 'html')
    msg.attach(mimepart)
    #send_message(SLACK_URL, subject, username=None)
    send_mail(sender=default_email_address,password=password,receiver=receiver_list,msg=msg) # sends outlook mail

def send_mail(sender,password,receiver,msg): # sends email to recipent(s)
    if 'gmail.com' in sender:
        s=smtplib.SMTP('smtp.gmail.com:587')
    elif 'fiind.com' in sender:
        s = smtplib.SMTP('smtp.office365.com:587')
    print 'Port Opened and Login executing....'
    s.starttls()
    s.login(sender,password)
    print 'login successfull!!'
    # if type(receiver) is list:
        # print 'List of receivers:',receiver
        # receiver=';'.join(receiver)
    # #s.sendmail(sender, receiver, msg.as_string())
    s.sendmail(sender,msg["To"].split(",") + msg["Cc"].split(","), msg.as_string())
    s.quit()

def send_message(slack_url, max_print=5, username='Default'): # messages will be sent to slack 
    text=(' ').join(max_print)
    #text = format_message(max_print)
    print "max_print:",max_print
    print "text :",text
    if not slack_url and text:
        print("slack_url not provided. Message will not be sent")
        print(text)
        return False
    
    if text:
        payload = {"text": text}
        if username:
            payload['username'] = username
        #print ("payload :",payload)
        r = requests.post(slack_url, data=json.dumps(payload))
        if not r.status_code == 200:
            raise Exception(r.text)
    return True
if __name__=='__main__':
    send_status_email(task='',receivers='ajith@fiind.com,interns@fiind.com,m.lashmanan13@gmail.com')