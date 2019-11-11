# -*- coding: utf-8 -*-
"""
    Description: This modules is used for testing. Testing is performed based on the list of commands given to perform in a website
    Version    : v1.5
    History    :
                v1.0 - 08/01/2016 - Initial version
                v1.1 - 08/05/2016 - Modified to accept List input.
                v1.2 - 08/05/2016 - Removed dead code in feed_input
                v1.3 - 08/05/2016 - Added function get_data_dictionary to return the fetched values
                v1.4 - 09/01/2016 - updated _print_ function and added log_process_status variable
                v1.5 - 09/22/2016 - variable to suppress output running. Default - output will be written to file.
    Open Issues: None.
    Pending :    Enhance coding standards. Clean up dead code in feed_input function
"""
__version__ = "1.0.0"
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from URL_Status import *
import time # for sleep
import requests #to check status of the page
from Utilities import *
class PatternScraping():

    def __init__(self,output_filename=None,developer_mode=False,print_instance=None,browser_instance=None,log_process_status=True,write_output=True):
        self.developer_mode = developer_mode
        self.log_process_status=log_process_status
        if output_filename:
            self.output_filename=output_filename
        else:
            self.output_filename='PatternScraping.' + get_timestamp_for_file() + '.testing.txt'
        self.write_output=write_output
        self.possible_commands = ['GO', 'GET_VALUE', 'CLICK', 'ENTER_VALUE','EXIT', 'SLEEP', 'GET_VALUES','GET_LINKS']
        self.possible_command_types = ['ID', 'XPATH', 'NAME', 'CLASS', 'CSS']
        self.browser = None
        self.ins_browser=browser_instance
        self.initiate_print_instance(instance_instance=print_instance)

    def _print_(self,input_string_in,skip_timestamp=False,add_leading_space=True,message_priority=''):
        module_name='PatternScraping'
        input_string=input_string_in
        if isinstance(input_string,str):
            input_string = get_html_to_unicode_string(input_string)
        if self.print_instance:
            self.print_instance.customPrint(input_string,skip_timestamp=skip_timestamp,add_leading_space=add_leading_space,module_name=module_name,message_priority=message_priority)
        else:
            print_string=u'' + module_name + '\t' + message_priority + '\t' + input_string
            if not skip_timestamp:
                print_string = log_time_stamp() + print_string
            print get_printable_string(print_string)
    def initiate_print_instance(self,instance_instance=None):
        self.print_instance=None
        if instance_instance:
            try:
                if instance_instance.check():
                    self.print_instance=instance_instance
                    return True
            except:            
                return False        
        return False
    def validate_input_commands(self,list_of_commands):#commands have tupple
        print_prefix='validate_input_commands\t'
        for i in range(len(list_of_commands)):
            if self.developer_mode:
                self._print_(print_prefix + 'Current Input:' + str(list_of_commands[i]))
            if list_of_commands[i][0] not in self.possible_commands:
                self._print_(print_prefix + 'Command not in list:' + str(list_of_commands[i][0]))
                custom_exit()
            line_no = str(i + 1)
            list_length = len(list_of_commands[i])
            command_name=list_of_commands[i][0]
            if command_name not in ['GO','SLEEP','EXIT'] and list_of_commands[i][1] not in self.possible_command_types:
                status="Unknown command type"+" in line number "+ line_no
                self._print_(print_prefix + status)
                custom_exit()
            if command_name == 'GO':
                if not list_of_commands[i][1]:
                    status = "no link provided" + " in line number "+ line_no
                    self._print_(print_prefix + status)
                    custom_exit()
            if command_name == 'GET_VALUE':
                if list_length != 4 or any(list_of_commands[i]) is False:
                    status = "no data provided"+" in line number "+ line_no
                    self._print_(print_prefix + status)
                    custom_exit()
            if command_name == 'GET_VALUES':
                if list_length != 4 or any(list_of_commands[i]) is False:
                    status = "no link provided"+" in line number "+ line_no
                    self._print_(print_prefix + status)
                    custom_exit()
            if command_name == 'CLICK':
                if list_length != 3 and list_length != 5:
                    status = "click command length error "+" in line number "+ line_no
                    self._print_(print_prefix + status)
                    custom_exit()
                if any(list_of_commands[i]) is False:
                    status = "click syntax error"+" in line number "+ line_no
                    self._print_(print_prefix + status)
                    custom_exit()
            if command_name == 'ENTER_VALUE':
                if not (list_length == 4 and list_of_commands[i][2]
                                        and list_of_commands[i][3]):
                    status = "ENTER VALUE syntax error"+" in line number "+ line_no
                    self._print_(print_prefix + status)
                    custom_exit()
            if command_name == 'SLEEP':
                if not (list_of_commands[i][1] and (list_length == 2)):
                    status = "SLEEP time not provided"+" in line number "+ line_no
                    self._print_(print_prefix + status)
                    custom_exit()
            if command_name == 'EXIT':
                if list_length != 1:
                    status = "Exit syntax error"+" in line number "+ line_no
                    self._print_(print_prefix + status)
                    custom_exit()
        return True
    def feed_input(self, input_commands):
        print_prefix='feed_input\t'
        self.data_dict = {}
        #if self.developer_mode: self._print_(self.browser.page_source)
        if isinstance(input_commands,str):
            with open(input_commands, "r") as fopen:
                self.base_list_of_lists = []
                self.command_list = fopen.readlines()
                for each_line in self.command_list:
                    self.base_list_of_lists.append((each_line.replace("\n", "")).split("\t"))
        elif isinstance(input_commands,list):
            self.base_list_of_lists=input_commands
        else:
            self._print_(print_prefix + ' Input argument should be either string(filename) or list(commands). Passed:' + str(type(input_commands)))
            custom_exit()
        input_status=self.validate_input_commands(self.base_list_of_lists)
        if self.developer_mode and input_status:
            self._print_(print_prefix + 'Input is Valid')
        return True

    def run(self):
        if not self.ins_browser:
            if not self.browser:
                self.browser = webdriver.PhantomJS()#Chrome()
        else:
            self.browser=self.ins_browser
        i = 0
        for each_list in self.base_list_of_lists:
            if self.developer_mode: 
                self._print_('Input:\t' +  str(i + 1) + '\t' + str(each_list))
            line = '\t'.join(each_list)
            if each_list[0] == 'GO':
                try:
                    status = self.go(each_list)
                    if self.developer_mode: self._print_('Command:\tGO\tStatus\t' + str(status))
                    self.file_write(line, status)
                    if status == 'Not available':
                        return 'Not available'
                except Exception as e:
                    self.file_write(line, str(e))
                    return str(e)
            elif each_list[0] == 'GET_VALUE':
                try:
                    status = self.get_value(each_list)
                    if self.developer_mode: self._print_('Command:\tGET_VALUE\tStatus\t' + str(status))
                    self.file_write(line, status)
                except Exception as e:
                    self.file_write(line, str(e))
                    return str(e)
            elif each_list[0] == 'GET_VALUES':
                # self._print_(self.browser.page_source.encode('utf-8')
                try:
                    status = self.get_values(each_list)
                    if self.developer_mode: self._print_('Command:\tGET_VALUES\tStatus\t' + str(status))          
                    self.file_write(line, status)
                except Exception as e:
                    self.file_write(line, str(e))
                    return str(e)
            elif each_list[0] == 'GET_LINKS':
                try:
                    self.file_write(line, "Links as below")
                    status = self.get_links(each_list)
                    if self.developer_mode: self._print_('Command:\tGET_LINKS\tStatus\t' + str(status))
                except Exception as e:
                    self.file_write(line, str(e))
                    return str(e)
            elif each_list[0] == 'CLICK':
                try:
                    status = self.click(each_list)  
                    if self.developer_mode: self._print_('Command:\tCLICK\tStatus\t' + str(status))
                    self.file_write(line, status)
                    if status == 'Not available':
                        return 'Not available'
                except Exception as e:
                    self.file_write(line, str(e))
                    return str(e)
            elif each_list[0] == 'ENTER_VALUE':
                try:
                    status = self.enter_value(each_list)
                    if self.developer_mode: self._print_('Command:\tENTER_VALUE\tStatus\t' + str(status))
                    self.file_write(line, status)
                    if status == 'Not available':
                        return 'Not available'
                except Exception as e:
                    self.file_write(line, str(e))
                    return str(e)
            elif each_list[0] == 'SLEEP':
                self.sleep(each_list[1])
                status = "Slept for " + each_list[1] + " second(s)"
                if self.developer_mode: self._print_('Command:\tSLEEP\tStatus\t' + str(status))
                self.file_write(line, status)
            elif each_list[0] == 'EXIT':
                self.file_write("EXIT", "OK")
                if self.developer_mode: self._print_('Command:\tEXIT')
                self.browser.quit()
            i += 1

    def go(self, list_of_values):
        self.browser.get(list_of_values[1])
        r = requests.get(list_of_values[1])
        time.sleep(2)
        link_status = r.status_code
        return link_status
    def close(self):
        if not self.ins_browser:
            if self.browser:
                self.browser.quit()
    def click(self, list_of_values):
        try:
            if list_of_values[1] == 'ID':
                a_obj = self.find_by_id(list_of_values[2])
            elif list_of_values[1] == 'XPATH':
                a_obj = self.find_by_xpath(list_of_values[2])
            elif list_of_values[1] == 'NAME':
                a_obj = self.find_by_name(list_of_values[2])
            elif list_of_values[1] == 'CLASS':
                a_obj = self.find_by_class(list_of_values[2])
            if len(list_of_values) == 3:
                a_obj.click()
                return "OK"
            elif len(list_of_values) > 3:
                if list_of_values[4] == 'Available':
                    if list_of_values[3] in self.data_dict.keys():
                        a_obj.click()
                        return "OK"
                    else:
                        return "Not available"
                elif list_of_values[4] == 'Not Available':
                    if list_of_values[3] not in self.data_dict.keys():
                        a_obj.click()
                        self._print_('Function:\tclick\tCondition:\t' + 'Available')
                        return "OK"
                    else:
                        return "Not available"
                else:
                    if list_of_values[4] == self.data_dict[list_of_values[3]]:
                        a_obj.click()
                        return "OK"
                    else:
                        return "Not available"
        except NoSuchElementException as e:
            self._print_('Function:\tclick\tError:\t' + str(e) + '\t Input:' + str(list_of_values))
            return "Not available"

    def get_value(self, list_of_values):
        if list_of_values[1] == 'ID':
            a_obj = self.find_by_id(list_of_values[2])
        elif list_of_values[1] == 'XPATH':
            a_obj = self.find_by_xpath(list_of_values[2])
        elif list_of_values[1] == 'NAME':
            a_obj = self.find_by_name(list_of_values[2])
        if a_obj:
            self.data_dict[list_of_values[3]] = a_obj.text
            if self.developer_mode: self._print_('Function\tget_value\tData:\t' + str(self.data_dict))
            return a_obj.text
        return "Not available"

    def get_values(self, list_of_values):
        edge_list = []
        new_news_list = []
        if list_of_values[1] == 'CLASS':
            elements = self.find_by_css_selector(list_of_values[2])
        elif list_of_values[1] == 'XPATH':
            elements = self.find_by_xpath(list_of_values[2])
        elif list_of_values[1] == 'NAME':
            elements = self.find_by_name(list_of_values[2])
        elif list_of_values[1] == 'CSS':
            elements = self.find_by_css_selector(list_of_values[2])
        if elements:
            edge_list = [a.get_attribute("href") for a in elements] 
        for each in edge_list:
            if each and (not each.startswith('mailto')) and each not in new_news_list:
                new_news_list.append(each)
        return new_news_list

    def get_links(self, list_of_values):
        edge_list = []
        new_news_list = []
        if list_of_values[1] == 'CLASS':
            path = "div."+list_of_values[2]+" a"
            elements = self.find_by_css_selector(path)
        elif list_of_values[1] == 'ID':
            path = "div#"+list_of_values[2]+" a"
            elements = self.find_by_css_selector(path)
        if elements:        
            edge_list = [a.get_attribute("href") for a in elements] 
        for each in edge_list:
            if each and (not each.startswith('mailto')) and each not in new_news_list:
                new_news_list.append(each)
        if new_news_list: #do we need to check the 4th argument
            self.data_dict[list_of_values[3]]=new_news_list
        main_window = self.browser.current_window_handle        
        if self.developer_mode: self._print_('Function\tget_links\tData:\t' + str(new_news_list))
        self.file_write("",str(len(new_news_list))+ " link(s) found. Their status are: (link"+"\t"+"is_url_active"+"\t"+"is_redirected"+"\t"+"redirected_to"+")")
        for each_link in new_news_list:
            res_dict = url_check_status(each_link)
            line = each_link+"\t"+res_dict['URL_Active']+"\t"+res_dict['Redirected']
            self.file_write(line, res_dict['Redirected_into'])  
        return new_news_list
        
    def enter_value(self, list_of_values):
        if list_of_values[1] == 'ID':
            a_obj = self.find_by_id(list_of_values[2])
        elif list_of_values[1] == 'XPATH':
            a_obj = self.find_by_xpath(list_of_values[2])
        elif list_of_values[1] == 'NAME':
            a_obj = self.find_by_name(list_of_values[2])            
        if a_obj:
            if list_of_values[3] == "Keys.ENTER":
                a_obj.send_keys(Keys.ENTER)
            else:
                a_obj.send_keys(list_of_values[3])
            return "Value entered"
        return "Not available"

    def sleep(self, sleep_time):
        time.sleep(float(sleep_time))
        return True

    def find_by_id(self, input_id):
        input_id_obj = self.browser.find_element_by_id(input_id)
        return input_id_obj
    
    def find_elements_by_id(self, input_id):
        input_id_obj = self.browser.find_elements_by_id(input_id)
        return input_id_obj

    def find_by_xpath(self, input_xpath):
        input_xpath_obj = self.browser.find_element_by_xpath(input_xpath)
        return input_xpath_obj

    def find_by_name(self, input_name):
        input_id_obj = self.browser.find_element_by_name(input_name)
        return input_id_obj
        
    def find_by_class(self, input_name):
        input_class_obj = self.browser.find_element_by_class_name(input_name)
        return input_class_obj
        
    def find_by_css_selector(self, input_name):
        input_class_obj = self.browser.find_elements_by_css_selector(input_name)
        return input_class_obj

    def file_write(self, command_line, status):
        if self.write_output:
            with open(self.output_filename, "a") as result_file:
                result_file.write(command_line + "\t" + str(status) + "\n")
    def get_data_dictionary(self):
        return self.data_dict

if __name__ == '__main__':
    # input_filename = 'input.txt'
    input_filename = 'input_22.txt'
    output_filename = 'output.txt'
    obj = PatternScraping(developer_mode=True)
    obj.feed_input([['GO','https://www.google.com'],['SLEEP','1'],['ENTER_VALUE','ID','lst-ib','Testing Automation'],['CLICK','NAME','btnG'],['SLEEP','5'],['EXIT']])
    obj.run()