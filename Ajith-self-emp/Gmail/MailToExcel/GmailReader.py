# Python 3.8.0
import smtplib
import time
import imaplib
import email
import traceback 
# -------------------------------------------------
#
# Utility to read email from Gmail Using Python
#
# ------------------------------------------------
# ORG_EMAIL = "@gmail.com" 
# FROM_EMAIL = "ajithkumar0511" + ORG_EMAIL 
FROM_EMAIL = "ajithkumar@sedintechnologies.com"
FROM_PWD = "A@sedin123" 


def read_emails(username,password,no_of_mails=5,developer_mode = True):
    SMTP_SERVER = "imap.gmail.com"
    SMTP_PORT = 993
    mail = None
    result_list = []
    try:
        print ('Logging in........',end='')
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(username,password)
        print(' Success !!')
    except Exception as e:
        print ('Error while logging in :',e)
        return False
    if mail:
        try:
            mail.select('inbox')
            data = mail.search(None, 'ALL')
            mail_ids = data[1]
            id_list = mail_ids[0].split()
            total_emails = len(id_list)
            if developer_mode :
                print('Total Emails:',total_emails)
            first_email_id = int(id_list[0])
            latest_email_id = int(id_list[-1])

            if no_of_mails< total_emails:
                first_email_id = latest_email_id-no_of_mails
            if developer_mode:
                print('first_email_id:', first_email_id)
                print('latest_email_id:', latest_email_id)
            for i in range(latest_email_id, first_email_id, -1):
                data = mail.fetch(str(i), '(RFC822)')
                body = None
                for response_part in data:
                    arr = response_part[0]
                    if isinstance(arr, tuple):
                        msg = email.message_from_string(str(arr[1], 'utf-8'))
                        if developer_mode:
                            print('msg : as extracted :', len(msg))
                            print('type(msg) :', type(msg))
                        if msg.is_multipart():
                            for part in msg.walk():
                                ctype = part.get_content_type()
                                cdispo = str(part.get('Content-Disposition'))
                                # skip any text/plain (txt) attachments
                                if ctype == 'text/plain' and 'attachment' not in cdispo:
                                    body = str(part.get_payload(decode=True))  # decode
                                    # print('\nGuessed body content ( if part) :', body, end='\n')
                                    break
                        # not multipart - i.e. plain text, no attachments, keeping fingers crossed
                        else:
                            body = str(msg.get_payload(decode=True))
                            # print('\nGuessed body content ( else part) :', body, end='\n')
                        print()
                        email_subject = msg['subject']
                        email_from = msg['from']
                        email_to = msg['to']
                        email_date = msg['date']
                        # email_cc = msg['cc']
                        comments = ''
                        # result_list.append({'from':email_from,'to':email_to,'subject':email_subject,'date':email_date,'body':body,'comments':comments})
                        #
                        # for res in result_list:
                        #     final_text =[res['from'],res['to'],res['subject'],res['date'],res['body'],res['comments']]
                        with open('sample_results.txt','a') as fp:
                            fp.write('\t'.join(apply_to_list([email_from,email_to,email_date,str(body).replace('\r\n','\t').replace('\t','  ')],make_string=True))+'\n')

                        print('From : ' + email_from + '\n')
                        print('Subject : ' + email_subject + '\n')
                        print('to : ' + email_to + '\n')
                        print('body : ' + body + '\n')
                        print('date : ' + email_date + '\n')

                # input('Proceed next ?')
                # sample excel output
                # full_log = [res['file_name'], res['tran_id'], res['tran_date'], res['tran_time'],
                #             res['tran_status'],
                #             res['biller_name'], res['biller_id'], res['k_number'], res['payment_mode'], res['mobile'],
                #             res['amount'],
                #             res['bill_date'], res['conv_fees'], res['total_amount']
                #             ]
                # full_log_text = apply_to_list(full_log, make_string=True)
                # # if developer_mode:
                #
                # dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                # # print("date and time =", dt_string)
                # full_log_text_log = full_log_text.copy()
                # full_log_text_log.insert(0, str(dt_string))
                # headers_log = HEADERS.copy()
                # headers_log.insert(0, 'TIMESTAMP')
                # write_excel(work_book_name='TOTAL_FILES_LOG.xlsx', rows=[full_log_text_log], headers=headers_log)
                # write_excel(work_book_name='Extracted_text.xlsx', rows=[full_log_text], headers=HEADERS)

        except Exception as e:
            traceback.print_exc()
            comments = str(e)
            print('Error while reading email :',str(e))


