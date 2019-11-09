from MasterGmail import * 
from TechProcessSupport import * 

def send_custom_mail(file_list):
    gm_obj=Gmail()
    #gm_obj.read_email_from_gmail()
    receivers='ajith@fiind.com'
    input_dict={}
    input_dict['subject']='Daily Astro Prediction on  {}!!'.format(get_printable_time_stamp(get_date_only=True))
    input_dict['body']={
                        'greetings':'Hi All ,',
                        'content':'Please check the  attachments  .',
                        'bottom_content':'',
                        'table_input':{
                                        'headers':{'Title':'Value'},
                                        'table_content':[
                                                        {'key1':'value1'}
                                                        ]
                                        }
                        }
    attachments=[]
    for each_file in file_list:
        temp_dict={'file_name':each_file,'full_file_path':os.path.join(os.getcwd(),each_file)}
        attachments.append(temp_dict)
    input_dict['attachment']=attachments
    #{'file_name':'Dummy_textFile.txt',
                                # 'full_file_path':'D:\\Ajith\\_code\\GeneralCodes\\Mail\\Dummy_textFile.txt'}
    
    receivers=['ajith@fiind.com']
    gm_obj.send_mail(input_dict=input_dict,receivers=receivers)
    #gm_obj.read_email_from_gmail(subject,receivers)
if __name__=="__main__":
    input_list=['aquarius_20190520.txt','aries_20190520.txt']
    send_custom_mail(input_list)