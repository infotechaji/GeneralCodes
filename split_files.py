"""
Functionality : splits the input based on the given numbers
Version : v1.1
History :
          v1.0 - 03/14/2019 - initial version 
          v1.1 - 03/14/2019 - splitting logic changed with Modulus Logic 
          
Pending :
Issues  : 
"""
import sys,os
import math

def write_into_file(file_name,file_lines,mode='w'):
    fp=open(file_name,mode)
    for each_line in file_lines:
        fp.write(each_line)
    fp.close()
def split_files(input_filename,split_lines_count='',no_of_files=2):
    input_filename=input_filename
    file_lines=open(input_filename).readlines()
    file_split=int(no_of_files)
    split_lines_count=split_lines_count
    splitted_file_names=[]
    if split_lines_count and file_split:
        print ("please specify any one !!")
    elif not split_lines_count and file_split:
        if int(len(file_lines))%file_split==0:
            split_lines_count=int(math.ceil(len(file_lines)/file_split))
        else:
            split_lines_count=int(math.ceil(len(file_lines)/file_split))+1
        #split_lines_count=int(math.ceil(len(file_lines)/file_split))+1
        print ("Calculated split_lines_count :",split_lines_count)
    elif split_lines_count and not file_split:
        pass
    loop_count=0
    temp_list=[]
    print ("len(file_lines) :",len(file_lines))
    no_of_files=0
    for i in range(len(file_lines)):
        loop_count+=1
        temp_list.append(file_lines[i])
        if (loop_count==split_lines_count) or (len(file_lines)-1==i):
            no_of_files+=1
            temp_file_name=input_filename.replace('.',str(no_of_files)+'.')
            #print "Splitted files :",temp_file_name
            write_into_file(file_name=temp_file_name,file_lines=temp_list)
            if temp_file_name not in splitted_file_names: splitted_file_names.append(temp_file_name)
            temp_list=[]
            loop_count=0
    return {'splitted_file_names':splitted_file_names}
    
if __name__=="__main__":
    input_filename=sys.argv[1]
    #file_lines=open(input_filename).readlines()
    file_split=int(sys.argv[2])
    #split_lines_count=''
    print (split_files(input_filename,no_of_files=file_split))
    