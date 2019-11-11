# -*- coding: utf-8 -*-
"""
    Description: this module has class to read from and write to sources.
    Version    : v1.3
    History    :
                v1.0 - 08/03/2015 - Initial version
                v1.1 - 08/23/2016 - strip \r\n while reading input and output as list
                v1.2 - 10/20/2016 - read in chunk for large file.
                v1.3 - 12/02/2016 - Added file_direction to provide text as input
    Open Issues: None.
    Pending : Include CSV reading, Excel reading, Database reading.
"""
from Utilities import *
import copy
class InputOutput:
    def __init__(self,direction='Input',developer_mode=False,print_instance=None,log_process_status=True,read_as_unicode=False):
        self.log_process_status=log_process_status
        self.developer_mode=developer_mode
        self.read_as_unicode=read_as_unicode
        self.initiate_print_instance(instance_instance=print_instance)
        self.chunk_size=65536*16
        self.append_write=False
        if direction.lower() in ['input','write']:
            self.file_direction='Input'
        elif direction.lower() in ['output','read']:
            self.file_direction='Output'
        elif direction.lower() in ['text','feed']:
            self.file_direction='Feed'
        else:
            self._print_('Invalid direction for the class init')
            custom_exit()
        if self.log_process_status:
            self._print_('__init__:\t' + ' Instance created with developer_mode:' + str(self.developer_mode) + ' \t Log Process:' + str(self.log_process_status))
    def _print_(self,input_string_in,skip_timestamp=False,add_leading_space=True,message_priority=''):
        module_name='InputOutput'
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
    def _return_chunk_(self,my_hanlde):
        while 1:
            block = my_hanlde.read(self.chunk_size)
            if not block:
                break
            yield block
    def give_unicode(self,input_string):
        if not input_string: return u''
        if isinstance(input_string,unicode):
            return input_string
        elif isinstance(input_string,str):
            temp_string=u''
            temp_string = temp_string + get_html_to_unicode_string(input_string)
            return temp_string
        else:
            self._print_('give_unicode handles only string or unicode. Received:' + str(type(input_string)))
            custom_exit()
    def give_utf_8(self,input_string):
        if not input_string: return ''
        return self.give_unicode(input_string).encode('utf-8')
    def open(self,file_name,append_write=True):
        if self.file_direction == 'Input':
            self.file_name=file_name
            self.append_write=append_write
            if append_write:
                self.handle=open(self.file_name,'ab')
            else:
                self.handle=open(self.file_name,'wb')
        elif self.file_direction == 'Output':
            self.file_name=file_name
            self.handle=open(self.file_name,'rb')
        elif self.file_direction == 'Feed':
            if isinstance(file_name,str):
                self.feed_text=self.give_unicode(file_name)
            elif isinstance(file_name,unicode):
                self.feed_text=file_name
            else:
                self._print_('Read function encount incorrect data type for file_direction=\'Feed\' \t expected str/unicode. Received:' + str(type(file_name)))
                custom_exit()
    def write(self,statement,column_structure=None,delimiter='\t'):
        if isinstance(delimiter,str):
            delimiter=unicode(delimiter)
        if self.file_direction == 'Input':
            if isinstance(statement,unicode):
                self.handle.write(statement.encode('utf-8'))
                statement.encode('utf-8') #from R
            elif isinstance(statement,str):
                temp_string=u''
                temp_string = temp_string + statement # do we need decode('utf-8')?
                return temp_string.encode('utf-8')#From R
                self.handle.write(temp_string.encode('utf-8'))
            elif isinstance(statement,list):
                statement_to_process=copy.deepcopy(statement)
                for each_record in statement_to_process:
                    if isinstance(each_record,unicode):
                        self.handle.write(each_record.encode('utf-8') + '\n')
                    elif isinstance(each_record,str):
                        self.handle.write(self.give_utf_8(each_record) + '\n')
                    elif isinstance(each_record,tuple):
                        self.handle.write(self.give_utf_8(delimiter.join(list(each_record))) + '\n')
                    elif isinstance(each_record,dict):
                        if not column_structure:
                            self._print_('column_structure is not provided when the input is list of dictionaries')
                            custom_exit()
                        temp_string=u''
                        first_record=True
                        for each_value in column_structure:
                            #print 'TSTTST:',each_value,each_record[each_value],each_record
                            if not first_record:
                                if each_value in each_record:
                                    if isinstance(each_record[each_value],str) or isinstance(each_record[each_value],unicode):
                                        pass
                                    else:
                                        each_record[each_value]=str(each_record[each_value])
                                    try:
                                        temp_string=temp_string + delimiter + each_record[each_value]
                                    except:
                                        #print type(temp_string),type(each_record[each_value]),type(delimiter)
                                        #print type(temp_string),repr(each_record[each_value]),delimiter
                                        temp_string=get_html_to_unicode_string(temp_string) + delimiter + get_html_to_unicode_string(each_record[each_value])
                                else:
                                    temp_string=temp_string + delimiter + u''
                            else:
                                if each_value in each_record:
                                    if isinstance(each_record[each_value],str) or isinstance(each_record[each_value],unicode):
                                        pass
                                    else:
                                        each_record[each_value]=str(each_record[each_value])
                                    temp_string=each_record[each_value]
                                else:
                                    temp_string=u''
                                first_record=False
                        self.handle.write(self.give_utf_8(temp_string + '\n'))
                    else:
                        self._print_('Write is not permitted when statement is list and records are not string or unicode or tuple or dict')
                        custom_exit()
            else:
                self._print_('Write is not permitted when statement is not unicode or string or list')
                custom_exit()
        else:
            self._print_('Write is not permitted when direction is other than Input/Read')
            custom_exit()
    def get_file_content(self):
        print_prefix='get_file_content:\t'
        if self.file_direction == 'Output':
            chunk_blocks=self._return_chunk_(self.handle)
        else:
            return None
        line_count=0
        break_at_line=-1
        skip_lines=0
        error_line_count=0
        valid_line_count=0
        first_line_encountered=False
        break_flow=False
        rest_of_string_to_be_consumed=''
        if self.read_as_unicode:
            output_line=u''
            newline_char=u'\n'
        else:
            output_line=''
            newline_char='\n'
        for each_block in chunk_blocks:
            if break_flow: break
            start_with_newline=False
            end_with_newline=False
            if each_block.startswith('\n'): 
                start_with_newline=True
            if each_block.endswith('\n'): 
                end_with_newline=True
            list_of_lines=each_block.split('\n')
            length_of_block= len(list_of_lines)
            if self.developer_mode:
                self._print_(print_prefix + 'No of lines in current chunk:' + str(length_of_block) + '\t Lines consumed:' + str(line_count))
            local_line_count=0
            for current_line_is in list_of_lines:
                #get_html_to_unicode_string is having performance issue
                if self.read_as_unicode:
                    current_line_norm=get_html_to_unicode_string(current_line_is)
                else:
                    current_line_norm=current_line_is
                if len(rest_of_string_to_be_consumed) > 0:
                    current_line = rest_of_string_to_be_consumed + current_line_norm
                else:
                    current_line = current_line_norm
                rest_of_string_to_be_consumed=''
                if (local_line_count+1) == length_of_block:##last line
                    if not end_with_newline:
                        rest_of_string_to_be_consumed = current_line
                        break
                if line_count == break_at_line: 
                    break_flow=True
                    break
                if len(current_line) == 0:
                    line_count = line_count + 1
                    continue
                if skip_lines != 0 and (line_count + 1) <= skip_lines:
                    line_count = line_count + 1
                    continue
                output_line = output_line + newline_char + current_line
                line_count=line_count+1
                local_line_count=local_line_count+1
        if len(rest_of_string_to_be_consumed)>0:
            output_line = output_line + newline_char + rest_of_string_to_be_consumed
        return output_line
    def read(self,output_format='string',column_structure=None,delimiter='\t',filter_empty=True):
        print_prefix='read:\t'
        if False:
            file_content = self.handle.read()
            self._print_(print_prefix + 'Length of the file:' + str(len(file_content)))
            if self.read_as_unicode:
                file_content=get_html_to_unicode_string(file_content)
        else:
            if self.file_direction == 'Output':
                file_content=self.get_file_content()
            elif self.file_direction == 'Feed':
                file_content=self.feed_text
        if self.developer_mode:
            self._print_(print_prefix + 'Length of the file:' + str(len(file_content)))
        #self.close()
        #return []
        #file_content = file_content.decode('utf-8')#do I need to disable
        record_count = 0
        if output_format == 'string':
            return file_content
        elif output_format == 'list':
            output_list=[]
            for each_line in file_content.strip('\n').split('\n'):
                output_list.append(each_line.strip('\r\n'))
                if self.developer_mode:
                    record_count += 1
                    if record_count % 1000 == 0:
                        self._print_(print_prefix + 'No of records read:' + str(record_count))
            return output_list
        elif output_format in ['tuple','dict']:
            if column_structure and isinstance(delimiter,str) and isinstance(column_structure,list):
                pass
            else:
                self._print_('column_structure of list type and delimiter of string type should be provided when output_format is tuple/dict')
                custom_exit()
            output_list=[]
            length_of_column_structure=len(column_structure)
            for each_line in file_content.split('\n'):
                each_line=each_line.strip('\r\n')
                if filter_empty and len(each_line.strip()) == 0: continue
                each_line_split=each_line.split(delimiter)
                if len(each_line_split) < length_of_column_structure:
                    for iter in range(length_of_column_structure - len(each_line_split)):
                        each_line_split.append('')
                if output_format == 'tuple':
                    output_list.append(tuple(copy.deepcopy(each_line_split)))
                else:
                    temp_dict={}
                    for each_of in range(len(column_structure)):
                        temp_dict[column_structure[each_of]]=each_line_split[each_of]
                    output_list.append(temp_dict.copy())
                #print each_line_split
                if self.developer_mode:
                    record_count += 1
                    if record_count % 1000 == 0:
                        self._print_(print_prefix + 'No of records read:' + str(record_count))
            return output_list
        else:
            self._print_(print_prefix + 'Write:Read:output_format  other than string/list is reserved for future use')
            custom_exit()
    def read_schunk(self,output_format='string',column_structure=None,delimiter='\t',filter_empty=True):
        print_prefix='read:\t'
        file_content = self.handle.read()
        file_content=get_html_to_unicode_string(file_content)
        #file_content = file_content.decode('utf-8')#do I need to disable
        if output_format == 'string':
            return file_content
        elif output_format == 'list':
            output_list=[]
            for each_line in file_content.split('\n'):
                output_list.append(each_line.strip('\r\n'))
            return output_list
        elif output_format in ['tuple','dict']:
            if column_structure and isinstance(delimiter,str) and isinstance(column_structure,list):
                pass
            else:
                self._print_('column_structure of list type and delimiter of string type should be provided when output_format is tuple/dict')
                custom_exit()
            output_list=[]
            length_of_column_structure=len(column_structure)
            record_count = 0 
            for each_line in file_content.split('\n'):
                each_line=each_line.strip('\r\n')
                if filter_empty and len(each_line.strip()) == 0: continue
                each_line_split=each_line.split(delimiter)
                if len(each_line_split) < length_of_column_structure:
                    for iter in range(length_of_column_structure - len(each_line_split)):
                        each_line_split.append('')
                if output_format == 'tuple':
                    output_list.append(tuple(copy.deepcopy(each_line_split)))
                else:
                    temp_dict={}
                    for each_of in range(len(column_structure)):
                        temp_dict[column_structure[each_of]]=each_line_split[each_of]
                    output_list.append(temp_dict.copy())
                #print each_line_split
                if self.developer_mode:
                    record_count += 1
                    if record_count % 1000 == 0:
                        self._print_(print_prefix + 'No of records read:' + str(record_count))
            return output_list
        else:
            self._print_(print_prefix + 'Write:Read:output_format  other than string/list is reserved for future use')
            custom_exit()
    def close(self):
        if self.file_direction != 'Feed':
            self.handle.close()
if __name__ == '__main__':
    if not True:
        ins=InputOutput('Input')
        ins.open('ascii_mode.txt')
        ins.write('Hellow World' + '\n')
        ins.write('Lemme close it\n')
        ins.close()
        exit()
    elif True:
        ins=InputOutput('Input')
        ins.open('unicode_mode.txt')
        ins.write(u'\u2119\u01b4\u2602\u210c\xf8\u1f24' + '\n')
        ins.write(u'Ŧเเภ๔\n')
        ins.close()
        exit()
    elif True:#
        ins=InputOutput('Output')
        ins.open('ascii_mode.txt')
        content_is=ins.read(output_format='dict',column_structure=['company','country'])
        print type(content_is)
        print content_is
        ins.close()
        ins=InputOutput('Output')
        ins.open('unicode_mode.txt')
        content_is=ins.read()
        print type(content_is)
        print content_is.encode('utf-8')
        ins.close()