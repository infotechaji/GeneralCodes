"""
    Description: Common functionality to flat the JSON data
    Version    : v1.0
    History    :
                v1.0 - 12/22/2016 - Publishing as major release
    Open Issues: None.
    Pending :   clean up
"""

import json

class JSONFlatten():
    def __init__(self,field_separator='.',list_separator_style='index',debug_mode=False,max_debug_record_count=15,select_record_is=0,replace_newline=True,print_instance=None):
        self.field_separator=field_separator
        self.list_separator_style=list_separator_style
        self.json_keys=[]
        self.record_count=0
        self.max_debug_record_count=max_debug_record_count
        self.debug_mode=debug_mode
        self.select_record_is=select_record_is
        self.replace_newline=replace_newline
        self.filter_on_json_keys=[]
        self.__initiate_print_instance__(print_instance)
        if self.list_separator_style not in ('index','dot','nothing'):
            self.list_separator_style ='index'
        if self.debug_mode: self._print_ ('\t' + 'JSON Flatten - Instance created')
    def _print_(self,input_string,skip_timestamp=False,add_leading_space=True):
        if self.print_instance:
            self.print_instance.customPrint(input_string,skip_timestamp=skip_timestamp,add_leading_space=add_leading_space)
        else:
            print input_string
    def __initiate_print_instance__(self,instance_instance=None):
        self.print_instance=None
        if instance_instance:
            try:
                if instance_instance.check():
                    self.print_instance=instance_instance
                    return True
            except:            
                return False        
        return False
    def is_JSON(self,to_be_checked_string):
        try:
            json_object = json.loads(to_be_checked_string)
        except ValueError, e:
            return False
        return True
    def trim_JSON(self,json_string,keys_to_remove):
        json_object={}
        if not self.is_JSON(json_string):
            return json_object        
        try:
            json_object = json.loads(json_string)
            for each_key in keys_to_remove:
                json_object.pop(each_key,None)
            return json_object
        except ValueError, e:
            pass
        return json_object
    def get_JSON(self,json_string):
        json_object={}
        if not self.is_JSON(json_string):
            return json_object        
        try:
            json_object = json.loads(json_string)
            return json_object
        except ValueError, e:
            pass
        return json_object.copy()
    def recursive_Flatten(self,parent_name,passedInput):
        return_flattn_data={}
        just_string=''
        curr_data_string=''
        if isinstance(passedInput,dict):
            for item in passedInput:
                just_string=parent_name + self.field_separator + item
                just_string=just_string.lstrip(self.field_separator)  
                if self.list_separator_style == 'index':
                    just_string=just_string.replace(']'+self.field_separator,']')
                elif self.list_separator_style == 'dot':
                    just_string=just_string.replace('.'+self.field_separator,'.')
                else:
                    just_string=parent_name.lstrip(self.field_separator)                
                if isinstance(passedInput[item],dict):
                    return_flattn_data.update(self.recursive_Flatten(parent_name + self.field_separator + str(item),passedInput[item]))
                elif isinstance(passedInput[item],list):
                    return_flattn_data.update(self.recursive_Flatten(parent_name + self.field_separator + str(item), passedInput[item]))
                elif isinstance(passedInput[item],str):
                    #print passedInput[item]
                    curr_data_string=passedInput[item]#.encode('ascii', 'ignore')#.decode('ascii')
                    if self.replace_newline: curr_data_string = curr_data_string.replace('\n',' ').replace('\r','')
                    if not self.filter_on_json_keys: 
                        return_flattn_data[just_string ]= curr_data_string
                    elif just_string in self.filter_on_json_keys: 
                        return_flattn_data[just_string ]= curr_data_string
                    self.json_keys.append(just_string)
                elif isinstance(passedInput[item],unicode):
                    curr_data_string=passedInput[item].encode('ascii', 'ignore')#.decode('ascii')
                    if self.replace_newline: curr_data_string = curr_data_string.replace('\n',' ').replace('\r','')
                    if not self.filter_on_json_keys: 
                        return_flattn_data[just_string ]= curr_data_string
                    elif just_string in self.filter_on_json_keys: 
                        return_flattn_data[just_string ]= curr_data_string
                    self.json_keys.append(just_string)                    
                else:
                    curr_data_string= str(passedInput[item])
                    if self.replace_newline: curr_data_string = curr_data_string.replace('\n',' ').replace('\r','')
                    if not self.filter_on_json_keys: 
                        return_flattn_data[just_string ]= curr_data_string
                    elif just_string in self.filter_on_json_keys: 
                        return_flattn_data[just_string ]= curr_data_string
                    self.json_keys.append(just_string)      
        elif isinstance(passedInput,list):
            for iter,item in enumerate(passedInput):
                if self.list_separator_style == 'index':
                    list_iter_add='[' + str(iter) + ']'
                    just_string=parent_name.lstrip(self.field_separator).replace(']'+self.field_separator,']')
                elif self.list_separator_style == 'dot':
                    list_iter_add =  '.' + str(iter) + '.'
                    just_string=parent_name.lstrip(self.field_separator).replace('.'+self.field_separator,'.')
                else:
                    list_iter_add = ''      
                    just_string=parent_name.lstrip(self.field_separator)
                if isinstance(item,dict):
                    return_flattn_data.update(self.recursive_Flatten(parent_name + list_iter_add,item))                    
                elif isinstance(item,list):
                    return_flattn_data.update(self.recursive_Flatten(parent_name + list_iter_add, item))
                elif isinstance(item,str):
                    curr_data_string= item.encode('ascii', 'ignore')#.decode('ascii')
                    if self.replace_newline: curr_data_string = curr_data_string.replace('\n',' ').replace('\r','')                    
                    if not self.filter_on_json_keys: 
                        return_flattn_data[just_string ]= curr_data_string
                    elif just_string in self.filter_on_json_keys: 
                        return_flattn_data[just_string ]= curr_data_string
                    self.json_keys.append(just_string)
                elif isinstance(item,unicode):
                    curr_data_string=item.encode('ascii', 'ignore')#.decode('ascii')
                    if self.replace_newline: curr_data_string = curr_data_string.replace('\n',' ').replace('\r','')
                    if not self.filter_on_json_keys: 
                        return_flattn_data[just_string ]= curr_data_string
                    elif just_string in self.filter_on_json_keys: 
                        return_flattn_data[just_string ]= curr_data_string
                    self.json_keys.append(just_string)   
                else:
                    curr_data_string=repr(item)
                    if self.replace_newline: curr_data_string = curr_data_string.replace('\n',' ').replace('\r','')
                    if not self.filter_on_json_keys: 
                        return_flattn_data[just_string ]= curr_data_string
                    elif just_string in self.filter_on_json_keys: 
                        return_flattn_data[just_string ]= curr_data_string
                    self.json_keys.append(just_string)
        else:
            self._print_ ( "\n\nError\n\n",type(passedInput))
        return return_flattn_data
    def set_json_selects_keys(self,select_key_json={}):
        self.filter_on_json_keys=[]
        for each_key in select_key_json:
            self.filter_on_json_keys.append(each_key)
    def get_Flatten_JSON(self,passedJSON):
        flattn_dict={}
        return_flattn_dict={}
        delete_JSON={}
        if isinstance(passedJSON,dict):
            flattn_dict.update(self.recursive_Flatten("",passedJSON))
        elif isinstance(passedJSON,list):
            flattn_dict.update(self.recursive_Flatten("",passedJSON))
        else:
            if self.debug_mode: self._print_ ( 'JSON Flatten - get Flatten JSON - Unknown error')
            raise MyException("Invalid JSON Input of type" + str(type(passedJSON)) + " " + passedJSON)
        self.json_keys=list(set(self.json_keys))
        return_flattn_dict["flattenJSON"]=flattn_dict
        self.record_count=self.record_count+1
        return return_flattn_dict
    def print_Flatten_JSON(self,flatted_JSON):
        output_string=''
        if isinstance(flatted_JSON,dict):
            input_JSON=flatted_JSON
        elif self.is_JSON(flatted_JSON):
            input_JSON=json.loads(flatted_JSON)
        for each_key_pair in input_JSON:
            output_string = output_string + each_key_pair + " : " + str(input_JSON[each_key_pair]) + "\n"
        return output_string
    def debug_mode_details(self,this_json):
        if self.select_record_is == 0 or self.select_record_is == self.record_count:
            for item in sorted(this_json):
                print self.record_count,item,"=",this_json[item]
    def encode_to_ucs2le(self,each_line,just_convert=True):
        current_line=each_line
        if current_line and just_convert:
            if current_line.endswith('\n'): current_line=current_line.replace('\n','\r\n')
            return current_line.encode('utf-16le')
        if len(current_line.strip('\r\n\t'))>0:
            if '|^|' not in current_line and '\t' in current_line:
                current_line=current_line.replace('\t','|^|')
            if current_line.endswith('\r\n'):
                return current_line.decode('utf-8').encode('utf-16le')#.replace('\r\n','\n')
            elif current_line.endswith('\n'):
                current_line=current_line.replace('\n','\r\n')
                return current_line.decode('utf-8').encode('utf-16le')#.replace('\r\n','\n')
        else:
            return current_line.decode('utf-8').encode('utf-16le')
    def get_Flatten_JSON_keys(self):
        return list(set(self.json_keys))
    def write_delimited_file(self,file_name,list_of_JSON,list_of_keys,column_separator='\t',encode=False,write_header=False):
        if self.debug_mode: self._print_ ( 'JSON Flatten - write to file - Starts')
        if self.debug_mode: self._print_ ( 'JSON Flatten - write to file - File Name: ' + file_name)
        result_list=[]
        print ('write_delimited_file , encode Status :',encode)
        if encode:
            fw=open(file_name,"wb")
        else:
            fw=open(file_name,"w")
        header_is=''
        for column_name in list_of_keys:
            header_is=str(header_is) + column_separator + str(column_name)
        if encode :
            encoded_header=str(self.encode_to_ucs2le(header_is.strip(column_separator))) +str(self.encode_to_ucs2le("\n"))
            if write_header:
                fw.write(encoded_header)
        else:
            fw.write(header_is.strip(column_separator) + "\n")
        myiter=0        
        for sJSON in list_of_JSON:
            result_list=[]
            myiter=myiter+1            
            for value in list_of_keys:
                if value in sJSON:
                    result_list.append(sJSON[value].replace(column_separator,' '))
                else:
                    result_list.append("")
            if encode:
                encoded_content=str(self.encode_to_ucs2le(column_separator.join(map(str, result_list))))  +str(self.encode_to_ucs2le("\n"))
                fw.write(encoded_content)
            else:
                fw.write(column_separator.join(map(str, result_list))  + "\n")
        fw.close()
        if self.debug_mode: self._print_ ('JSON Flatten - write to file - Ends')