def write_excel(work_book_name, rows=[], headers=''):
    try:
        try:
            book = openpyxl.load_workbook(work_book_name)
            sheet = book.active

        # print('Opening excisting file !')
        except Exception as e:
            # book = Workbook(write_only=True)
            # print('Error , Creating new excel file ')
            book = Workbook(write_only=True)
            sheet = book.create_sheet()
            if headers:
                sheet.append(headers)

        for row in rows:
            sheet.append(row)

        book.save(work_book_name)
    except Exception as e:
        print ('Please close the output excel file  !!!! and rerun the application')
        exit()
    return True
# write_excel(work_book_name='Extracted_text.xlsx', rows=[full_log_text], headers=HEADERS)

def apply_to_list(input_list,make_upper = False, make_lower= False,make_int= False,make_string=False):
    # added to make the list comprehension process easy  , added on 15/10/2020
    temp_list = input_list
    if make_string: return [str(i) for i in temp_list]
    elif make_upper: return [str(i).upper() for i in temp_list]
    elif make_lower: return [str(i).lower() for i in temp_list]
    elif make_int: return [int(i) for i in temp_list]
    return temp_list

def handle_extension(input_sp, extension_to_add='.sql',developer_mode = False):
    status = False
    DIRECTORY, extracted_file_name = os.path.split(input_sp)
    sp_name = None
    file_name = None
    try:
        sp_name = str(extracted_file_name).split('.')[0]
        file_name = str(sp_name) + str(extension_to_add)
        status = True
    except Exception as e:
        developer_print('Error in handling name :',e)
        status = False
    return {
            'no_extension': sp_name
            , 'new_extension': file_name
            , 'directory': DIRECTORY
            , 'file_name': extracted_file_name
            }

# write_excel(work_book_name='Extracted_text.xlsx', rows=[full_log_text], headers=HEADERS)





# def read_email_from_gmail():
#     try:
#         mail = imaplib.IMAP4_SSL(SMTP_SERVER)
#         print ('mail :',mail)
#         try:
#             print ('Logging in........')
#             mail.login(FROM_EMAIL,FROM_PWD)
#         except Exception as e:
#             print ('Error while logging in :',e)
#             return False
#         mail.select('inbox')
#
#         data = mail.search(None, 'ALL')
#         mail_ids = data[1]
#         id_list = mail_ids[0].split()
#         first_email_id = int(id_list[0])
#         latest_email_id = int(id_list[-1])
#         print ('first_email_id :',first_email_id)
#         print ('latest_email_id :',latest_email_id)
#
#         for i in range(latest_email_id,first_email_id, -1):
#             data = mail.fetch(str(i), '(RFC822)' )
#             for response_part in data:
#                 arr = response_part[0]
#                 if isinstance(arr, tuple):
#                     msg = email.message_from_string(str(arr[1],'utf-8'))
#                     print('msg : as extracted :',len(msg))
#                     print('type(msg) :',type(msg))
#                     # Try1
#                     # b = email.message_from_string(a)
#                     # if msg.is_multipart():
#                     #     for payload in msg.get_payload():
#                     #         # if payload.is_multipart(): ...
#                     #         print ('Guessed body content ( if part) :',payload.get_payload())
#                     # else:
#                     #     print ('Guessed body content - else part :',msg.get_payload())
#
#                     # try 02
#                     if msg.is_multipart():
#                         for part in msg.walk():
#                             ctype = part.get_content_type()
#                             cdispo = str(part.get('Content-Disposition'))
#
#                             # skip any text/plain (txt) attachments
#                             if ctype == 'text/plain' and 'attachment' not in cdispo:
#                                 body = part.get_payload(decode=True)  # decode
#                                 print('\nGuessed body content ( if part) :', body,end='\n')
#                                 break
#                     # not multipart - i.e. plain text, no attachments, keeping fingers crossed
#                     else:
#                         body = msg.get_payload(decode=True)
#                         print('\nGuessed body content ( else part) :', body, end='\n')
#
#                     email_subject = msg['subject']
#                     email_from = msg['from']
#                     email_cc = msg['cc']
#
#
#                     print('From : ' + email_from + '\n')
#                     print('Subject : ' + email_subject + '\n')
#                     print('CC : ' + email_cc + '\n')
#                     print('body : ' + body + '\n')
#
#             input('Proceed next ?')
#
#     except Exception as e:
#         traceback.print_exc()
#         print(str(e))

# read_email_from_gmail()
if __name__ =='__main__':
    FROM_EMAIL = "ajithkumar@sedintechnologies.com"
    FROM_PWD = "A@sedin123"
    print (read_emails(username = FROM_EMAIL, password  = FROM_PWD, no_of_mails=5, developer_mode=True))