import sys,os

"""
File content added 
"""
def Get_files_list(input_directory,full_file_path=False):
    """

    :param input_directory:
    :return: Returns all the file_names in the directory
    """
    total_files = []
    for root, dirs, files in os.walk(input_directory):
        for each_file in files:
            if full_file_path:
                file_name = os.path.join(input_directory, each_file)
            else:
                file_name = each_file
            if file_name not in total_files:
                total_files.append(file_name)
        break  # to stop the depth of the loop
    return {
        'total_files': len(total_files),
        'file_names': total_files,
        'full_path': input_directory
    }
if __name__ == "__main__":
    input_directory = sys.argv[1]
    file_list = Get_files_list(input_directory)['file_names']
    write_content = False
    print(file_list)
    fp = open('Files_list.txt', mode='w')
    if write_content:
    	fp2 = open('error_content.txt', mode='w')
    for index,each_name in enumerate(file_list):
        print(index+1,each_name)
        # if each_name.lower().endswith('.sql'):
        #     each_name=each_name.strip('.sql')
        fp.write(str(each_name)+'\n')
        if write_content:
	        files_content = str(open(os.path.join(input_directory,each_name)).read()).replace('\r',' ').replace('\n',' ').replace('\t',' ')
	        c_content = str(each_name)+'\t'+str(files_content).strip()+'\n'
	        fp2.write(c_content)

	fp.close()
    if write_content:
    	fp2.close()
