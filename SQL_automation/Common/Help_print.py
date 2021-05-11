"""
Functionality :
Version :   v1.1
History :
            v1.0 - 05/10/2020 - initial version
            v1.1 - 07/10/2020 - function developer_print() is added to help the developer to know file name and function name
"""

from TimeStamp import *

import os,sys,time
import inspect
# import inspect
# inspect_list = inspect.stack() [0][3]
# inspect_list = inspect.stack()
# print('function name : ',inspect_list)
# for index, i in enumerate(inspect_list):
#     print(index,i)
#     print(type(i))
#     for j_index,j in enumerate(i) :
#         print(j_index,j)

# input('Help print ')
# #         break


def print_each_line(input_list):
    for index, i in enumerate(input_list):
        print(index, i)




def developer_print(*print_content_argv, developer_mode=False, time_stamp=False):
    # for i in print_content_argv:
    #     print(type(i), i)
    #
    # print ('list :',[str(i) for i in print_content_argv])
    inspect_list = inspect.stack()
    print_content = ' '.join([str(i).strip() for i in print_content_argv])
    to_print_list = []
    current_time_stamp = ''
    if time_stamp:
        current_time_stamp = str(get_time_stamp()['common_timestamp'])
        to_print_list.append(current_time_stamp)

    python_module_name = str(inspect_list[1][1]) #
    python_function_name = str(inspect_list[1][3]) #

    to_print_list.append(python_module_name)
    to_print_list.append(python_function_name)
    to_print_list.append(print_content)

    print(':\t'.join(to_print_list))