"""
    Description: Common functions related file handling
    Version    : v1.4
    History    :
                v1.0 - 12/22/2016 - Publishing as major version
                v1.1 - 01/31/2017 - Function extract_columns is to extract columns from each line of a file
                v1.2 - 02/03/2017 - rename and file timestamp function
                v1.3 - 02/17/2017 - New function bulk_move based on extension , pattern
                v1.4 - 04/13/2017 - Added get_all_directories
    Open Issues: None.
    Pending : Clean up
"""

import sys
import json
import os
import os.path
from os import walk
import fnmatch
import datetime,time
from Utilities import * #used for get_printable_string
class FileHandling():
    def __init__(self,field_delimiter=',',trim_fields_char=None,record_trim_chars=None,debug_mode=True,developer_mode=False,print_instance=None,log_process_status=True):
        self.field_delimiter=field_delimiter
        self.trim_fields_char=trim_fields_char
        self.record_trim_chars=record_trim_chars
        self.file_name_is=None
        self.directory_name=None
        self.file_name_ext=None
        self.file_name_base=None
        self.processed_line_count=-2
        self.delimted_file_set=False
        self.chunk_size=65536
        self.file_size=None
        self.debug_mode=debug_mode
        self.developer_mode=developer_mode
        self.log_process_status=log_process_status
        self.initiate_print_instance(print_instance)
        self.set_delimited_file_setting()
        self.set_output_file()
    def _print_(self,input_string_in,skip_timestamp=False,add_leading_space=True,message_priority=''):
        module_name='CompanyPage'
        input_string=input_string_in
        if isinstance(input_string,str):
            input_string = get_html_to_unicode_string(input_string)
        if self.print_instance:
            self.print_instance.customPrint(input_string,skip_timestamp=skip_timestamp,add_leading_space=add_leading_space,module_name=module_name,message_priority=message_priority)
        else:
            print_string=u'' + module_name + '\t' + message_priority + '\t' + input_string
            if not skip_timestamp:
                print_string = log_time_stamp() + print_string
            # print get_printable_string(print_string)
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
    def _remove_files_(self,directory_is,pattern):
        current_directory_is=None
        if directory_is:
            if os.path.isdir(directory_is):
                current_directory_is=directory_is
        if not current_directory_is:
            current_directory_is=self.directory_name
        result_file=[]
        for (root_path,dir_list,file_list) in walk(current_directory_is):
            for f_name in file_list:
                if pattern:
                    if full_path:
                        if fnmatch.fnmatch(f_name,pattern):
                            result_file.append(os.path.abspath(os.path.join(root_path, f_name)))
                    else:
                        if fnmatch.fnmatch(f_name,pattern):
                            result_file.append(f_name)
                else:
                    if full_path:
                        result_file.append(os.path.abspath(os.path.join(root_path, f_name)))
                    else:
                        result_file.append(f_name)        
            return result_file
    def _file_size_(self):
        statinfo = os.stat(self.file_name_is)        
        return statinfo.st_size
    def _return_chunk_(self,my_hanlde):
        while 1:
            block = my_hanlde.read(self.chunk_size)
            if not block:
                break
            yield block
    def is_list_of_dict(self,input_is):
        has_dict=False 
        if isinstance(input_is,list):
            for each_item in input_is:
                if isinstance(each_item,dict):
                    has_dict=True
                else:
                    return False
            return has_dict
        return False
    def set_file_name(self,file_name_is):
        if os.path.isfile(file_name_is):
            self.file_name_is=file_name_is
            self.processed_line_count=-1
        else:
            print ("File does not exist:" + file_name_is)
            self.processed_line_count=-2
            return
        if not os.path.dirname(self.file_name_is):
            self.directory_name=os.getcwd()
        else:
            self.directory_name=os.path.dirname(self.file_name_is)
        base_name_is=os.path.basename(self.file_name_is)
        self.file_name_base=os.path.splitext(base_name_is)[0]
        self.file_name_ext=os.path.splitext(base_name_is)[1].strip('.')
        self.file_size=self._file_size_()
        if self.debug_mode: self._print_ ( 'File Name Set -' + self.file_name_is)
    def get_file_name(self):
        return self.file_name_is
    def get_file_extension(self):
        return self.file_name_ext
    def get_file_base_name(self):
        return self.file_name_base
    def get_file_directory(self):
        return self.directory_name  
    def set_directory_name(self,directory_is,reset_on_failure=True):
        output_is=False
        if directory_is and os.path.isdir(directory_is):
            self.directory_name=directory_is
            output_is=True
            if self.debug_mode: self._print_ ( 'File Handling Instance - Directory name is set to ' + self.directory_name)
        else:
            if directory_is and self.debug_mode: self._print_ ( 'File Handling Instance - Directory does not exist:' + directory_is)
            if reset_on_failure:
                self.directory_name=None        
        self.file_name_base=None
        self.file_name_ext=None
        self.file_name_is=None
        return output_is
    def set_extension(self,new_extension):
        if len(new_extension.strip())>0:
            self.file_name_ext=new_extension.strip()
            self.file_name_is=self.directory_name + '\\' + self.file_name_base + '.' + self.file_name_ext
            return True
        return False
    def print_data(self,data_,medium='print'):
        delimiter='\t'
        if isinstance(data_,list):
            if self.is_list_of_dict(data_):
                for item_dict in data_:
                    output_line=''
                    for item_key in item_dict:
                        output_line =output_line +delimiter + str(item_dict[item_key])
                    print output_line.strip(delimiter)
            else:
                for item in data_:
                    print item
        elif isinstance(data_,dict):
            output_line=''
            for item in data_:
                output_line =output_line +delimiter + str(data_[item])
            print output_line.strip(delimiter)
        else:
            print str(data_)
    def get_all_files(self,directory_is=None,pattern=None,full_path=True,recursive=False):
        #directory_is or self.directory_name is mandatory
        iter=0
        if self.debug_mode: self._print_ ( 'Get All File Name - Starts')
        current_directory_is=None
        if directory_is:
            if os.path.isdir(directory_is):
                current_directory_is=directory_is
        if not current_directory_is:
            if not self.directory_name:
                if self.debug_mode: self._print_ ( 'Get All File Name - Directory name is missing')
                return []
            current_directory_is=self.directory_name
        result_file=[]
        for (root_path,dir_list,file_list) in walk(current_directory_is):
            iter_inner=0
            for f_name in file_list:
                if pattern:
                    if full_path:
                        if fnmatch.fnmatch(f_name,pattern):
                            result_file.append(os.path.abspath(os.path.join(root_path, f_name)))
                    else:
                        if fnmatch.fnmatch(f_name,pattern):
                            result_file.append(f_name)
                else:
                    if full_path:
                        result_file.append(os.path.abspath(os.path.join(root_path, f_name)))
                    else:
                        result_file.append(f_name)
            if not recursive:
                if self.debug_mode: self._print_ ( 'Get All File Name - Ends')
                return result_file
        if self.debug_mode: self._print_ ( 'Get All File Name - Ends')
        return result_file
    def rename_files(self,directory_is,search_string,replace_string,file_selection_pattern=None):
        if self.debug_mode: self._print_ ( 'Rename the files - Starts')
        if search_string==replace_string:
            if self.debug_mode: self._print_ ( 'Rename the files - actual string is same as replace string - \'' + replace_string + '\'')
            return False
        if file_selection_pattern:
            file_pattern_to_select=file_selection_pattern
        else:
            file_pattern_to_select='*'+ search_string + '*.*'
        list_of_files=self.get_all_files(directory_is,file_pattern_to_select,full_path=True)
        print list_of_files
        if len(list_of_files) >0:
            for each_file in list_of_files:
                try:
                    print each_file,each_file.replace(search_string,replace_string)
                    curr_folder_name=os.path.dirname(each_file)
                    curr_file_name=os.path.basename(each_file)
                    new_file_name=curr_file_name.replace(search_string,replace_string)
                    new_file_is=os.path.join(curr_folder_name,new_file_name)
                    if curr_folder_name and curr_file_name:
                        if curr_file_name == new_file_name:
                            if self.debug_mode: self._print_ ( 'File \''+ each_file + '\' is not processed. Both old and new file name are same')
                        else:
                            os.rename(each_file,new_file_is)
                            if self.debug_mode: self._print_ ( 'File is renamed from \'' + each_file + '\' to \'' + new_file_is + '\'. Result is '  + str(sys.exc_info()))
                    else:
                        if self.debug_mode: self._print_ ( 'File \''+ each_file + '\' is not processed. Not able to extract folder name and file name')
                except:
                    if self.debug_mode: self._print_ ( 'Error while renaming file from \'' + each_file + '\' to \'' + each_file.replace(search_string,replace_string) + '\'. Error is '  + str(sys.exc_info()))
                    return False                
        else:
            if self.debug_mode: self._print_ ( 'No file name found to replace in \'' + directory_is + '\'')
        if self.debug_mode: self._print_ ( 'Rename the files - Ends')
        return True
    def rename_file(self,source_file,target_file=None,target_folder=None,attach_timestamp_if_exist=True,repeatation=0):
        if (not target_file) and (not target_folder):
            print 'rename_file both target_file and target_folder are none'
            exit()
        if target_file:
            temp_target_file=target_file
        elif target_folder:
            temp_target_file=os.path.join(target_folder,os.path.basename(source_file))
        if not target_folder:
            target_folder=os.path.dirname(temp_target_file)
        if not os.path.isdir(target_folder):
            self.create_directory(target_folder)
        target_file_exist=False
        if os.path.isfile(source_file) and len(temp_target_file)>1 and '\\' in temp_target_file:
            if os.path.isfile(temp_target_file):
                target_file_directory_name=os.path.dirname(temp_target_file)
                target_file_base_name_is=os.path.basename(temp_target_file)
                target_file_file_name_base=os.path.splitext(target_file_base_name_is)[0]
                target_file_file_name_ext=os.path.splitext(target_file_base_name_is)[1].strip('.')
                temp_file_name=target_file_file_name_base + '_' + self.get_time_stamp_for_file() + '.' + target_file_file_name_ext
                
                new_target_file_name=os.path.join(target_file_directory_name,temp_file_name)
            else:
                new_target_file_name=temp_target_file
            try:
                os.rename(source_file,new_target_file_name)
            except Exception as e:
                if (' create a file when that file already exists' in str(e) or 'file exists' in str(e)) and attach_timestamp_if_exist and repeatation <= 1:
                    if self.developer_mode:
                        print str(e),'\n Now Retry'
                        print source_file,target_file,target_folder,temp_target_file,new_target_file_name
                    time.sleep(1)
                    return self.rename_file(source_file,target_file=new_target_file_name,repeatation = repeatation+1 )
                if self.developer_mode:
                    print str(e)
                    print source_file,target_file,target_folder,temp_target_file,new_target_file_name
                #exit()
            return True
        else:
            #print source_file,temp_target_file
            return False
    def get_time_stamp_for_file(self):
        return str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S'))
    def coin_file_name(self,output_extension='out',output_folder='',output_suffix='',):
        output_extension_is=''
        output_file_name_is=''
        if output_extension == self.file_name_ext:
            output_extension_is = self.file_name_ext + '.' + output_extension
        else:
            output_extension_is = output_extension
        if output_suffix == '':
            output_extension_is = '.' + output_extension_is
        else:
            output_extension_is = output_suffix + '.' + output_extension_is
        if output_folder == '':
            output_file_name_is= self.directory_name + '\\' + self.file_name_base + output_extension_is
        else:
            output_file_name_is= output_folder + '\\' + self.file_name_base + output_extension_is
        return output_file_name_is
    def split_file(self,no_of_lines=100000,file_suffix='-split-'):
        read_line_in_bulk=1
        file_iter=1
        current_line_count=0
        split_file_base_is=self.directory_name + '\\' + self.file_name_base + file_suffix
        file_handle_in=open(self.file_name_is,'r')
        output_file_base=split_file_base_is + str(file_iter) + '.' +self.file_name_ext
        file_handle_out=open(output_file_base,'w')
        if self.debug_mode: self._print_ ( output_file_base + " is created")
        while True:
            current_line=file_handle_in.readline()
            if not current_line: break
            if (current_line_count + read_line_in_bulk) <= no_of_lines :
                file_handle_out.write(current_line)
            else:
                file_handle_out.close()
                file_iter=file_iter +1
                current_line_count=0
                output_file_base=split_file_base_is + str(file_iter) + '.' +self.file_name_ext
                file_handle_out=open(output_file_base,'w')
                if self.debug_mode: self._print_ ( output_file_base + "is created")
                file_handle_out.write(current_line)     
            current_line_count = current_line_count + read_line_in_bulk
        file_handle_in.close()
        file_handle_out.close()
    def extract_columns(self,output_file_name,extract_columns,delimiters_in,append_file=True):
        read_line_in_bulk=1
        file_iter=1
        current_line_count=0
        #split_file_base_is=self.directory_name + '\\' + self.file_name_base + file_suffix
        if self.file_name_is == output_file_name:
            self._print_("Both input filename and output file name is same")
            self._print_("Input File:\t" + repr(self.file_name_is) + '\t Output File:\t' + repr(output_file_name))
            exit()
        file_handle_in=open(self.file_name_is,'rb')
        #output_file_base=split_file_base_is + str(file_iter) + '.' +self.file_name_ext
        if append_file:
            file_handle_out=open(output_file_name,'ab')
            if self.debug_mode: self._print_ ( output_file_name + " is opened for writing")
        else:
            file_handle_out=open(output_file_name,'wb')
            if self.debug_mode: self._print_ ( output_file_name + " is created")
        if isinstance(extract_columns,list):
            pass
        else:
            self._print_('extract_columns: extract_columns is list type')
            exit()
        if isinstance(delimiters_in,list):
            delimiters=copy.deepcopy(delimiters_in)
        elif isinstance(delimiters_in,str):
            delimiters=[]
            delimiters.append(delimiters_in)
        else:
            self._print_('extract_columns: delimiters_in is list/string type')
            exit()
        record_count=0
        processed_record_count=0
        while True:
            current_line=file_handle_in.readline()
            record_count += 1
            #print str(record_count), current_line
            if not current_line: 
                self._print_('extract_columns: no input from iteration. Read:' + str(record_count) + ' break')
                break
            modified_line=current_line.strip('\n')
            for each_delim in delimiters:
                modified_line=modified_line.replace(each_delim,'~1~2~3~')
            modified_line_split=modified_line.split('~1~2~3~')
            #print record_count,'modified_line',modified_line_split
            output_line=''
            len_of_split=len(modified_line_split)
            for each_column_index in extract_columns:
                if each_column_index < len_of_split:
                    if len(output_line) == 0:
                        output_line = modified_line_split[each_column_index]
                    else:
                        output_line = output_line + delimiters[0] + modified_line_split[each_column_index]
                else:
                    output_line=''
                    break
            if len(output_line) == 0: continue
            processed_record_count += 1
            output_line = output_line + '\n'
            file_handle_out.write(output_line)
            #print processed_record_count,'Process',output_line
            #break
        file_handle_in.close()
        file_handle_out.close()
        if self.debug_mode: self._print_('extract_columns:' + 'No Of Lines:' + str(record_count) + '\tProcessed:' + str(processed_record_count))
        return processed_record_count
    def filter_based_on_column(self,output_file_name,filter_column_dict,delimiters_in,append_file=True):
        read_line_in_bulk=1
        file_iter=1
        current_line_count=0
        #split_file_base_is=self.directory_name + '\\' + self.file_name_base + file_suffix
        if self.file_name_is == output_file_name:
            self._print_("Both input filename and output file name is same")
            self._print_("Input File:\t" + repr(self.file_name_is) + '\t Output File:\t' + repr(output_file_name))
            exit()
        file_handle_in=open(self.file_name_is,'rb')
        #output_file_base=split_file_base_is + str(file_iter) + '.' +self.file_name_ext
        if append_file:
            file_handle_out=open(output_file_name,'ab')
            if self.debug_mode: self._print_ ( output_file_name + " is opened for writing")
        else:
            file_handle_out=open(output_file_name,'wb')
            if self.debug_mode: self._print_ ( output_file_name + " is created")
        if isinstance(filter_column_dict,dict):
            pass
        else:
            self._print_('filter_based_on_column: filter_column_dict is dict type')
            exit()
        if isinstance(delimiters_in,list):
            delimiters=copy.deepcopy(delimiters_in)
        elif isinstance(delimiters_in,str):
            delimiters=[]
            delimiters.append(delimiters_in)
        else:
            self._print_('filter_based_on_column: delimiters_in is list/string type')
            exit()
        record_count=0
        processed_record_count=0
        while True:
            current_line=file_handle_in.readline()
            record_count += 1
            #print str(record_count), current_line
            if not current_line: 
                self._print_('filter_based_on_column: no input from iteration. Read:' + str(record_count) + ' break')
                break
            modified_line=current_line.strip('\n')
            for each_delim in delimiters:
                modified_line=modified_line.replace(each_delim,'~1~2~3~')
            modified_line_split=modified_line.split('~1~2~3~')
            #print record_count,'modified_line',modified_line_split
            output_line=''
            len_of_split=len(modified_line_split)
            select_row=True
            for each_index in filter_column_dict:
                if each_index < len_of_split:
                    if modified_line_split[each_index].lower() == filter_column_dict[each_index].lower():
                        pass
                    else:
                        select_row=False
                        break
                else:
                    select_row=False
                    break
            if len(current_line) == 0 or (not select_row): continue
            processed_record_count += 1
            current_line = current_line + '\n'
            file_handle_out.write(current_line)
            #print processed_record_count,'Process',output_line
            #break
        file_handle_in.close()
        file_handle_out.close()
        if self.debug_mode: self._print_('filter_based_on_column:' + 'No Of Lines:' + str(record_count) + '\tProcessed:' + str(processed_record_count))
        return processed_record_count
    def file_len(self,line_delimiter='\n'):
        if self.processed_line_count > -1:
            return self.processed_line_count
        file_h=open(self.file_name_is,'r')
        chunk_blocks=self._return_chunk_(file_h)
        line_count_is=0
        for each_block in chunk_blocks:
            line_count_is = line_count_is + each_block.count(line_delimiter)
        file_h.close()
        return line_count_is
    def _samefile(self,src, dst):
        # Macintosh, Unix.
        if hasattr(os.path, 'samefile'):
            try:
                return os.path.samefile(src, dst)
            except OSError:
                return False

        # All other platforms: check for same pathname.
        return (os.path.normcase(os.path.abspath(src)) ==
                os.path.normcase(os.path.abspath(dst)))
    def _copyfileobj(self,fsrc, fdst, length=16*1024):
        """copy data from file-like object fsrc to file-like object fdst"""
        while 1:
            buf = fsrc.read(length)
            if not buf:
                break
            fdst.write(buf)
    def copyfile(self,src, dst):
        """Copy data from src to dst.

        If follow_symlinks is not set and src is a symbolic link, a new
        symlink will be created instead of copying the file it points to.

        """
        if self.debug_mode: self._print_ ( 'Copying file from \'' + src + '\' to \'' + dst + '\'.')        
        if self._samefile(src, dst):
            raise SameFileError("{!r} and {!r} are the same file".format(src, dst))

        for fn in [src, dst]:
            try:
                st = os.stat(fn)
            except OSError:
                # File most likely does not exist
                pass
            else:
                # XXX What about other special files? (sockets, devices...)
                if stat.S_ISFIFO(st.st_mode):
                    raise SpecialFileError("`%s` is a named pipe" % fn)

        with open(src, 'rb') as fsrc:
            with open(dst, 'wb') as fdst:
                self._copyfileobj(fsrc, fdst)
        if self.debug_mode: self._print_ ( 'File copied from \'' + src + '\' to \'' + dst + '\'.')
        return dst
    def get_partial_file(self,display_bytes=1000):
        file_h=open(self.file_name_is,'r')
        partial_content=file_h.read(display_bytes)
        file_h.close()
        return partial_content
    def create_directory(self,directory_name):
        print_prefix='create_directory:\t'
        if (not directory_name) or len(directory_name) == 0: return False
        if not os.path.isdir(directory_name):
            try:
                os.makedirs(directory_name)
                self._print_(print_prefix + 'Directory created:' + directory_name)
            except OSError as exc: # Python >2.5
                if exc.errno == errno.EEXIST and os.path.isdir(directory_name):
                    pass
                else: raise
        else:
            if self.developer_mode:
                self._print_(print_prefix + 'Directory exists:' + directory_name)
    def merge_all_files(self,directory_name,file_pattern,output_file):
        if self.debug_mode: self._print_ ( 'Merging all File - Starts. Directory name:\'' + directory_name + '\'. File Pattern is :\'' + file_pattern + '\'')
        if not os.path.isdir(directory_name):
            if self.debug_mode: self._print_ ( 'Merging all File - Exits. Directory \'' + directory_name + '\' does not exist')
            return False
        if not file_pattern:
            if self.debug_mode: self._print_ ( 'Merging all File - Exits. File pattern should be given')
            return False
        if not output_file:
            if self.debug_mode: self._print_ ( 'Merging all File - Exits. Output File name should be given')
            return False            
        all_file_list=self.get_all_files(directory_is=directory_name,pattern=file_pattern,full_path=True)
        if not all_file_list:
            if self.debug_mode: self._print_ ( 'Merging all File - Exits. No file found with pattern \'' + file_pattern + '\' in the directory \'' + directory_name + '\'')
            return False
        if self.debug_mode: self._print_ ( 'Merging all File :  Found ' + str(len(all_file_list)) + 'file(s)')
        if not self.create_file(output_file): return False
        file_w=open(output_file,'a+')
        for file_is in all_file_list:
            file_h=open(file_is,'r')
            if self.debug_mode: self._print_ ( '\t Mergin file \'' + file_is + '\'')
            chunk_blocks=self._return_chunk_(file_h)
            for each_block in chunk_blocks:
                file_w.write(each_block)            
            file_h.close()
        file_w.close()
        if self.debug_mode: self._print_ ( 'Merging all File - Completed. Directory name:\'' + directory_name + '\'. File Pattern is :\'' + file_pattern + '\'. Output File:\'' + output_file + '\'')
    def does_file_have_string(self,input_file,search_string):
        try:
            if os.path.isfile(input_file):
                file_i=open(input_file,'r')    
            else:
                return False
            if len(search_string.strip()) < 10:
                return False
            content_is=file_i.read(1000)
            #print content_is
            if search_string in content_is:
                file_i.close()
                return True
            return False
        except:
            return False
    def merge_files(self,primary_file,other_file,output_file=None):
        if primary_file == other_file: return False
        file_w=open(primary_file,'a+')
        file_h=open(other_file,'r')
        chunk_blocks=self._return_chunk_(file_h)
        for each_block in chunk_blocks:
            file_w.write(each_block)
        file_h.close()
        file_w.close()
        return True
    def create_file(self,output_file):
        try:
            if os.path.isfile(output_file):
                file_w=open(output_file,'w+')
            else:
                file_w=open(output_file,'w+')
            file_w.close()
            if self.debug_mode: self._print_ ( 'Create file completed for the file \'' + output_file + '\'')
            return True
        except:
            if self.debug_mode: self._print_ ( 'Create file failed with error ' + str(sys.exc_info())  + '\t' + '. File name: \'' + output_file + '\'')
            return False
    def set_output_file(self,output_file=''):
        self.output_file_name_is=output_file
    def set_delimited_file_setting(self,no_of_fields_restriction=0,include_column_id=None,exclude_column_id=None):
        self.delimted_file_set=True
        self.delimted_no_of_fields_restriction=no_of_fields_restriction
        self.delimted_include_column_id=include_column_id
        self.delimted_exclude_column_id=exclude_column_id
        if self.debug_mode: self._print_ ( 'Delimited File Setting is completed.')
    def process_delimited_file(self,output_append=False,break_at_line=-1,skip_lines=0):
        if self.debug_mode: self._print_ ( 'Process Delimited File - Starts')
        if not self.file_name_is:
            self._print_ ( "No Input File...existing....")
            return
        input_file_handle=open(self.file_name_is,'r')
        if self.output_file_name_is == '':
            output_file=self.file_name_is + '.out'
        else:
            output_file=self.output_file_name_is
        if output_append:
            output_file_handle=open(output_file,'a+')
        else:
            output_file_handle=open(output_file,'w')
        if self.delimted_no_of_fields_restriction > 0 :
            error_record_handle=open(self.file_name_is + '.records.bad','w')
        line_count=0        
        while True:
            current_line=input_file_handle.readline()
            if (not current_line) or line_count == break_at_line: break
            if skip_lines != 0 and (line_count + 1) <= skip_lines:
                line_count = line_count + 1
                continue
            if len(self.record_trim_chars) > 0 :
                intermediate_line=current_line.strip(self.record_trim_chars).split(self.field_delimiter)
            else:
                intermediate_line=current_line.split(self.field_delimiter)
            output_line=''
            no_of_fields=len(intermediate_line)
            if self.delimted_no_of_fields_restriction == 0 or self.delimted_no_of_fields_restriction == no_of_fields :
                col_count=1
                for each_field in intermediate_line:
                    if self.delimted_exclude_column_id and col_count in self.delimted_exclude_column_id:
                        pass
                    elif self.delimted_include_column_id and col_count not in self.delimted_include_column_id:
                        pass
                    else:
                        if len(self.trim_fields_char) > 0:
                            format_field=each_field.strip(self.trim_fields_char)
                        else:
                            format_field=each_field
                        output_line=output_line + self.field_delimiter + format_field
                    col_count=col_count + 1
                output_file_handle.write(output_line.strip(self.field_delimiter)+'\n')
            else:
                error_record_handle.write(current_line)
            line_count=line_count+1
        self.processed_line_count=line_count
        input_file_handle.close()
        output_file_handle.close()
        if self.delimted_no_of_fields_restriction > 0 :
            error_record_handle.close()
        if self.debug_mode: self._print_ ( 'Process Delimited File - Ends')

    def process_delimited_file_chunk(self,output_append=False,break_at_line=-1,skip_lines=0):
        if self.debug_mode: self._print_ ( 'Process Delimited File(c) - Starts')
        if self.debug_mode: self._print_ ( 'Process Delimited File(c) - Properties' + '.Append is ' + str(output_append) + '.Skip lines -' + str(skip_lines))
        if not self.file_name_is:
            self._print_ ( "No Input File...existing....")
            return
        input_file_handle=open(self.file_name_is,'r')
        if self.output_file_name_is == '':
            output_file=self.file_name_is + '.out'
        elif self.output_file_name_is == self.file_name_is:
            output_file=self.file_name_is + '.out'
        else:
            output_file=self.output_file_name_is
        if output_append:
            output_file_handle=open(output_file,'a+')
        else:
            output_file_handle=open(output_file,'w')
        if self.delimted_no_of_fields_restriction > 0 :
            error_record_handle=open(self.file_name_is + '.records.bad','w')
        chunk_blocks=self._return_chunk_(input_file_handle)
        line_count=0  
        error_line_count=0
        valid_line_count=0
        first_line_encountered=False
        break_flow=False
        rest_of_string_to_be_consumed=''
        for each_block in chunk_blocks:
            if break_flow: break
            start_with_newline=False
            end_with_newline=False            
            if each_block.startswith('\n'): start_with_newline=True
            if each_block.endswith('\n'): end_with_newline=True
            list_of_lines=each_block.split('\n')
            length_of_block= len(list_of_lines)
            local_line_count=0
            for current_line_is in list_of_lines:
                if len(rest_of_string_to_be_consumed) > 0:
                    current_line = rest_of_string_to_be_consumed + current_line_is
                else:
                    current_line = current_line_is
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
                if len(self.record_trim_chars) > 0 :
                    intermediate_line=current_line.strip(self.record_trim_chars).split(self.field_delimiter)
                else:
                    intermediate_line=current_line.split(self.field_delimiter)
                output_line=''
                no_of_fields=len(intermediate_line)
                if self.delimted_no_of_fields_restriction == 0 or self.delimted_no_of_fields_restriction == no_of_fields :
                    col_count=1
                    for each_field in intermediate_line:
                        if self.delimted_exclude_column_id and col_count in self.delimted_exclude_column_id:
                            pass
                        elif self.delimted_include_column_id and col_count not in self.delimted_include_column_id:
                            pass
                        else:
                            if len(self.trim_fields_char) > 0:
                                format_field=each_field.strip(self.trim_fields_char)
                            else:
                                format_field=each_field
                            output_line=output_line + self.field_delimiter + format_field
                        col_count=col_count + 1
                    output_file_handle.write(output_line.strip(self.field_delimiter)+'\n')
                    valid_line_count=valid_line_count+1
                else:
                    error_record_handle.write(current_line + '\n')
                    error_line_count=error_line_count+1
                line_count=line_count+1
                local_line_count=local_line_count+1
        self.processed_line_count=line_count                
        input_file_handle.close()
        output_file_handle.close()
        if self.delimted_no_of_fields_restriction > 0 :
            error_record_handle.close()
        if self.debug_mode: self._print_ ( 'Process Delimited File(c) - Ends.'+ ' Total:' + str(line_count)+ '. Valid:'+str(valid_line_count)+'.Error:'+str(error_line_count))
        return True
    def process_file(self):
        if self.debug_mode: self._print_ ( 'Function - process_file - Starts' + '.Input File : ' + self.file_name_is + '.Output File :'+self.output_file_name_is)        
        file_handle=open(self.file_name_is,'r')
        twitter_keys={"actor.displayName":"name","actor.preferredUsername":"username","actor.languages":"language","actor.location.displayName":"location","object.actor.postedTime":"posted_time","object.actor.languages":"post_language","generator.displayName":"device_type","body":"content","verb":"action_type"}
        JSONF=JSONFlatten('.','dot',False,15,8)
        my_local_result_flattenJSON=[]
        my_local_result_keys=[]
        JSONF_result={}
        line_count=0
        json_dict_count=0
        empty_line_count=0
        other_line_count=0
        for line in file_handle:
            line_count=line_count +1
            current_line_is=line.strip()
            if len(current_line_is) > 0 :
                if JSONF.is_JSON(current_line_is):
                    JSONF_result=JSONF.get_Flatten_JSON(json.loads(current_line_is))
                    my_local_result_flattenJSON.append(JSONF_result["flattenJSON"])
                    json_dict_count=json_dict_count+1
                else:
                    other_line_count=other_line_count+1            
            else:
                empty_line_count=empty_line_count+1
        file_handle.close()
        JSONF.write_delimited_file(self.output_file_name_is,my_local_result_flattenJSON,twitter_keys)
        if self.debug_mode: self._print_ ( 'Function - process_file - Ends' + '. Total Line:'+str(line_count) + '. JSON:'+str(json_dict_count) + '. Others:'+str(other_line_count) + '. Empty:'+str(empty_line_count))    
    def process_file_chunk(self,output_append=False,break_at_line=-1,skip_lines=0,format='json'):
        if self.debug_mode: self._print_ ( 'Function - process_file - Starts' + '.Input File : ' + self.file_name_is + '.Output File :'+self.output_file_name_is)        
        file_handle=open(self.file_name_is,'r')
        twitter_keys={"actor.displayName":"name","actor.preferredUsername":"username","actor.languages":"language","actor.location.displayName":"location","object.actor.postedTime":"posted_time","object.actor.languages":"post_language","generator.displayName":"device_type","body":"content","verb":"action_type"}
        JSONF=JSONFlatten('.','dot',False,15,8)
        JSONF.set_json_selects_keys(twitter_keys)
        if self.debug and self.developer_mode: self._print_ ( '\t' + 'process_file: Starting _return_chunk_()')
        chunk_blocks=self._return_chunk_(file_handle)        
        if self.debug and self.developer_mode: self._print_ ( '\t' + 'process_file: return from _return_chunk_()')       
        my_local_result_flattenJSON=[]
        my_local_result_keys=[]
        JSONF_result={}
        break_flow=False
        rest_of_string_to_be_consumed=''
        line_count=0 
        chunk_count=0
        valid_line_count=0
        empty_line_count=0
        other_line_count=0
        for each_block in chunk_blocks:
            chunk_count=chunk_count+1
            if self.debug and self.developer_mode: self._print_ ( '\t' + 'process_file: processing chunks: ' + str(chunk_count) + ' with length ' + str(len(each_block)))
            if break_flow: break
            end_with_newline=False            
            if each_block.endswith('\n'): end_with_newline=True
            list_of_lines=each_block.split('\n')
            length_of_block= len(list_of_lines)
            local_line_count=0
            for current_line_is in list_of_lines:
                if self.debug and self.developer_mode: self._print_ ( '\t' + 'process_file: processing chunks - Chunk:' + str(chunk_count) + '. Line:' + str(local_line_count) + ' with length ' + str(len(current_line_is)))
                if len(rest_of_string_to_be_consumed) > 0:
                    current_line = rest_of_string_to_be_consumed + current_line_is
                else:
                    current_line = current_line_is
                rest_of_string_to_be_consumed=''         
                if (local_line_count+1) == length_of_block:##last line
                    if not end_with_newline:
                        rest_of_string_to_be_consumed = current_line
                        if self.debug and self.developer_mode: self._print_ ( '\t' + 'process_file: processing chunks - Chunk:' + str(chunk_count) + '. Line:' + str(local_line_count) + ' is in last line with no new line at end')
                        break
                if line_count == break_at_line: 
                    break_flow=True
                    if self.debug and self.developer_mode: self._print_ ( '\t' + 'process_file: processing chunks - Chunk:' + str(chunk_count) + '. Line:' + str(local_line_count) + ' breaking the flow. ' + str(break_at_line) + ' Lines consumed')
                    break
                if len(current_line) == 0:
                    line_count = line_count + 1
                    if self.debug and self.developer_mode: self._print_ ( '\t' + 'process_file: processing chunks - Chunk:' + str(chunk_count) + '. Line:' + str(local_line_count) + ' line is empty')
                    continue
                if skip_lines != 0 and (line_count + 1) <= skip_lines:
                    line_count = line_count + 1
                    if self.debug and self.developer_mode: self._print_ ( '\t' + 'process_file: processing chunks - Chunk:' + str(chunk_count) + '. Line:' + str(local_line_count) + ' skipping the line')
                    continue
                current_line_is=current_line.strip()                
                if len(current_line_is) > 0 :
                    if JSONF.is_JSON(current_line_is):
                        if self.debug and self.developer_mode: self._print_ ( '\t' + 'process_file: processing chunks - Chunk:' + str(chunk_count) + '. Line:' + str(local_line_count) + '. a json format')                    
                        JSONF_result=JSONF.get_Flatten_JSON(json.loads(current_line_is))
                        my_local_result_flattenJSON.append(JSONF_result["flattenJSON"])
                        valid_line_count=valid_line_count+1
                    else:
                        if self.debug and self.developer_mode: self._print_ ( '\t' + 'process_file: processing chunks - Chunk:' + str(chunk_count) + '. Line:' + str(local_line_count) + '. Not a json format')                                        
                        other_line_count=other_line_count+1            
                else:
                    if self.debug and self.developer_mode: self._print_ ( '\t' + 'process_file: processing chunks - Chunk:' + str(chunk_count) + '. Line:' + str(local_line_count) + '. Empty line')                                    
                    empty_line_count=empty_line_count+1
                line_count=line_count+1
                local_line_count=local_line_count+1        
        file_handle.close()
        JSONF.write_delimited_file(self.output_file_name_is,my_local_result_flattenJSON,twitter_keys)
        if self.debug_mode: self._print_ ( 'Function - process_file - Ends' + '. Total Line:'+str(line_count) + '. JSON:'+str(valid_line_count) + '. Others:'+str(other_line_count) + '. Empty:'+str(empty_line_count))    
    def process_file_json_trim(self,output_append=False,break_at_line=-1,skip_lines=0,format='json'):
        if self.debug_mode: self._print_ ( 'Function - process_file JSON Trim - Starts' + '.Input File : ' + self.file_name_is + '.Output File :'+self.output_file_name_is)        
        file_handle=open(self.file_name_is,'r')
        file_handle_w=open(self.output_file_name_is,'w')
        twitter_keys={"actor.displayName":"name","actor.preferredUsername":"username","actor.languages":"language","actor.location.displayName":"location","object.actor.postedTime":"posted_time","object.actor.languages":"post_language","generator.displayName":"device_type","body":"content","verb":"action_type"}
        JSONF=JSONFlatten('.','dot',False,15,8)
        JSONF.set_json_selects_keys(twitter_keys)
        if self.debug and self.developer_mode: self._print_ ( '\t' + 'process_file JSON Trim: Starting _return_chunk_()')
        chunk_blocks=self._return_chunk_(file_handle)        
        if self.debug and self.developer_mode: self._print_ ( '\t' + 'process_file JSON Trim: return from _return_chunk_()')       
        json_trim=[]
        json_trim.append("gnip")        
        my_local_result_flattenJSON=[]
        my_local_result_keys=[]
        JSONF_result={}
        break_flow=False
        rest_of_string_to_be_consumed=''
        line_count=0 
        chunk_count=0
        valid_line_count=0
        empty_line_count=0
        other_line_count=0
        for each_block in chunk_blocks:
            chunk_count=chunk_count+1
            if self.debug and self.developer_mode: self._print_ ( '\t' + 'process_file JSON Trim: processing chunks: ' + str(chunk_count) + ' with length ' + str(len(each_block)))
            if break_flow: break
            end_with_newline=False            
            if each_block.endswith('\n'): end_with_newline=True
            list_of_lines=each_block.split('\n')
            length_of_block= len(list_of_lines)
            local_line_count=0
            for current_line_is in list_of_lines:
                if self.debug and self.developer_mode: self._print_ ( '\t' + 'process_file JSON Trim: processing chunks - Chunk:' + str(chunk_count) + '. Line:' + str(local_line_count) + ' with length ' + str(len(current_line_is)))
                if len(rest_of_string_to_be_consumed) > 0:
                    current_line = rest_of_string_to_be_consumed + current_line_is
                else:
                    current_line = current_line_is
                rest_of_string_to_be_consumed=''         
                if (local_line_count+1) == length_of_block:##last line
                    if not end_with_newline:
                        rest_of_string_to_be_consumed = current_line
                        if self.debug and self.developer_mode: self._print_ ( '\t' + 'process_file JSON Trim: processing chunks - Chunk:' + str(chunk_count) + '. Line:' + str(local_line_count) + ' is in last line with no new line at end')
                        break
                if line_count == break_at_line: 
                    break_flow=True
                    if self.debug and self.developer_mode: self._print_ ( '\t' + 'process_file JSON Trim: processing chunks - Chunk:' + str(chunk_count) + '. Line:' + str(local_line_count) + ' breaking the flow. ' + str(break_at_line) + ' Lines consumed')
                    break
                if len(current_line) == 0:
                    line_count = line_count + 1
                    if self.debug and self.developer_mode: self._print_ ( '\t' + 'process_file JSON Trim: processing chunks - Chunk:' + str(chunk_count) + '. Line:' + str(local_line_count) + ' line is empty')
                    continue
                if skip_lines != 0 and (line_count + 1) <= skip_lines:
                    line_count = line_count + 1
                    if self.debug and self.developer_mode: self._print_ ( '\t' + 'process_file JSON Trim: processing chunks - Chunk:' + str(chunk_count) + '. Line:' + str(local_line_count) + ' skipping the line')
                    continue
                current_line_is=current_line.strip()                
                if len(current_line_is) > 0 :
                    if JSONF.is_JSON(current_line_is):
                        if self.debug and self.developer_mode: self._print_ ( '\t' + 'process_file JSON Trim: processing chunks - Chunk:' + str(chunk_count) + '. Line:' + str(local_line_count) + '. a json format')                    
                        JSONF_result=JSONF.trim_JSON(current_line_is,json_trim)
                        if JSONF_result:
                            json.dump(JSONF_result,file_handle_w)
                            file_handle_w.write('\n')                    
                        valid_line_count=valid_line_count+1
                    else:
                        if self.debug and self.developer_mode: self._print_ ( '\t' + 'process_file JSON Trim: processing chunks - Chunk:' + str(chunk_count) + '. Line:' + str(local_line_count) + '. Not a json format')                                        
                        other_line_count=other_line_count+1            
                else:
                    if self.debug and self.developer_mode: self._print_ ( '\t' + 'process_file JSON Trim: processing chunks - Chunk:' + str(chunk_count) + '. Line:' + str(local_line_count) + '. Empty line')                                    
                    empty_line_count=empty_line_count+1
                line_count=line_count+1
                local_line_count=local_line_count+1        
        file_handle.close()
        file_handle_w.close()
        if self.debug_mode: self._print_ ( 'Function - process_file JSON Trim- Ends' + '. Total Line:'+str(line_count) + '. JSON:'+str(valid_line_count) + '. Others:'+str(other_line_count) + '. Empty:'+str(empty_line_count))            
    def bulk_move(self,source_directory,target_directory,pattern=None,include_extension=[],exclude_extension=[],include_no_extension=False,action_if_exists='Ignore'):
        #action_if_exists - Ignore,Replace,add_time_stamp and move,latest,oldest. Only Ignore and add_time_stamp & move is implemented
        #If multiple selection criteria is given, the first non-null indicator will be consider in pattern,include_extension,exclude_extension,include_no_extension
        #       include_no_extension will be considered along with exclude_extension or include_extension
        #       for include and exclude_extension ,only one word pattern is considered that .html is ok but html.tmp is not ok.
        if not os.path.isdir(source_directory):
            if self.developer_mode: self._print_('Directory does not exist:' + source_directory)
            return False
        if pattern or include_extension or exclude_extension or include_no_extension:
            pass
        else:
            self._print_('Provide one of the selection indicator:' + 'pattern, include_extension,exclude_extension or include_no_extension')
            return False
        if action_if_exists in ['Ignore','add_time_stamp']:#,'Replace','Latest','Oldest']:
            pass
        else:
            self._print_('Action if exists should be one of Ignore,add_time_stamp')#',Replace,Latest, Oldest')
            return False
        if pattern:
            check_pattern=pattern
        else:
            check_pattern=None
        check_include_extension=[]
        if include_extension:
            for each_item in include_extension:
                check_include_extension.append(each_item.lower())
        check_exclude_extension=[]
        if exclude_extension:
            for each_item in exclude_extension:
                check_exclude_extension.append(each_item.lower())
        check_include_no_extension=include_no_extension
        if pattern and check_include_no_extension:
            check_include_no_extension=False
        add_timestamp=False
        if action_if_exists == 'add_time_stamp':
            add_timestamp=True
        record_count = 0
        processed_record_count = 0
        for filename in os.listdir(source_directory):
            record_count += 1
            if pattern:
                if fnmatch.fnmatch(filename,pattern):
                    pass
                else:
                    continue
            else:
                if '.' in filename:
                    tmp_extension=filename.split('.')[-1].lower()
                    if check_include_extension and tmp_extension in check_include_extension:
                        pass
                    elif check_exclude_extension and tmp_extension not in check_exclude_extension:
                        pass
                    else:
                        continue
                elif check_include_no_extension:
                    pass
                else:
                    continue
            #print filename
            file_full_path=os.path.join(source_directory,filename)
            self.rename_file(file_full_path,target_folder=target_directory,attach_timestamp_if_exist=add_timestamp)
            processed_record_count += 1
            if self.developer_mode:
                self._print_('Moved the File (' + str(processed_record_count) + ' of ' + str(record_count) + '):' + repr(file_full_path))
    def get_all_directories(self,directory_is=None,recursive=False):
        #directory_is or self.directory_name is mandatory
        iter=0
        if self.debug_mode: self._print_ ( 'Get All Dir Name - Starts')
        current_directory_is=None
        if directory_is:
            if os.path.isdir(directory_is):
                current_directory_is=directory_is
        if not current_directory_is:
            if not self.directory_name:
                if self.debug_mode: self._print_ ( 'Get All Dir Name - Directory name is missing')
                return []
            current_directory_is=self.directory_name
        result_dirs=[]
        for (root_path,dir_list,file_list) in walk(current_directory_is):
            iter_inner=0
            for d_name in dir_list:
                result_dirs.append(os.path.abspath(os.path.join(root_path, d_name)))
            if not recursive:
                if self.debug_mode: self._print_ ( 'Get All Dir Name - Ends')
                return result_dirs
        if self.debug_mode: self._print_ ( 'Get All Dir Name - Ends')
        return result_dirs
    def distinct_based_on_columns(self,output_file_name,extract_columns,delimiters_in,append_file=True,has_keyword=''):
        read_line_in_bulk=1
        file_iter=1
        current_line_count=0
        #split_file_base_is=self.directory_name + '\\' + self.file_name_base + file_suffix
        if self.file_name_is == output_file_name:
            self._print_("Both input filename and output file name is same")
            self._print_("Input File:\t" + repr(self.file_name_is) + '\t Output File:\t' + repr(output_file_name))
            exit()
        file_handle_in=open(self.file_name_is,'rb')
        #output_file_base=split_file_base_is + str(file_iter) + '.' +self.file_name_ext
        if append_file:
            file_handle_out=open(output_file_name,'ab')
            if self.debug_mode: self._print_ ( output_file_name + " is opened for writing")
        else:
            file_handle_out=open(output_file_name,'wb')
            if self.debug_mode: self._print_ ( output_file_name + " is created")
        if isinstance(extract_columns,list):
            pass
        else:
            self._print_('distinct_based_on_columns: extract_columns is list type')
            exit()
        if isinstance(delimiters_in,list):
            delimiters=copy.deepcopy(delimiters_in)
        elif isinstance(delimiters_in,str):
            delimiters=[]
            delimiters.append(delimiters_in)
        else:
            self._print_('distinct_based_on_columns: delimiters_in is list/string type')
            exit()
        record_count=0
        processed_record_count=0
        processed_key=[]
        while True:
            current_line=file_handle_in.readline()
            record_count += 1
            #print str(record_count), current_line
            if not current_line: 
                self._print_('distinct_based_on_columns: no input from iteration. Read:' + str(record_count) + ' break')
                break
            modified_line=current_line.strip('\n')
            for each_delim in delimiters:
                modified_line=modified_line.replace(each_delim,'~1~2~3~')
            modified_line_split=modified_line.split('~1~2~3~')
            #print record_count,'modified_line',modified_line_split
            output_line=''
            len_of_split=len(modified_line_split)
            for each_column_index in extract_columns:
                if each_column_index < len_of_split:
                    if len(output_line) == 0:
                        output_line = modified_line_split[each_column_index]
                    else:
                        output_line = output_line + delimiters[0] + modified_line_split[each_column_index]
                else:
                    output_line=''
                    break
            if len(output_line) == 0: continue
            #print processed_record_count,'Process',output_line
            #print processed_record_count,processed_key
            if output_line.lower() in processed_key:
                continue
            if len(has_keyword)>2 and has_keyword not in output_line: continue
            processed_key.append(output_line.lower())
            processed_record_count += 1
            file_handle_out.write(current_line.strip('\n') + '\n')
            #print processed_record_count,'Process',output_line
            #if processed_record_count>3:
            #    break
        file_handle_in.close()
        file_handle_out.close()
        if self.debug_mode: self._print_('distinct_based_on_columns:' + 'No Of Lines:' + str(record_count) + '\tProcessed:' + str(processed_record_count))
        return processed_record_count
