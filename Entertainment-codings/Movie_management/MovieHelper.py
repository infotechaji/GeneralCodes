from CustomisedFileOperation import  *
from Help_print import  *
import sys

def create_dummies(input_directory,add_extension = '.txt',developer_mode = False):
    dummy_dir = check_and_make_path(os.path.join(input_directory,'Dummies'))['directory']
    created = 0
    skipped = 0

    for root, dirs, files in os.walk(input_directory):
        total_files = 0
        for each_file in files:
            total_files+=1
            # if each_file.endswith(delete_extension):
            #     delete_files_count+=1

            temp1 = (each_file).split('.')[-1]
            raw_file = each_file.replace('.'+temp1,'').replace('.','_')
            developer_print('raw_file :',raw_file)
            temp_file_name='Movie_dummy_'+raw_file +add_extension
            if developer_mode:
                developer_print('Created file name :',temp_file_name)
            dummy_temp = os.path.join(dummy_dir,temp_file_name)
            if os.path.exists(dummy_temp):
                skipped+=0
            else:
                write_into_file(file_name = dummy_temp, contents = '.', mode='w')
                created+=1
        break
    return {
            'total_files':total_files
            ,'skipped':skipped
            ,'created':created
    }




if __name__ =='__main__':
    input_dir = sys.argv[1]
    create_dummies(input_directory = input_dir)


# if path.exists(file_to_be_deleted):
#     os.remove(file_to_be_deleted)