if __name__ == '__main__':
    if not True:
        f_h=FileHandling()
        f_h.set_file_name(os.path.join(os.getcwd(),'ddg_company_search_result_run2.txt'))
        f_h.extract_columns(output_file_name=os.path.join(os.getcwd(),'ddg_company_search_result_run2_wiki_urls.txt'),extract_columns=[2],delimiters_in='\t')
    elif True:
        f_h=FileHandling()
        f_h.set_file_name(os.path.join(os.getcwd(),'ddg_company_search_result_run2_wiki_urls.txt'))
        f_h.distinct_based_on_columns(output_file_name=os.path.join(os.getcwd(),'ddg_company_search_result_run2_wiki_urls_dist.txt'),extract_columns=[0],delimiters_in='\t',has_keyword='wikipedia.org',append_file=False)
    if not True:
        f_h=FileHandling()
        all_files = f_h.get_all_files(directory_is='D:\\Projects\\o9\\Newsss\\topics_all_processing\\',pattern='*.psql',full_path=False)
        for each_file in all_files:
            cnt += 1
            print str(cnt) + '.\t',each_file
            f_h.rename_file(each_file,target_folder="H:\\_code\\l_upload")
        exit()
    elif not True:
        f_h=FileHandling()
        all_dirs=f_h.get_all_directories(directory_is='C:\\Users\\ils-prabu\\Downloads\\Harish',recursive=True)
        for each_dir in all_dirs:
            print each_dir
    elif not True:
        f_h=FileHandling()
        w_o=open('all_output_files2.txt','a')
        cnt=0
        o_r=open('H:\\_code\\linkedin\\html.output.txt')
        for each_line in o_r:
            cnt +=1
            each_line=each_line.strip('\n\r')
            if not os.path.isfile(each_line):continue
            if 'inncr2' in each_line:
                print 'SKIPPED\t',str(cnt) + '.\t',each_line
            else:
                print str(cnt) + '.\t',each_line
                f_h.rename_file(each_line,target_folder="H:\\_code\\l_html")
                w_o.write(each_line + '\n')
        o_r.close()
    elif not True:
        f_h=FileHandling()
        f_h.set_file_name('f3_news.txt')
        f_h.split_file(no_of_lines=2799,file_suffix='-split-')
        exit()
    elif not True:
        f_h=FileHandling()
        f_h.rename_files(directory_is='E:\\Projects\\TFS\\productjobs\\POC\\JSON\\parallels_tech_23k\\',search_string='.pdf',replace_string='.json',file_selection_pattern='*.pdf')
    elif not True:
        f_h=FileHandling()
        f_h.set_file_name('H:\\_code\\l_files\\harish_new\\core_ui_company_social_profile.txt')
        f_h.extract_columns(output_file_name='H:\\_code\\l_files\\harish_new\\core_ui_company_social_profile_li_li.txt',extract_columns=[2],delimiters_in='|^|')
    elif not True:
        directory_list=[
            'H:\\_code\\linkedin\\CompString1'
            ,'H:\\_code\\linkedin\\CompString2'
            ,'H:\\_code\\linkedin\\CompString3'
            ,'H:\\_code\\linkedin\\CompString4'
            ,'H:\\_code\\linkedin\\CompString5'
            ,'H:\\_code\\linkedin\\CompString6'
            ,'H:\\_code\\linkedin\\EduString'
            ,'H:\\_code\\linkedin\\K700'
            ,'H:\\_code\\linkedin\\KBigBfinal_1'
            ,'H:\\_code\\linkedin\\KBigBFinal_3_100K'
            ,'H:\\_code\\linkedin\\KBigBFinal_4_119K'
            ,'H:\\_code\\linkedin\\KBigBfinal_number'
            ,'H:\\_code\\linkedin\\li_save_3'
            ,'H:\\_code\\linkedin\\li_save_4'
            ,'H:\\_code\\linkedin\\li_save_11k'
            ,'H:\\_code\\linkedin\\li_saver_7k'
            ,'H:\\_code\\linkedin\\li_save_run1'
            ,'H:\\_code\\linkedin\\li_save_run2'
            ,'H:\\_code\\linkedin\\li_save_run3'
            ,'H:\\_code\\linkedin\\li_save_run4'
            ,'H:\\_code\\linkedin\\li_saver_12K_DaaS'
            ,'H:\\_code\\linkedin\\li_saver_2K_DaaS'
            ,'H:\\_code\\linkedin\\li_save_IT_dir1'
            ,'H:\\_code\\linkedin\\li_save_IT_dir2'
            ,'H:\\_code\\linkedin\\li_save_IT_dir3'
            ]
            
        f_h=FileHandling(developer_mode=True)
        #f_h.bulk_move(source_directory='H:\\_code\\linkedin\\EduString',target_directory='P:\\linkedin_2_html',pattern=None,include_extension=[],exclude_extension=[],include_no_extension=True,action_if_exists='Ignore')
        for each_directory in directory_list:
            f_h.bulk_move(source_directory=each_directory,target_directory='P:\\linkedin_3_html',pattern=None,include_extension=[],exclude_extension=['readme','z'],include_no_extension=True,action_if_exists='Ignore')
    elif not True:
        f_h=FileHandling(developer_mode=True)
        input_file_name='C:\\Users\\ils-prabu\\Desktop\\1\\_d\\100.104.224.38_output.txt'
        f_h.set_file_name(input_file_name)
        f_h.filter_based_on_column(output_file_name='comb_conso_output.txt',filter_column_dict={2:'LinkedIn'},delimiters_in=['\t'],append_file=True)