"""
Functionlaity : Script to merge Objects
Version       : v6.2
History       :
                v1.0 - 17/09/2020 - initial version
                v2.0 - 18/09/2020 - Logic updated to remove the repeated lines / extra lines with "?".
                v2.1 - 18/09/2020 - Functions get_extra_lines_removed(), get_similarity_percentage()
                v2.2 - 18/09/2020 - "Extra spaces" is handled in the CustomisedFileOperation file and calling functions and core logic is working fine for test-set1
                v2.3 - 21/09/2020 - In function ObjectMerge () , "if correct_list[-1] != result[index-1].strip('- '):" this condition is added to handle the similar line ignorance
                v2.4 - 21/09/2020 - Variable "is_block" is added to handle the new set of blocks, Strip() function is replaced by list comprehension functions as it is making some changes in the actual script
                v3.0 - 22/09/2020 - ID-1001 - Major logic change in file B addition/ ignorance  in object code ObjectMerge ()
                v3.1 - 22/09/2020 - ID-1002 - "end" and "empty lines" are handled in b file
                v3.2 - 22/09/2020 -         -  New pattern to detect the defect ID is added in the function File "CompareAndUpdate" function "get_all_fix_id()"
                v3.3 - 22/09/2020 - ID-1003 -  '(',')' are added to the exceptional cases to handle regularity
                v3.4 - 22/09/2020 - ID-1004 - spaces and tabs are handled in the function get_duplicates() and a new function added reduce_space()
                v3.5 - 28/09/2020 - Altering the procedure is not succeed with the functions() validate_sp(), get_alter_sp() may work in future
                v3.6 - 29/09/2020 - In function "ObjectMerge()" the logic to detect the block of new codes from A is upgraded.
                v3.7 - 30/09/2020 -  "ObjectMerge()" the logic to handle single words  are upgraded like begin, end , ) , (
                v3.8 - 30/09/2020 -  "Object_merge_config" is added to manage configuration effectively.
                v3.9 - 03/10/2020 -  Input for "GITAutomation.py" is prepared in the file 'GITAutomation_input.txt'
                v4.0 - 03/10/2020 -  Functions add_timestamp(),prepare_GITAutomation_input() are added to handle the input addition
                v4.1 - 03/10/2020 -  EPE-ID is added in the input pattern and the function "input_from_excel()" is updated to handle "epe-id"
                v4.2 - 03/10/2020 -  ID-1005 - {EPE-ID : along with sps } and {sps: along with defects-ids } are handled in input_from excel
                v4.3 - 05/10/2020 -            imported Help_print.py to add print options Major logic enhancement for adding/ignoring plus lines in result list - working version - some line are missing
                v4.4 - 06/10/2020 -            "defect_id_match" key is added to the list "lines_added_from_a"
                v4.5 - 06/10/2020 -            lines from a and b are both added in the result list , need to handle
                v4.6 - 07/10/2020 -            "is_block" logic enhancement in ObjectMerge() and developer_print() function is created and added
                v4.7 - 08/10/2020 -            New case is handled : "/*" and "*/" are ignored in detecting incorrect lines. So handled using similarity percentage.
                                                and also "ndiff" is added in getting the raw results and prev logic is commented.
                v4.8 - 09/10/2020 -            reduce_space () logic is improved
                v4.9 - 09/10/2020 -            Function "check_commented_sections()" is added but needs enhancement
                v4.9 - 10/10/2020 -            LINE_THRESHOLD is calculated using "LINE_THRESHOLD_PERCENTAGE" from the config file  and the leve is 15 %
                v5.0 - 12/10/2020 -            first match logic is upgraded in the function validate_plus_lines()
                v5.1 - 13/10/2020 -            unified_diff in files is added - Working version
                v5.2 - 14/10/2020 -            Test case -01 is passed for updated unified logic
                v5.3 - 14/10/2020 -            Minor upgrade in GIT Automation input generation and options to disable object merge operation is added
                v5.4 - 15/10/2020 -            File comparison logic is enhanced in the git_input_generation function
                v5.5 - 16/10/2020 -            Logic enhancement is done in prepare_GITAutomation_input() ,   logs file names are hard coded in Object merge conflict file
                v5.6 - 16/10/2020 -            prepare_GITAutomation_input() - Directory is handled to provide the results in respective directory
                v5.7 - 18/10/2020 -            Minor case handling is handled without the '--defects_file'
                v5.8 - 21/10/2020 -            functions get_patch_filename_to_deploy() and get_next_files() is added to handle the patch file deployment and tested successfully
                v5.9 - 28/10/2020 -            OBJECT_MERGE_FULL_LOG.txt - the defects are separated by commas.
                v6.0 - 29/10/2020 -  ID-1006   Consolidated defects list for an sp - is added as a separate file , modified functions get_input_excel_object_merge()
                v6.1 - 02/11/2020 -            Case sensitive defects fixes are handled here , and defects ids are added in the GIT Input files
                v6.2 - 13/11/2020 -            Login enhancement in finding start and end of blocks
Input:
                1. Directories contains updated procedures ( mandatory)
                2, Output directory which may contains the latest sp or the sps can be extracted from the Server by the script ( Either one should be given )
                3, Defect IDs ( optional)
Process      :  Do the match and updates
Output       :


Test Cases Results  :
Date	Passed	Not_passed	Total_test_cases	Success_percentage
08-10-20	10	4	14	71.43
09-10-20	9	2	11	81.82
10-10-20	14	3	17	82.35
10-10-20	13	3	16	81.25
12-10-20	15	1	16	93.75




Pending  items :
                1, A's block lines are missing in the result "wms_maintain_bin_exec_dtl_sp.sql"
                2, Capturing needs to be added for : --LLE-123 starts and also adding comma or brackets in the previous line of blocks
                3, Separate function to get the new patch file name may be added





Open issues :
Comments :

Future cases :
            1, API Service
            2, Web application 
"""
import difflib,sys
from difflib import Differ
from pprint import pprint

sys.path.insert(1, 'G:\\Ajith\\OtherFiles\\common')
from CompareAndUpdate import get_all_fix_id
from CustomisedFileOperation import *
from copy_folder import *
from TimeStamp import *
from Help_print import *
from Text_to_speech import * # speak_words(i)

from Object_merge_config import * # contains all the variable having upper cases
from HelpText_sp import *



import sys,re,os,argparse,filecmp
from datetime import datetime
import logging,math


logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p',filename='ObjectMerge.log')
# logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',filename='myapp.log', level=logging.INFO)

logging.warning('is when this event was logged: warning ')
logging.info('Finished :info')
logging.debug('This message should go to the log file :Debugging ')
logging.error('This message should go to the log file :error ')
logging.critical('This message should go to the log file :critical')


def get_similarity_percentage(text1, text2):
    similarity = difflib.SequenceMatcher(None, text1, text2).ratio()
    return int(similarity * 100)


def get_extra_lines_removed(input_list, to_ignore = '?', developer_mode = False):
    """

    :param input_list: List contains all the line differences
    :return:
    """
    new_list = []
    for i in input_list:
        if i.startswith(to_ignore):
            if developer_mode:
                print('get_extra_lines_removed:\teach_line started with condition satisifed :', i, 'each char match :',to_ignore)
            continue
        new_list.append(i)
        if developer_mode:
            print('get_extra_lines_removed:\t new_list ', new_list)
    return new_list

def is_commented_line(input_line):
    """

    :param input_line: takes any sql line as input
    :return: the commented line details like , is the input line is commented , types  and start / end
    """
    commented = False
    comment_type = None
    comment_started = False
    comment_ended = False

    if input_line.strip().startswith('--'):
        commented = True
        comment_type = 'single_line_comment'
    elif input_line.strip().startswith('/*') : # and input_line.strip().endswith('*/'): # for future cases added on 03/10/2020
        commented = True
        comment_type = 'multi_line_comment'
        comment_started = True
        # comment_ended = True # for future cases added on 03/10/2020

    if input_line.strip().endswith('*/'):
        commented = True
        comment_type = 'multi_line_comment'
        comment_ended = True

    return {
        'status' : commented,
        'comment_type' : comment_type,
        'comment_started' : comment_started,
        'comment_ended' : comment_ended,

    }

def are_commented_lines(line1,line2,developer_mode = False):
    lineA = line1.strip('\r\n\t ')
    lineB = line2.strip('\r\n\t ')
    if not is_commented_line(lineA) and not is_commented_line(lineB): # if the line A is commented and line B is not commented
        pass

def reduce_space(input_string,trim_characters =[],developer_mode = False, check_in_start = False,use_strip = True):
    """

    :param input_string: gets input along with spaces and tabs and
    :return:
    updated to handle single spaces tooo
    11/10/2020 - logic enhancement for
    """
    replace_with = ''
    if use_strip:
        input_string = input_string.strip()
    if developer_mode:
        developer_print('Before reducing spaces input_string :',input_string)
        developer_print('Before reducing spaces len(input_string) :',len(input_string))
    for ech_trm in trim_characters:
        if check_in_start:
            if input_string.startswith(ech_trm):
                # input_string = input_string.replace(ech_trm,replace_with)
                input_string = input_string.lstrip(ech_trm)
        else:
            input_string = input_string.replace(ech_trm,replace_with)
    temp_str=input_string.replace('\t',' ')
    # while '  ' in temp_str:
    emp_str = temp_str.replace('  ', ' ')
    while ' ' in temp_str:
        temp_str = temp_str.replace(' ','')
    if developer_mode:
        developer_print('After reducing spaces input_string :',temp_str)
        developer_print('After reducing spaces len(input_string) :',len(temp_str))

    return temp_str

def get_duplicates(current_line, input_list,is_block = False , defects_to_be_added = [], direct_match = True , developer_mode = False):
    """

    :param current_line: input line
    :param input_ist:  input list
    :return: returns True if the line is present inside given list
    """


    duplicate_presence = False
    current_line = reduce_space(current_line, trim_characters = ['- ','+ ','  ']) # ID - 1004
    if developer_mode:
        developer_print('current_line :',current_line)
        developer_print('ObjectMerge:\tget_duplicates:\t input_list :',input_list)
    for next_line in input_list:
        next_line = reduce_space(next_line, trim_characters = ['- ','+ ','  ']) # ID - 1004
        if direct_match:
            if developer_mode:
                developer_print('inside direct_match = True : ')
                developer_print('current_line : ',current_line)
                developer_print('next_line : ',next_line)
                developer_print('len(current_line) : ', len(current_line))
                developer_print('len(next_line) : ',len(next_line))
            if current_line.lower() == next_line.lower() :
                duplicate_presence = True
                break
            print('If condition not satisfied !')
        else:
            if current_line.lower() in next_line.lower():
                duplicate_presence = True
                break
    return duplicate_presence


def ObjectMerge(FilelinesA, FilelinesB, defects_to_be_added = [], developer_mode = False, strictly_add_from_B = True):
    """

    :param FilelinesA: Updated File with defect fixes
    :param FilelinesB: Destination file in which the defects are to be added.
    :param defects_to_be_added: Selective defects also can be added.
    :param developer_mode: Enables the print statement for the developers
    :return: Defects updated in File B.
    # """

    # developer_mode = True
    stop_after_line = 13769
    # stop_after_line = 1

    if developer_mode:
        developer_print('Filelines A :', len(FilelinesA), '\t Filelines B :', len(FilelinesB))

    SPL_SINGLE_WORD_CASES = ['end', '(', ')', 'begin', 'return', 'if']

    # d = Differ()
    # # d = Differ(linejunk = None , charjunk= ' ')
    FilelinesA_trimmed = [reduce_space(i,use_strip=False) for i in FilelinesA]
    FilelinesB_trimmed = [reduce_space(i,use_strip=False) for i in FilelinesB]

    # result_temp = list(d.compare(FilelinesA, FilelinesB))  # geting the differences from two files
    # result_temp = list(d.compare(FilelinesA_trimmed, FilelinesB_trimmed))  # geting the differences from two files

    result_temp = difflib.ndiff(FilelinesA,FilelinesB) # added on 08/10/2020 due to a suspect case

    # result_temp = difflib.ndiff(FilelinesA_trimmed,FilelinesB_trimmed) # added on 08/10/2020 due to a suspect case

    # '-' represents line missing in B
    # '+' represents lines missing in  A
    # '?' represents new lines and this case is ignored in this script

    correct_list = []
    lines_added_from_a = []
    is_block = False
    is_prev_line_added = False
    result = get_extra_lines_removed(result_temp)  # removing lines starts with "?" as it cause trouble by adding dummy lines
    write_into_file('Trans_view.sql', contents=''.join(result), mode='w')
    # get real line result_tmp
    # map the line exact line with dict and return it.

    for index, each_line in enumerate(result):

        # ID-1001 starts here
        if developer_mode:
            if stop_after_line and index >= stop_after_line:
                temp = input('Debugging option enabled : press Enter')
                if str(temp) == '0': stop_after_line = ''
            else:
                continue
        ids = get_all_fix_id(each_line)['valid_fixes']  # Extracting Defect Ids in the current line
        if developer_mode:
            developer_print('************************************************************************')
            developer_print(' Processing line  :', index, each_line.strip())
            developer_print(' is_block :', is_block)
            developer_print(' is_prev_line_added  :', is_prev_line_added)
            developer_print(' Extraced IDS from the line   :', ids)
            developer_print(' We are looking for defects id :', defects_to_be_added)


        if each_line.startswith('+ '):
            correct_list.append(each_line)  # adding all the plus lines_along with
            if developer_mode:
                developer_print(' Plus line : Hence added to the list directly :',each_line.strip())
        elif each_line.startswith('- ') and defects_to_be_added:  # so this is the new line to be added in File B
            if ids:  # if we found defect ID in the line then the decision to add/ignore will be done here
                id_dict = get_defect_id_presence(ids=ids, defects_to_be_added = defects_to_be_added)
                if id_dict['id_presence'] == True:
                    if developer_mode:
                        developer_print(' Minus line : Expected defect id is present in this line , Hence added ')
                    correct_list.append(each_line[2:])
                    # def check_for_undefined_start(result = result,index = index,matched_defect_id = id_dict )['status']:

                    if is_block == False:
                        start_res = check_for_block_start_and_end(each_line = each_line,developer_mode = developer_mode)
                        if start_res['start_comment_status'] and start_res['start_block_status']:
                            if developer_mode:
                                developer_print(' "block_status" is changed to "TRUE" ')
                            is_block = True
                        # elif start_res['start_comment_status']:
                        #     for temp_i in range(index+1,len(result)):
                        #         if reduce_space(result[temp_i]) and str(result[temp_i]).startswith('-'):
                        #             if developer_mode:
                        #                 developer_print('Suspecting block : Minus line presence')
                        #
                        #         else:
                        #             if temp_i!= index+1:
                        #                 if get_defect_id_presence(ids=get_all_fix_id(result[temp_i-1])['valid_fixes'], defects_to_be_added=defects_to_be_added)['id_presence']
                        #                     end_res = check_for_block_end(each_line=result[temp_i-1])
                        #                     is_block = end_res['status']
                        #                     comment_status = end_res['comment_status']
                        #                     if is_block==False or comment_status:
                        #                         if developer_mode:
                        #                             developer_print(' Based on suspecting : "block_status" is changed to "TRUE"')
                        #                         is_block = True

                    elif is_block == True:
                        end_res = check_for_block_start_and_end(each_line=each_line, developer_mode=developer_mode)
                        if end_res['end_comment_status'] and end_res['end_block_status']:
                            if developer_mode:
                                developer_print(' "block_status" is changed to "False" ')
                            is_block = False
                        # elif end_res['end_comment_status']:
                        #     if not str(result[index+1]).startswith('-'):
                        #         if developer_mode:
                        #             developer_print(' Based on suspecting : "block_status" is changed to "False" ')
                        #         is_block = False

                    if reduce_space(each_line[2:]):
                        lines_added_from_a.append({'lined_added':False,'line': [each_line[2:]],'defect_id_match': True,'is_block': is_block,'result_index': index,'hint': 'added with presence of defect id ( case : ids : matched in detected list '})


                elif is_block: # or is_prev_line_added:
                    if developer_mode:
                        developer_print(' Minus line : Defect id is not matched in the extracted defects list , but is_block is True, Hence added ')
                    correct_list.append(each_line[2:])
                    if reduce_space(each_line[2:]):
                        lines_added_from_a.append( {'lined_added':False, 'line': [each_line[2:]],'defect_id_match': False,'is_block': is_block,'result_index': index, 'hint' : 'added because of is_block : True ( case : ids = True , but not matched with list '})

            else:  # if we dont have any valid defect ID extracted from the current line
                if is_block:  # if the previous lines are added as a valid fix , then these lines also will be added=
                    if developer_mode:
                        developer_print(' Minus line : no defects are extracted from the line, but "is_block" = True , Hence added ')
                    correct_list.append(each_line[2:])
                    if reduce_space(each_line[2:]):
                        lines_added_from_a.append({'lined_added':False, 'line': [each_line[2:]], 'defect_id_match': False, 'is_block': is_block, 'result_index': index,'hint': 'added because of is_block : True ( case : ids = False  '})
        elif each_line.startswith('  '):
            if developer_mode:
                developer_print(' No sign line : Hence added')
            if is_block == True:
                if ids and defects_to_be_added:
                    if check_for_block_end(each_line=each_line[2:])['status'] == False and get_defect_id_presence(ids = ids , defects_to_be_added = defects_to_be_added)['id_presence'] == True:
                        is_block = False
            correct_list.append(each_line[2:])

        if developer_mode:
            developer_print(' End of the looping for line  :', each_line.strip())
            developer_print(' is_block status :', is_block)
            if len(correct_list) > 2:
                developer_print('correct_list[-3] :',correct_list[-3])
                developer_print('correct_list[-2] :',correct_list[-2])
                developer_print('correct_list[-1] :',correct_list[-1])
            developer_print('len(correct_list) :',len(correct_list))
            developer_print('************************************************************************')

            if stop_after_line and index >= stop_after_line:
                temp = input()
                if str(temp) == '0': stop_after_line = ''


    if developer_mode:
        developer_print('len(correct_list) :',len(correct_list))
        developer_print('len(lines_added_from_a) :',len(lines_added_from_a))


    correct_list = validate_plus_lines(correct_list = correct_list , lines_added_from_a = lines_added_from_a ,developer_mode = developer_mode )['correct_list']
    # developer_mode = False
    return {
        'updated_file_A': correct_list
    }


def check_for_block(each_line, input_list): # added on 05-10-2020
    # if char:
    #     return any([True if each_line.lower().startswith() else False for i in input_list])
    # else:
    return any([True if i in each_line.lower() else False for i in input_list])

def validate_plus_lines(correct_list , lines_added_from_a ,developer_mode = False):
    """

    :param correct_list: result list contains lines with "+ " which are added from file B
    :param lines_added_from_a: Lines which are detected and added from A are only in this list - Newly added lines
    :param developer_mode:
    :return: plus lines are handled in this list
    """
    prev_len = len(lines_added_from_a)
    # for i_index,eachh in enumerate(lines_added_from_a):
    #     print(i_index,eachh['result_index'], eachh['line'])
    # input()
    # developer_mode = True
    # stop_after_line = 1790

    # stop_after_line = 1

    LINE_THRESHOLD = int(len(correct_list) * LINE_THRESHOLD_PERCENTAGE)
    LINE_THRESHOLD_NEG = int(math.ceil(LINE_THRESHOLD/2)) #  code added on 11/10/2020 starts here


    if developer_mode:
        developer_print ('Lines added from A Total lines added from A Only  :',len(lines_added_from_a))
        developer_print ('Lines added from A Total lines added  len (correct list ):',len(correct_list))
        developer_print ('calculated  LINE_THRESHOLD     :',LINE_THRESHOLD)
        developer_print ('calculated  LINE_THRESHOLD_NEG :',LINE_THRESHOLD_NEG)




    # in case of debugging
    if developer_mode:
        write_into_file(file_name ='lines_added_from_a.txt',contents = '',mode='w')
        for i in lines_added_from_a:
            final_text = str(LINE_THRESHOLD)+'\t'+str(i['result_index']) + '\t' + str(i['is_block']) + '\t' + str(i['line'][0]).strip()+ '\t' + str(i['hint']).strip()+ '\n'
            write_into_file(file_name ='lines_added_from_a.txt',contents = final_text, mode='a')

    # if the line added in the new files , then jsut ignore it
    breaked = False

    is_block_block = False
    for index, each_line in enumerate(correct_list):
        if each_line.startswith('+ '):
            if developer_mode:
                developer_print('-----------------------------------------------------------------------------')
                developer_print('##### Processing line  :',index,each_line[2:].strip())
                if stop_after_line and index>= stop_after_line:
                    temp = input()
                    if str(temp) == '0': stop_after_line = ''

            current_line = each_line[2:]

            if lines_added_from_a and len(current_line.strip())>1:  # dictionary
                breaked = False
                for dic_index,each_dict in enumerate(lines_added_from_a):
                    breaked = False

                    looping_line = each_dict['line'][0]
                    # current_line_reduced = reduce_space(str(current_line).lower(), trim_characters =['--'],developer_mode = False, check_in_start = True)
                    # looping_line_reduced = reduce_space(str(looping_line).lower(), trim_characters =['--'],developer_mode = False, check_in_start = True)
                    current_line_reduced = reduce_space(str(current_line).lower())
                    looping_line_reduced = reduce_space(str(looping_line).lower())
                    current_line_reduced_trm = reduce_space(current_line_reduced, trim_characters =['--'],developer_mode = False, check_in_start = True)
                    looping_line_reduced_trm = reduce_space(looping_line_reduced, trim_characters =['--'],developer_mode = False, check_in_start = True)
                    if current_line_reduced_trm in looping_line_reduced_trm or looping_line_reduced_trm in current_line_reduced_trm:

                        # line_difference = index - int(each_dict['result_index'])
                        line_difference = int(each_dict['result_index']) - index
                        # code added on 11/10/2020 starts here
                        if line_difference <0:
                            line_threshold_temp = LINE_THRESHOLD_NEG
                        else:
                            line_threshold_temp = LINE_THRESHOLD
                        # code added on 11/10/2020 ends here
                        sim_percent = get_similarity_percentage(each_line, looping_line)

                    else:
                        if developer_mode: developer_print('Skipping in , first present in case !')
                        continue

                    if developer_mode:
                        developer_print('lopping line :',looping_line)
                        developer_print('line_difference :',line_difference)
                        developer_print('looping line index   :',each_dict['result_index'])
                        developer_print('each_dict :',each_dict)
                        developer_print('similarity % :',sim_percent)

                    # if the looping line comes under threshold
                    if abs(line_difference) <= line_threshold_temp:
                        pass
                    else:
                        if each_dict['result_index']< index:
                            if developer_mode:
                                developer_print('Considered as non required dict and deleting this for future cases :',each_dict)
                            lines_added_from_a.remove(each_dict) # added on 10/10/2020
                        if developer_mode: developer_print('Skipping due to line difference threshold criteria')
                        continue

                    com_section_match = check_commented_sections(current_line, looping_line, developer_mode=developer_mode)
                    # if reduce_space(str(current_line)) == reduce_space(str(looping_line)):  # previous
                    if current_line_reduced == looping_line_reduced:  # previous
                        if developer_mode:
                            developer_print(' Case 1 : Exact direct matching case , Hence  removing this line !!')
                        pass
                    elif com_section_match['status']: # if any one line commented the another one is not commented then b line will be ignored
                        if com_section_match['status'] == True:
                            if developer_mode: developer_print(' Case 2-A : commented line  and uncommented line  are matched  !')
                            pass
                        # added on 11/10/2020
                        elif com_section_match['status'] == 'not_matched':
                            if developer_mode: developer_print(' Case 2-B : commented line  and uncommented line  are not matched  !')
                            continue

                    elif sim_percent >SIMILARITY_THRESHOLD  and ( each_dict['defect_id_match'] == True or each_dict['is_block'] == True):
                        if developer_mode:
                            developer_print(' Case 3  ,present in matched,  fix id_presence / is_block is  true , Hence ignoring  !!')
                            developer_print(' each_dict[defect_id_match] :',each_dict['defect_id_match'])
                            developer_print(' each_dict[is_block] :',each_dict['is_block'])
                        pass
                    else:
                        if developer_mode:
                            # developer_print(' Exception case for plus line : ',current_line)
                            developer_print('No matching case: Skipping the looping line :',looping_line)
                            # lines_added_from_a.remove(each_dict) # added for processing only future cases on oct/8
                        continue
                    # if is_b_block: we need to add that line
                    correct_list[index] = ''
                    breaked = True
                    lines_added_from_a.remove(each_dict) # added on 10/10/2020
                    break

                if breaked == True:
                    if developer_mode:
                        developer_print(' Line status : Ignored ')
                    continue # breaking the for loop
                else: # cases to add
                    if developer_mode:
                        developer_print(' Line status : added')


                        # # if get_duplicates(current_line = current_line, input_list = correct_list[index-7:index], direct_match=True) == False:

                    # for future cases  - added on 06/10/2020
                    # try:
                    #     if current_line in correct_list[index-7:index-1]:
                    #         print('Line status : Added ( duplicate check passed ) ')
                    #         correct_list[index] = ''
                    # except Exception as e: pass
                    #
                    # else:
                    correct_list[index] = (each_line[2:])

            else: # cases to ignore
                if developer_mode:
                    developer_print(' Line status : Added from outer else : ',each_line[2:].strip())
                    developer_print('-----------------------------------------------------------------------------')
                correct_list[index] = (each_line[2:])
            if developer_mode:
                developer_print('Index : {0} : Line : {1} '.format(index,each_line[2:].strip()))
                if stop_after_line and index >= stop_after_line:
                    temp = input()
                    if str(temp) == '0': stop_after_line = ''
    developer_mode = False
    print(' Suspectful lines from File2  :',prev_len)
    print(' Added lines                  :',len(lines_added_from_a))
    print(' Ignored lines                :',abs(prev_len-len(lines_added_from_a)))
    return {
            'correct_list' :correct_list
            ,'lines_suspected':prev_len
            ,'lines_added':len(lines_added_from_a)
            ,'lines_ignored':abs(prev_len-len(lines_added_from_a))
            }

def validate_plus_lines_unified(correct_list , lines_added_from_a , index_dict ={} ,filelines_a =[], filelines_b =[],filelines_a_trimmed =[], filelines_b_trimmed =[],developer_mode = False):
    """

    :param correct_list: result list contains lines with "+ " which are added from file B
    :param lines_added_from_a: Lines which are detected and added from A are only in this list - Newly added lines
    :param developer_mode:
    :return: plus lines are handled in this list
    """
    prev_len = len(lines_added_from_a)
    # for i_index,eachh in enumerate(lines_added_from_a):
    #     print(i_index,eachh['result_index'], eachh['line'])
    # input()
    developer_mode = True
    stop_after_line = 1790

    # stop_after_line = 1

    # LINE_THRESHOLD = int(len(correct_list) * LINE_THRESHOLD_PERCENTAGE)
    # LINE_THRESHOLD_NEG = int(math.ceil(LINE_THRESHOLD/2)) #  code added on 11/10/2020 starts here

    # for updated logic
    LINE_THRESHOLD = len(correct_list)
    LINE_THRESHOLD_NEG = len(correct_list)


    if developer_mode:
        developer_print ('Lines added from A Total lines added from A Only  :',len(lines_added_from_a))
        developer_print ('Lines added from A Total lines added from A Only  :',lines_added_from_a)
        developer_print ('Lines added from A Total lines added  len (correct list ):',len(correct_list))
        developer_print ('Lines added from A Total lines added  len (correct list ):',correct_list)
        developer_print ('calculated  LINE_THRESHOLD     :',LINE_THRESHOLD)
        developer_print ('calculated  LINE_THRESHOLD_NEG :',LINE_THRESHOLD_NEG)
        input()




    # in case of debugging
    if developer_mode:
        write_into_file(file_name ='lines_added_from_a.txt',contents = '',mode='w')
        for i in lines_added_from_a:
            final_text = str(LINE_THRESHOLD)+'\t'+str(i['result_index']) + '\t' + str(i['is_block']) + '\t' + str(i['line'][0]).strip()+ '\t' + str(i['hint']).strip()+ '\n'
            write_into_file(file_name ='lines_added_from_a.txt',contents = final_text, mode='a')

    # if the line added in the new files , then jsut ignore it
    breaked = False

    is_block_block = False
    for index, each_line in enumerate(correct_list):
        # if each_line.startswith('+ '):
        if each_line.startswith('+'): # for updated logic 14/10/2020
            if developer_mode:
                developer_print('-----------------------------------------------------------------------------')
                developer_print('##### Processing line  :',index,each_line[2:].strip())
                if stop_after_line and index>= stop_after_line:
                    temp = input()
                    if str(temp) == '0': stop_after_line = ''

            # current_line = each_line[2:]
            current_line = each_line[1:] # updated logic 14/10/2020
            developer_print('index_dict :',index_dict)
            developer_print('current line  :',current_line )
            developer_print('filelines_b_trimmed[index_dict[start_index_b]-1] :',filelines_b_trimmed[index_dict['start_index_b']-1])
            if str(reduce_space(current_line)).strip() == str(filelines_b_trimmed[index_dict['start_index_b']-1]).strip():
                developer_print('Your new test case is matched ')
                correct_list[index] = ''
                correct_list.remove(each_line)
                continue

            # if True: continue
            if lines_added_from_a and len(current_line.strip())>1:  # dictionary
                breaked = False
                for dic_index,each_dict in enumerate(lines_added_from_a):
                    breaked = False

                    looping_line = each_dict['line'][0]
                    # current_line_reduced = reduce_space(str(current_line).lower(), trim_characters =['--'],developer_mode = False, check_in_start = True)
                    # looping_line_reduced = reduce_space(str(looping_line).lower(), trim_characters =['--'],developer_mode = False, check_in_start = True)
                    current_line_reduced = reduce_space(str(current_line).lower())
                    looping_line_reduced = reduce_space(str(looping_line).lower())
                    current_line_reduced_trm = reduce_space(current_line_reduced, trim_characters =['--'],developer_mode = False, check_in_start = True)
                    looping_line_reduced_trm = reduce_space(looping_line_reduced, trim_characters =['--'],developer_mode = False, check_in_start = True)
                    if current_line_reduced_trm in looping_line_reduced_trm or looping_line_reduced_trm in current_line_reduced_trm:

                        # line_difference = index - int(each_dict['result_index'])
                        line_difference = int(each_dict['result_index']) - index
                        # code added on 11/10/2020 starts here
                        if line_difference <0:
                            line_threshold_temp = LINE_THRESHOLD_NEG
                        else:
                            line_threshold_temp = LINE_THRESHOLD
                        # code added on 11/10/2020 ends here
                        sim_percent = get_similarity_percentage(each_line, looping_line)

                    else:
                        if developer_mode: developer_print('Skipping in , first present in case !')
                        continue

                    if developer_mode:
                        developer_print('lopping line :',looping_line)
                        developer_print('line_difference :',line_difference)
                        developer_print('looping line index   :',each_dict['result_index'])
                        developer_print('each_dict :',each_dict)
                        developer_print('similarity % :',sim_percent)

                    # if the looping line comes under threshold
                    if abs(line_difference) <= line_threshold_temp:
                        pass
                    else:
                        if each_dict['result_index']< index:
                            if developer_mode:
                                developer_print('Considered as non required dict and deleting this for future cases :',each_dict)
                            lines_added_from_a.remove(each_dict) # added on 10/10/2020
                        if developer_mode: developer_print('Skipping due to line difference threshold criteria')
                        continue

                    com_section_match = check_commented_sections(current_line, looping_line, developer_mode=developer_mode)
                    # if reduce_space(str(current_line)) == reduce_space(str(looping_line)):  # previous
                    if current_line_reduced == looping_line_reduced:  # previous
                        if developer_mode:
                            developer_print(' Case 1 : Exact direct matching case , Hence  removing this line !!')
                        pass
                    elif com_section_match['status']: # if any one line commented the another one is not commented then b line will be ignored
                        if com_section_match['status'] == True:
                            if developer_mode: developer_print(' Case 2-A : commented line  and uncommented line  are matched  !')
                            pass
                        # added on 11/10/2020
                        elif com_section_match['status'] == 'not_matched':
                            if developer_mode: developer_print(' Case 2-B : commented line  and uncommented line  are not matched  !')
                            continue

                    elif sim_percent >SIMILARITY_THRESHOLD  and ( each_dict['defect_id_match'] == True or each_dict['is_block'] == True):
                        if developer_mode:
                            developer_print(' Case 3  ,present in matched,  fix id_presence / is_block is  true , Hence ignoring  !!')
                            developer_print(' each_dict[defect_id_match] :',each_dict['defect_id_match'])
                            developer_print(' each_dict[is_block] :',each_dict['is_block'])
                        pass
                    else:
                        if developer_mode:
                            # developer_print(' Exception case for plus line : ',current_line)
                            developer_print('No matching case: Skipping the looping line :',looping_line)
                            # lines_added_from_a.remove(each_dict) # added for processing only future cases on oct/8
                        continue
                    # if is_b_block: we need to add that line
                    correct_list[index] = ''
                    breaked = True
                    lines_added_from_a.remove(each_dict) # added on 10/10/2020
                    break

                if breaked == True:
                    if developer_mode:
                        developer_print(' Line status : Ignored ')
                    continue # breaking the for loop
                else: # cases to add
                    if developer_mode:
                        developer_print(' Line status : added')


                        # # if get_duplicates(current_line = current_line, input_list = correct_list[index-7:index], direct_match=True) == False:

                    # for future cases  - added on 06/10/2020
                    # try:
                    #     if current_line in correct_list[index-7:index-1]:
                    #         print('Line status : Added ( duplicate check passed ) ')
                    #         correct_list[index] = ''
                    # except Exception as e: pass
                    #
                    # else:
                    correct_list[index] = (current_line)
            elif reduce_space(current_line) == filelines_b_trimmed[index_dict['start_index_b']-1]:
                developer_print('Your new test case is matched ')
                correct_list[index] = ''
                pass
            else: # cases to ignore
                if developer_mode:
                    developer_print(' Line status : Added from outer else : ',current_line.strip())
                    developer_print('-----------------------------------------------------------------------------')
                correct_list[index] = (current_line)
            if developer_mode:
                developer_print('Index : {0} : Line : {1} '.format(index,current_line.strip()))
                if stop_after_line and index >= stop_after_line:
                    temp = input()
                    if str(temp) == '0': stop_after_line = ''
    developer_mode = False
    # print(' Suspectful lines from File2  :',prev_len)
    # print(' Added lines                  :',len(lines_added_from_a))
    # print(' Ignored lines                :',abs(prev_len-len(lines_added_from_a)))
    return {
            'correct_list' :correct_list
            ,'lines_suspected':prev_len
            ,'lines_added':len(lines_added_from_a)
            ,'lines_ignored':abs(prev_len-len(lines_added_from_a))
            }


def get_alter_sp(input_text,developer_mode = False):
    file_lines = ''

    if type(input_text) == list:
        file_lines = '\n'.join(input_text)
    if type(input_text) == str:
        file_lines = input_text
    else:
        print('ObjectMerge\t:get_alter_sp\t: Acceptable input formats , List and string ')
        return  False
    alter_command = ''
    # Logic 1
    # alter_command = re.sub('create\s+procedure', ' alter procedure ', file_lines.rstrip(), 1, re.I)
    # print ('alter command :',alter_command)
    # input()
    splitss = re.split('create\s+procedure', str(file_lines), re.I)
    try:
        alter_command = 'alter procedure '+str(splitss[1])
        print('Prepared alter command :',alter_command)

    except Exception as e:
        print('ObjectMerge:\tget_alter_sp:\t Error while splitting the procedure using "create procedure" :',e)

    print('alter section :',alter_command[:100])
    input()

    return  {'alter_command' : alter_command}



def validate_sp(directory,sp_list,db_details = {},developer_mode = False):
    """

    :param sp_list: List contains all the procedures needs to be altered
    :param db_details: Server and database to connect
    :param developer_mode: works for developer mode
    :return: Success / Failed lists
    """
    alter_db_details = db_details.copy()

    # CONNECTION_STRING = get_connection_string(db_details = db_details)
    # cursor = connect(get_connection_string(db_details = db_details)) # Ehnancement # future cases
    # help_text = get_sptext(each_sp, cursor)['help_text']
    # print('validate_sp:\t help text is extracted !', help_text)
    # defect_ids = []
    # defect_ids_temp = get_all_defect_ids(help_text)
    # defcts_ids.append()
    #
    alter_db_details['database'] = 'ScmdbTesting'
    alter_cursor = connect(get_connection_string(db_details = alter_db_details))

    validation_failed = validation_success =  ACCEPTABLE_ERRORS = []

    for each_sp in sp_list:
        if not each_sp.lower().endswith('.sql'):
            each_sp+='.sql'
        sp_text = get_file_content(filename = os.path.join(directory,each_sp),return_lines = False)
        print('validate_sp:\t sp content !',sp_text[:10])
        alter_command = get_alter_sp(sp_text,developer_mode = developer_mode)['alter_command']
        print('validate_sp:\t altered content  !', alter_command[:100])
        input()
        try:
            print('Executing alter command..........')
            alter_cursor.execute(alter_command)
            for row in alter_cursor.fetchall():
                print ('Results :',row)
                # full_text += str(row[0]).replace('\r\n', '\n')
                # print()
            validation_success.append(each_sp)
        except Exception as error_message:
            error_message = str(error_message)
            print('Error while getting procedure text :', error_message)
            validation_failed.append(each_sp)
            # if error_message.lower() in ACCEPTABLE_ERRORS:

            #



    # return {
    #         'validation_success' : validation_success,
    #         'validation_failed'  : validation_failed,
    #         'defect_ids'  : defect_ids
    #
    #         }

def Get_files_list(input_directory,defects_file = {}):
    """

    :param input_directory:
    :return: Returns all the file_names in the directory
    """
    source = 'file_path'
    total_files = []
    for root, dirs, files in os.walk(input_directory):
        for each_file in files:
            file_name = os.path.join(input_directory, each_file)
            if file_name not in total_files: total_files.append(each_file)
        break  # to stop the depth of the loop
    if not total_files and defects_file:
        source = 'defects_file'
        for e in defects_file:
            if e not in total_files :total_files.append(e)

    return {
        'total_files': len(total_files)
        ,'file_names': total_files
        ,'full_path': input_directory
        ,'source': source
    }


def Get_helptext_from_server(SERVER_DETAILS, SP_LIST, DIRECTORY, developer_mode=False , strict_mode = False):
    """

    :param SERVER_DETAILS: Server credentials to connect and extract help text
    :param SP_LIST: list of procedure names which descriptions are to be extracted
    :param DIRECTORY: In which the procedures needs to be stored
    :return: Directory , Extraction status , no_of_success, no_of_failures
    """
    # developer_mode = True
    file_directory = DIRECTORY
    if not os.path.exists(file_directory): os.mkdir(file_directory)
    # connecting the required DB.
    CONNECTION_STRING = get_connection_string(SERVER_DETAILS)
    if developer_mode:
        developer_print(' CONNECTION_STRING:', CONNECTION_STRING)
        developer_print(' SP LIST:', SP_LIST)
        developer_print(' len( SP LIST) :', len(SP_LIST))
    cursor = connect(CONNECTION_STRING)  # connects to the server
    # file_lines = get_file_content(args.input_file)
    succeed = []
    errored = []
    skipped = []

    for index, each_line in enumerate(SP_LIST):
        each_line = each_line.strip('\t\r\n')
        file_name = get_file_name(each_line)
        if file_directory:
            file_name = os.path.join(file_directory, file_name)
        if developer_mode:
            developer_print('Before checking locally the file name :',file_name)
        if not strict_mode:
            try:
                if os.path.exists(file_name) and len(get_file_content(filename=  file_name,return_lines=True))>1:
                    developer_print('Skipping help text ',each_line,' due to its presence in "',str(file_directory).split(os.sep)[-1],'"')
                    skipped.append(each_line)
                    continue
            except Exception as e:
                developer_print('Error while looking for the file :',each_line)
                pass
        if developer_mode:
            developer_print('Extracting procedure :\t', index + 1, each_line)

        help_text = str(get_sptext(each_line, cursor)['help_text'])
        if help_text:
            if developer_mode:
                developer_print(' Writing into the file :\t', file_name)
            try:
                write_into_file(file_name = file_name, contents = help_text, mode = 'w')
                succeed.append(file_name)
            except Exception as e:
                developer_print('Error while writing the help text :',e)
                write_into_file(file_name=file_name, contents=str(help_text), mode='w')
                errored.append(file_name)
                # write_into_file(file_name=file_name, contents=help_text.encode('utf-8'), mode='w')

    if developer_mode:
        developer_print('Extraction is completed \nSuccess : {0}\nFailed  : {1}'.format(len(succeed),len(errored)))

    return {
        'success': succeed
        ,'errored': errored
        ,'skipped': skipped

    }


def get_dict_from_filelines(file_lines, developer_mode=False):
    sp_list = []
    for each_line in file_lines:
        sp = each_line.split(os.sep)[-1]
        if sp.lower().endswith('.sql'): sp = sp.lower().split('.sql')[0]
        sp_list.append({'sp_name': sp, 'defect_ids': [], 'epe_id' : []})
    if developer_mode:
        print('get_dict_from_filelines:\t Input dictionary prepared from files }'.format(len(sp_list)))
    return sp_list


def get_input_text(input_text_file, developer_mode=False):
    file_lines = get_file_content(input_text_file)
    rows = len(file_lines)
    cols = len(file_lines[0].strip('\t\r\n').split('\t'))
    if developer_mode:
        print('get_input_text:\tSheet Name :{0}\tRows:{1}\tColumns:{2}'.format(input_text_file, rows, cols))
    sp_list = []
    if cols == 2:
        for each_line in file_lines:
            splits = each_line.strip('\t\r\n').split('\t')
            sp = splits[0]
            try:
                defects = (splits[1]).split(',')
            except:
                defects = []
            if developer_mode:
                sys.stdout.write('get_input_text:\t Reading row ..... SP..' + str(sp) + ',Defects : ' + str(defects))
                sys.stdout.write('\r')
            if sp.lower().endswith('.sql'): sp = sp.split('.sql')[0]
            sp_list.append({'sp_name': sp, 'defect_ids': defects})

    return {
        'rows': rows,
        'cols': cols,
        'sp_list': sp_list
    }


def get_input_excel_object_merge(excel_file_name, developer_mode=False):
    """
     
     :param excel_file_name: name of the uploaded excel file  
     :return: names along with the defect IDS
     """
    excel_dict = get_input_excel(excel_file_name = excel_file_name, developer_mode=developer_mode)
    input_data = excel_dict['excel_data']
    rows = excel_dict['rows']
    cols = excel_dict['cols']
    sp_list = []
    for index,temp_line in enumerate(input_data):
        each_line = temp_line[0]
        if index == 0:
            print('Ignoring headers from input file ....',each_line)
            continue
        # print('Line : {0} each_line : {1} '.format(index, each_line))
        sp_names = check_suspects(each_line[1])['result']
        defects = check_suspects(str(each_line[0]).upper())['result'] # making the defects id upper ()
        epe_ids = check_suspects(str(each_line[2]).upper())['result'] # making the EPE id upper ()
        # print('sp_names :', sp_names)
        # print('defects :', defects)
        # print('epe_ids :', epe_ids)
        for each_epe_id in epe_ids:
            for each_sp in sp_names:
                sp_list.append({'sp_name': each_sp.strip(), 'defect_ids': defects, 'epe_ids' :str(each_epe_id).upper()})
                # sample result  : {'sp_name': 'WMA_Stkarl_Sp_Tacbtn_SklspO', 'defect_ids': ['VLVI-412'], 'epe_ids': 'EPE-24270'}
        # print('sp_list :',sp_list)
        # input('Testing.... proceed ?')

    if developer_mode:
        developer_print('sp_list before modification len(sp_list):',len(sp_list))
        developer_print('sp_list before modification sp_list[-1]:',sp_list[-1])

    sp_defect_dict = {}
    # epe_dict
    epe_dict = {}
    for each_dict in sp_list:
        if each_dict['epe_ids'] not in epe_dict.keys():
            epe_dict[each_dict['epe_ids']] =[]
        epe_dict[each_dict['epe_ids']] = merge_list(epe_dict[each_dict['epe_ids']], [each_dict['sp_name']])

        # sp_defect_dict
        if each_dict['sp_name'] not in sp_defect_dict.keys():
            sp_defect_dict[each_dict['sp_name']] ={'defects':[],'epe_id':each_dict['epe_ids']} # #ID-1006 updated due to the consolodated list
        if developer_mode:
            developer_print('sp_defect_dict[each_dict[sp_name][defects]] :',sp_defect_dict[each_dict['sp_name']]['defects'])
        sp_defect_dict[each_dict['sp_name']]['defects'] = merge_list(sp_defect_dict[each_dict['sp_name']]['defects'],each_dict['defect_ids']) # #ID-1006 updated due to the consolodated list

        # sp_defect_dict[each_dict['sp_name']].append(defects)
    # print('sp_defect_ids :',sp_defect_dict)
    if developer_mode:
        for i in sp_defect_dict:
            print(i," : ",sp_defect_dict[i])
        input()
    return {
        'rows': rows
        ,'cols': cols
        ,'sp_list': sp_list # single lines
        ,'sp_and_defects': sp_defect_dict # {sp1 : [defect1,defect2] , sp2 : [defect1,defect2]} #ID-1005
        ,'epe_id_and_sps': epe_dict #  # {epe_id1 : [sp1,sp2] , epe_id2 : [sp1,sp2] }   #ID-1005
    }

def merge_list(list_1,list_2,developer_mode = False):
    if developer_mode:
        developer_print('Input list_1 :',list_1)
        developer_print(' Input list_2 :',list_2)
    list_2_items_not_in_list_1 = list(set(list_2) - set(list_1))
    if developer_mode:
        developer_print('  list_2_items_not_in_list_1 :',list_2_items_not_in_list_1)
    combined_list = list_1 + list_2_items_not_in_list_1
    if developer_mode:
        developer_print('  combined_list :',combined_list)
        input()
    return combined_list

# def prepare_GITAutomation_input(epe_id,directory,files_list,developer_mode =False,git_input_file = ''):
def prepare_GITAutomation_input(epe_id_dict,directory,developer_mode = False,git_input_file = '',sp_and_defects = []):
    DIRECTORY =''
    if git_input_file:
        t_dic = handle_extension(git_input_file)
        temp_file_name = str(t_dic['no_extension']) + '_GITAutomation_input.txt'
        DIRECTORY = t_dic['directory']
        git_input_file = temp_file_name
    else:
        git_input_file = GIT_AUTOMATION_DEFAULT_INPUT
    if not DIRECTORY:DIRECTORY = os.getcwd()
    git_input_file = os.path.join(DIRECTORY, git_input_file)

    modifed_dir = directory
    extracted_dir = directory.replace(os.sep + 'modified', '')
    source_dir = extracted_dir.replace(os.sep + 'Extracted_objects', '')

    git_headers ='TOTAL_OBJECTS \t EPE_ID \t DIRECTORY \t OBJECTS \t DEFECTS_IDS\n'
    write_into_file(file_name=git_input_file, contents=git_headers, mode = 'w')
    processed_sps =[] # added to handle / ignore the duplication of handled objects
    process_log_list =[]
    # defects_to_be_added = sp_and_defects[each_dict]['defects']
    for each_dict in epe_id_dict:
        epe_id = each_dict
        files_list = epe_id_dict[each_dict]
        files_to_deploy =[]
        file_status = []
        defects_total_list = []
        for each_file in files_list:
            # if not str(each_file).lower().endswith('.sql'): each_file+='.sql'
            # if it is a patch file
            #  then just find the latest id of mandatory patches and produce the next name of patch file
            #     rename the current patch file and copy it in mandatory patches path
            epe_id_dir = os.path.join(directory, epe_id)
            handle_dict = handle_extension(each_file)
            each_file = handle_dict['new_extension']
            sp_name = handle_dict['no_extension']
            try:
                defects_list = sp_and_defects[sp_name]['defects']
            except:
                defects_list =[]

            if get_all_fix_id(file_content=each_file, extract_from_header=False, developer_mode=False)['valid_fixes']: # patch file is handled here
                developer_print('Detected as patch file :', each_file)
                if os.path.exists(os.path.join(source_dir,each_file)):
                    copy_file(src=source_dir, dst=epe_id_dir, files_list=[each_file],developer_mode=developer_mode)  # copies the selected files
                    if developer_mode:
                        developer_print('Patch File copied ',os.path.join(epe_id_dir,each_file))

                if os.path.exists(os.path.join(epe_id_dir,each_file)):
                    src = os.path.join(epe_id_dir,each_file)
                    new_patch_file_name  = handle_extension(get_patch_filename_to_deploy(epe_id=epe_id,patch_folder=GIT_DEPLOYMENT_MANDATORY_PATCH_PATH,developer_mode = developer_mode)['new_patch_filename'])['new_extension']

                    dst = os.path.join(epe_id_dir,new_patch_file_name)
                    try:
                        os.rename(src, dst)
                    except Exception as e:
                        developer_print('error while renaming the patch file :',e)
                        pass
                    if developer_mode:
                        developer_print('Patch File renamed ',new_patch_file_name)
                    files_to_deploy.append(new_patch_file_name)
                    defects_total_list.append(';'.join(defects_list))
                    file_status.append({'file_name': new_patch_file_name, 'reason': 'copied', 'status': 'success', 'comments': ''})
                continue
                # patch file is handled here


            # added to ignore the already processed sps added on 16/10/2020
            if str(each_file).lower() in processed_sps:
                if developer_mode: developer_print('Ignoring the sp as processed earlier ')
                file_status.append({'file_name':each_file , 'reason':'already_processed' ,'status':'skipped','comments':''})
                continue
            else:
                processed_sps.append(str(each_file).lower())
            # added to ignore the already processed sps added on 16/10/2020

            try:
                mod_file = os.path.join(modifed_dir,each_file)
                extr_file = os.path.join(extracted_dir,each_file)
                if filecmp.cmp(mod_file,extr_file)==True: # checking
                    if developer_mode: developer_print('Extracted file and modified file are same : No change , hence ignoring !')
                    file_status.append({'file_name':each_file , 'reason':'no_change','status':'skipped','comments':''})
                    continue

                else:
                    copy_file(src=modifed_dir, dst=epe_id_dir, files_list=[each_file],developer_mode = developer_mode)  # copies the selected files
                    files_to_deploy.append(each_file)
                    defects_total_list.append(';'.join(defects_list))
                    file_status.append({'file_name': each_file, 'reason': 'copied','status':'success','comments':''})
            except Exception as e:
                # print('Error :\t ObjectMerge : \t prepare_GITAutomation_input :  Error :{0} , line : {1}'.format(e,each_file))
                # print('Skipping file .... :',each_file)
                file_status.append({'file_name': each_file, 'reason': 'errored','status':'skipped' ,'comments' : str(e)})
                continue
        if os.path.exists(epe_id_dir) and len(files_to_deploy)>0:
            final_text = str(len(files_to_deploy)) + '\t'
            final_text += str(epe_id) + '\t' + str(epe_id_dir) + '\t' +str(','.join(files_to_deploy))+ '\t' +str(','.join(defects_total_list))
            final_text += '\n'
            write_into_file(file_name = git_input_file, contents=final_text, mode='a')
            write_into_file(file_name = OBJECT_MERGE_GIT_INPUT_LOG, contents = add_timestamp(final_text), mode='a') # general file content backups
        for fil_ind,fil_status in enumerate(file_status):
            each_file_status = [epe_id,len(files_to_deploy),fil_ind+1,fil_status['file_name'],fil_status['status'],fil_status['reason'],fil_status['comments']]
            text_to_write = '\t'.join(apply_to_list(each_file_status,make_string= True))
            write_into_file(file_name = OBJECT_MERGE_DEEP_SP_LOG,contents=add_timestamp(text_to_write),mode='a')  # general file content backups

        process_log_list.append({'epe_id':epe_id
                                ,'files_list':files_list
                                ,'file_status':file_status
                                ,'files_to_deploy':files_to_deploy
                                }
                                )


    return {
            'git_input_file': git_input_file
            ,'git_log_file': OBJECT_MERGE_GIT_INPUT_LOG
            ,'processed_sps': processed_sps
            ,'process_log_list': process_log_list
    }

def add_timestamp(input_text):
    return str(get_time_stamp()['common_timestamp'])+'\t'+input_text.strip('\t\r\n') + '\n'

def check_for_block_start_and_end(each_line, developer_mode=False): # added on 7/10/2020
    start_comment_status = check_for_block(each_line, START_BLOCK_CHARS)
    start_block_status = check_for_block(each_line, START_BLOCK_WORDS)
    end_comment_status = check_for_block(each_line, END_BLOCK_CHARS)
    end_block_status = check_for_block(each_line, END_BLOCK_WORDS)

    # if comment_status == True and start_block_status == True:
    #     status = True
    return {
            'start_comment_status': start_comment_status
            ,'start_block_status': start_block_status
            , 'end_comment_status': end_comment_status
            , 'end_block_status': end_block_status
    }


def check_for_block_end(each_line, developer_mode=False): # added on 7/10/2020
    status = True

    comment_status = check_for_block(each_line, END_BLOCK_CHARS)
    end_block_status = check_for_block(each_line, END_BLOCK_WORDS)

    if comment_status == True and end_block_status == True:
        status = False
    return {
        'status': status
        ,'comment_status': comment_status
        ,'block_status': end_block_status
    }

def get_defect_id_presence(ids , defects_to_be_added ,developer_mode = False): # added on 7/10/2020
    """
    :param ids:
    :param defects_to_be_added:
    :param developer_mode:
    :return: True if the ids gets matched
    """
    id_presence = False
    matched_id = 0
    if ids:  # if we found defect ID in the line then the decision to add/ignore will be done here
        for each_id in ids:
            if str(each_id).upper() in defects_to_be_added:
                id_presence = True
                matched_id = str(each_id).upper()
                break
    return  {
            'id_presence' : id_presence
            ,'matched_id' : matched_id

    }


def get_matches_advanced(uncommented_line, commented_line): # added on 9/10/2020  to return the matches
    tmp_uncommented_line = uncommented_line
    try:uncommented_line = uncommented_line.split('--')[1]
    except: uncommented_line = tmp_uncommented_line
    if type(commented_line)!=list: commented_line = commented_line.split('--')
    matches = difflib.get_close_matches(uncommented_line, commented_line)
    return {'matches': matches}

def check_commented_sections(current_line, looping_line , developer_mode =False):
    status = False
    commented_line = ''
    uncommented_line = ''
    current_line= current_line.strip()
    looping_line= looping_line.strip()
    if developer_mode:
        developer_print('Raw input : current_line :', current_line)
        developer_print('Raw input : looping_line :', looping_line)
    if current_line.strip().startswith('--') and not looping_line.strip().startswith('--'):  # A is commented and B is not commented
        if developer_mode:developer_print('if case : 01 : current line is Commented')
        commented_line = current_line
        uncommented_line = looping_line.strip('--').split('--')[0]
    elif not current_line.strip().startswith('--') and looping_line.strip().startswith('--'):  # A is not commented . B is commented
        if developer_mode: developer_print('if case : 02 : looping line is Commented')
        commented_line = looping_line
        uncommented_line = current_line.strip('--').split('--')[0]
    elif current_line.strip().startswith('--') and looping_line.strip().startswith('--'):  # A is not commented . B is commented
        if developer_mode: developer_print('if case : 03 : both lines are Commented')
        commented_line = looping_line.strip('--')
        uncommented_line = current_line.strip('--').split('--')[0]
    elif not current_line.strip().startswith('--') and not looping_line.strip().startswith('--'):  # Commented on 11/10/2020
        if developer_mode:developer_print('if case : 04 : both lines are not Commented')
        commented_line = looping_line.strip()
        uncommented_line = current_line.strip('--').split('--')[0]

    if developer_mode:
        developer_print('commented_line :', commented_line)
        developer_print('uncommented_line :', uncommented_line)
        developer_print('commented_line splits :', commented_line.split('--'))
        developer_print('Matching (uncommented_line,commented_line:',difflib.get_close_matches(uncommented_line, commented_line.split('--')))
        developer_print('Matching (commented_line,uncommented_line :',difflib.get_close_matches(commented_line, uncommented_line.split('--')))

    if len(commented_line)>1 and len(uncommented_line)>1:
        # diffs = difflib.get_close_matches(uncommented_line,commented_line.split('--'))
        diffs = get_matches_advanced(uncommented_line, commented_line.split('--'))['matches']
        if developer_mode:
            developer_print(' len(diffs) :', len(diffs))
            developer_print(' diffs :', diffs)
        # input('New condition should be defined here !!')
        if len(diffs) == 1:
            status = True
            # if reduce_space(uncommented_line)==diffs[0]: # commented  to get better results
            #     if developer_mode: developer_print('diff length = 1 , Hence ignoring this line ')
            #     status = True
            # else:
            #     status = 'not_matched' # added for spl cases on 11/10/20202
        else:
            if developer_mode: developer_print('diff length > 1 , Hence continuing the loop. diffs :', diffs)

    else:
        if developer_mode: developer_print('Commented line / uncommented line are not detected from the lines  !')
    # print('check_commented_sections : commented section status :',status)
    # input()
    return {'status': status}


def prepare_input_from_defects_file(defects_file, developer_mode=False): # added on 10/10/2020
    epe_id_and_sps = []
    sp_and_defects = []
    source_file = None
    if defects_file:
        if defects_file.lower().endswith('.xlsx'):
            developer_print('\n Input file type :\t Excel')
            result_dict = get_input_excel_object_merge(defects_file, developer_mode=developer_mode)
            epe_id_and_sps = result_dict['epe_id_and_sps']  #
            sp_and_defects = result_dict['sp_and_defects']  # sp_and_defects
            source_file = 'excel'
        elif defects_file.lower().endswith('.txt'):
            developer_print('\nInput file type :\t Text')
            sp_and_defects = get_input_text(defects_file, developer_mode=developer_mode)['sp_list']
            source_file = 'text'
        else:
            developer_print('Input file type :\t Undefined')
            developer_print('Please upload a valid input file ! \n Accepted formats :\n 1.\tExcel \n2.\t Text')
    else:
        developer_print('Defects file is not given ')
    return {
        'sp_and_defects': sp_and_defects
        , 'epe_id_and_sps': epe_id_and_sps
        , 'source_file': source_file
    }


def get_updated_file_b(file_lines_b,file_lines_a, file_lines_a_trimmed, file_lines_b_trimmed, updated_b_fixes=[],developer_mode = False): # added on 13/10/2020 for new logic
    temp_file_lines_b = file_lines_b
    temp_file_lines_a = file_lines_a

    if developer_mode:
        developer_print('len(file_lines):', len(temp_file_lines_b))
    for each_dict in updated_b_fixes:
        if developer_mode:
            developer_print('Each dict :',each_dict['content'])

        start_index_a = each_dict['start_index_a']
        stop_index_a = each_dict['stop_index_a']
        start_index_b = each_dict['start_index_b']
        stop_index_b = each_dict['stop_index_b']
        content = each_dict['content']

        if stop_index_a == 0 and stop_index_b>0:
            if developer_mode:
                developer_print('Block of lines are present in B only ')
        elif stop_index_b == 0 and stop_index_a>0:
            if developer_mode:
                developer_print('Block of lines are present in A only ')

        elif stop_index_a>0 and stop_index_b>0:
            if developer_mode:
                developer_print('No  blocks are detected ')


        try:
            if developer_mode:
                developer_print('temp_file_lines_a[start_index_a+stop_index_a-1] :',temp_file_lines_a[start_index_a+stop_index_a-1])
                developer_print('temp_file_lines_b[start_index_b] :',temp_file_lines_b[start_index_b])
                developer_print('start_index_a :',start_index_a)
                developer_print('stop_index_a :',stop_index_a)
                developer_print('start_index_b :', start_index_b)
                developer_print('stop_index_b :', stop_index_b)
                # input()
            if file_lines_a_trimmed[start_index_a+stop_index_a-1] == file_lines_b_trimmed[start_index_b]:
                # if content and reduce_space(content[-1])!= file_lines_b_trimmed[start_index_b]:
                    content.append(temp_file_lines_b[start_index_b])
        except Exception as e:
            print('Error while cross checking before updating ...',e)
            pass

        # elif temp_file_lines_a[start_index_a+start_index_a] == temp_file_lines_b[start_index_b]:
        # test_list.insert(0, 6)# we can insert the values at the front here

        content_txt = ''.join(content)
        temp_file_lines_b[start_index_b] = content_txt
        # status = each_dict['status']

        # making the indexes null

        if start_index_b > (start_index_b+stop_index_b):
            for i in range(start_index_b, start_index_b+stop_index_b):
                if developer_mode:
                    developer_print('Making null...',i,temp_file_lines_b[i])

                temp_file_lines_b[i] = ''


    if developer_mode:
        developer_print('Processed file lines :',len(temp_file_lines_b))
        developer_print('Processed lines :',temp_file_lines_b)

    return  {
        'correct_list': temp_file_lines_b
             }


def merge_the_files(filename_a, filename_b, defects_to_be_added=[], developer_mode=False): # added on 13/10/2020
    """

    :param filename_a:
    :param filename_b:
    :param defects_to_be_added:
    :param developer_mode:
    :return:
    Date : 13/10/2020 - Updated Logic for the distinct lines
    """
    developer_mode = True
    stop_after_line = 1005
    # stop_after_line = 1

    no_of_lines = 0
    FilelinesA = get_file_content(filename=filename_a,trim_spaces=True)  # This option ", " can be added to ignore the spacces
    FilelinesB = get_file_content(filename=filename_b, trim_spaces=True)
    if developer_mode:
        developer_print('len(Filelines A) :',len(FilelinesA))
        developer_print('len(Filelines b) :',len(FilelinesB))
    FilelinesA_trimmed = [reduce_space(i, use_strip=False).lower() for i in FilelinesA]
    FilelinesB_trimmed = [reduce_space(i, use_strip=False).lower() for i in FilelinesB]

    fromdate = file_mtime(filename_a)
    todate = file_mtime(filename_b)

    # diff_uni = difflib.unified_diff(fromlines, tolines, fromfile, tofile, fromdate, todate, n=3)
    diff_uni = list(difflib.unified_diff(FilelinesA_trimmed, FilelinesB_trimmed, filename_a, filename_b, fromdate, todate,n=no_of_lines))
    # if developer_mode:
        # developer_print('len(diff_uni):',len(diff_uni))
    write_into_file(file_name='temp_uni_diff.sql', contents=''.join(diff_uni), mode='w')
    index_of_b = 0
    updated_b_fixes = []
    sample_dict = {'start_index_a': '', 'content': [], 'stop_index_a': '', 'start_index_b': '', 'stop_index_b': '', 'status': 'added' } #added/'ignored
    correct_list = []
    is_block = False
    developer_print('Before the loop type(diff_uni):',type(diff_uni))

    temp_index =0
    temp_index_plus = 0
    lines_added_from_a = []
    for index, each_line in enumerate(diff_uni):
        if index < 2:
            # developer_print('Skipping Juk l :', each_line.strip())
            continue
        if len(each_line[1:].strip())<1:continue
        if each_line.strip().startswith('@@'):
            if developer_mode:
                developer_print('index lines are detected :',each_line)

            uni_indexes = extract_indexes(each_line,developer_mode = developer_mode)
            if developer_mode:
                developer_print('type(uni_indexes) : ',type(uni_indexes))
                developer_print('uni_indexes : ',uni_indexes)

            if correct_list:
                if developer_mode:
                    developer_print('Before validation len(correct_list) : ',len(correct_list))
                    developer_print('Before validation correct_list : ',correct_list)
                    input()

                correct_list2 = validate_plus_lines_unified(correct_list=correct_list, lines_added_from_a=lines_added_from_a, index_dict =temp_dict, filelines_a =FilelinesA, filelines_b =FilelinesB, filelines_a_trimmed =FilelinesA_trimmed, filelines_b_trimmed =FilelinesB_trimmed, developer_mode=developer_mode)['correct_list']
                if developer_mode:
                    developer_print('After validation len(correct_list2) : ', len(correct_list2))
                    developer_print('After validation correct_list2 : ', correct_list2)
                    input()
                temp_dict['content'] = correct_list2
                if developer_mode:
                    developer_print('B\'s index:',temp_dict['start_index_b'])
                    for indr,i in enumerate(correct_list):
                        developer_print('Correct list: ',indr, i.strip())
                if temp_dict['content']:
                    updated_b_fixes.append(temp_dict)
            temp_dict = sample_dict.copy()
            temp_index = -1
            # if len(uni_indexes)==3: uni_indexes.append(-1)
            # if len(uni_indexes)==2:
            #     uni_indexes.append(-1)
            #     uni_indexes.append(-1)
            if len(uni_indexes)==4:
                temp_dict['start_index_a'] = int(uni_indexes[0])
                temp_dict['stop_index_a'] = int(uni_indexes[1])
                temp_dict['start_index_b'] = int(uni_indexes[2])
                temp_dict['stop_index_b'] = int(uni_indexes[3])
            else:
                developer_print('Length of the uni_indexes are not fine !')
            correct_list = []
            lines_added_from_a = [] # added on 14/10/2020
            # print('Indexes planned :',temp_dict)
            continue



        developer_print('each line :',each_line.strip())
        if developer_mode:
            developer_print('************************************************************************')
            developer_print(' Processing line  :', index, each_line.strip())
            developer_print(' is_block :', is_block)
            # developer_print(' Extraced IDS from the line   :', ids)
            developer_print(' We are looking for defects id :', defects_to_be_added)
            if stop_after_line and index >= stop_after_line:
                temp = input()
                if str(temp) == '0': stop_after_line = ''

        if each_line.startswith('+'):
            if temp_dict['stop_index_a'] == 0 and temp_dict['stop_index_b'] == -1 :
                continue
            if temp_dict['stop_index_b']>0:
                temp_index_plus += 1

            suspect_b = int(temp_dict['start_index_b']) + temp_index_plus

            temp_plus_line  = FilelinesB[suspect_b - 1]
            if developer_mode :
                developer_print('suspect_b  :',suspect_b)
                developer_print('temp_plus_line  :',temp_plus_line)
                
            correct_list.append('+'+str(temp_plus_line))  # adding all the plus lines_along with
            if developer_mode:
                developer_print(' Plus line : Hence added to the list directly :', each_line.strip())
            print('temp dict :',temp_dict)
            input()
        elif each_line.startswith('-') and defects_to_be_added:  # so this is the new line to be added in File B
            temp_index += 1
            suspect_a = int(temp_dict['start_index_a']) + temp_index
            if developer_mode:
                developer_print('each line :', each_line.strip())
                developer_print('temp_index :', temp_index)
                developer_print('suspect_a :',suspect_a)
                developer_print('FilelinesA :',FilelinesA[suspect_a-1])
                developer_print('FilelinesA_trimmed :',FilelinesA_trimmed[suspect_a-1])
            id_detection_line = FilelinesA[suspect_a-1]


            ids = get_all_fix_id(id_detection_line)['valid_fixes']  # Extracting Defect Ids in the current line
            if ids:  # if we found defect ID in the line then the decision to add/ignore will be done here
                if get_defect_id_presence(ids=ids, defects_to_be_added=defects_to_be_added)['id_presence'] == True:
                    if developer_mode:
                        developer_print(' Minus line : Expected defect id is present in this line , Hence added ')
                    # correct_list.append(each_line[1:])
                    correct_list.append(id_detection_line)

                    if is_block == False:
                        is_block = check_for_block_start(each_line=id_detection_line)['status']
                        if developer_mode:
                            if is_block:
                                developer_print(' "block_status" is changed to "TRUE" ')

                    if is_block == True:
                        is_block = check_for_block_end(each_line=id_detection_line)['status']
                        if developer_mode:
                            if is_block == False:
                                developer_print(' "block_status" is changed to "False" ')

                    if reduce_space(each_line[1:]):
                        lines_added_from_a.append(
                            {'lined_added': False, 'line': [each_line[1:]], 'defect_id_match': True, 'is_block': is_block,
                             'result_index': index,
                             'hint': 'added with presence of defect id ( case : ids : matched in detected list '})


                elif is_block:  # or is_prev_line_added:
                    if developer_mode:
                        developer_print(
                            ' Minus line : Defect id is not matched in the extracted defects list , but is_block is True, Hence added ')
                    # correct_list.append(each_line[2:])
                    correct_list.append(id_detection_line)
                    if reduce_space(each_line[1:]):
                        lines_added_from_a.append(
                            {'lined_added': False, 'line': [each_line[1:]], 'defect_id_match': False, 'is_block': is_block,
                             'result_index': index,
                             'hint': 'added because of is_block : True ( case : ids = True , but not matched with list '})

            else:  # if we dont have any valid defect ID extracted from the current line
                if is_block:  # if the previous lines are added as a valid fix , then these lines also will be added=
                    if developer_mode:
                        developer_print(' Minus line : no defects are extracted from the line, but "is_block" = True , Hence added ')
                    # correct_list.append(each_line[2:])
                    correct_list.append(id_detection_line)
                    if reduce_space(each_line[1:]):
                        lines_added_from_a.append({'lined_added': False, 'line': [each_line[1:]], 'defect_id_match': False, 'is_block': is_block,'result_index': index, 'hint': 'added because of is_block : True ( case : ids = False  '})

        if is_block == True:
            if ids and defects_to_be_added:
                if check_for_block_end(each_line=each_line[1:])['status'] == False and get_defect_id_presence(ids=ids, defects_to_be_added=defects_to_be_added)['id_presence'] == True:
                    is_block = False


        if developer_mode:
            developer_print(' End of the looping for line  :', each_line.strip())
            developer_print(' is_block status :', is_block)
            if len(correct_list) > 2:
                developer_print('correct_list[-3] :', correct_list[-3])
                developer_print('correct_list[-2] :', correct_list[-2])
                developer_print('correct_list[-1] :', correct_list[-1])
            developer_print('len(correct_list) :', len(correct_list))
            developer_print('************************************************************************')

            if stop_after_line and index >= stop_after_line:
                temp = input()
                if str(temp) == '0': stop_after_line = ''

    if developer_mode:
        for ind,i in enumerate(updated_b_fixes):
            developer_print('updated_b_fixes :',ind,i)

    updated_list = get_updated_file_b(file_lines_b=FilelinesB,file_lines_a=FilelinesA, file_lines_b_trimmed =FilelinesB_trimmed,file_lines_a_trimmed=FilelinesA_trimmed, updated_b_fixes=updated_b_fixes, developer_mode= developer_mode)['correct_list']

    return {
            'correct_list' : updated_list
    }


def extract_indexes(each_line, developer_mode=False): # added on 14/10/2020
    splits = str(each_line).split('+')
    minus_tmp = re.findall('\d+', str(splits[0]))
    plus_tmp = re.findall('\d+', str(splits[1]))
    if len(minus_tmp) == 1:
        minus_tmp.append(-1)
    if len(plus_tmp) == 1:
        plus_tmp.append(-1)
    tmp = minus_tmp + plus_tmp
    tmp = [int(i) for i in tmp]
    return tmp
def get_next_files(epe_id ,start_index =0,stop_index = 10): # added on 21/10/2020
    temp_list = []
    for i in range(start_index,stop_index):
        if i < 10:
            patch_name = epe_id + '_0'
        else:
            patch_name = epe_id + '_'
        temp_list.append(str(patch_name)+str(i))
    return temp_list

def get_patch_filename_to_deploy(epe_id,patch_folder,developer_mode = False,check_threshold = 10): # added on 21/10/2020
    if developer_mode:
        print('EPE_ID :', epe_id)
        print('PATCH_FOLDER:', patch_folder)
    new_patch_filename = ''
    last_patch_file_name = ''
    i=0
    while True:
        i = i + 1
        if i>1000:
            print('Reached maximum threshold in Looking patch file')
            break

        if developer_mode:
            print('looping index :',i)
        if i<10:
            patch_name = epe_id + '_0'
        else:
            patch_name = epe_id + '_'
        next_10_files = get_next_files(epe_id = epe_id,start_index = i,stop_index = i+check_threshold)
        next_10_match = [os.path.exists(os.path.join(patch_folder, str(i) + '.sql')) for i in next_10_files]
        any_10 = any(next_10_match)
        if developer_mode:
            print('File names :',next_10_files)
            print('File presence :',next_10_match)
            print('any_10 :',any_10)

        patch_name+=str(i)
        if i==1:last_patch_file_name = patch_name
        if developer_mode:
            print('Looking for patch file :', patch_name)

        if os.path.exists(os.path.join(patch_folder,str(patch_name)+'.sql')):
            if developer_mode :
                print('Patch file exists :',patch_name)
            last_patch_file_name = patch_name
            continue
        elif any_10 == False:
            new_patch_filename = patch_name
            if developer_mode:
                print('Patch file doesn\'t exists :', patch_name)
            break

    return {
            'new_patch_filename':new_patch_filename
            ,'last_patch_file_name':last_patch_file_name
    }

if __name__ == "__main__":
    start = time.time()
    if False:
        looping_line1 = 'and isnull(su.sbl_lot_no,'')        = isnull(dtl.wms_stk_acc_lotno,isnull(su.sbl_lot_no,'')) -- Code Added for LRT-4117-- Code Commented for LRT-4117 -- Code uncommented for NIE-567'
        looping_line2 = '--and isnull(su.sbl_lot_no,'')        = isnull(dtl.wms_stk_acc_lotno,isnull(su.sbl_lot_no,'')) -- Code Added for LRT-4117-- Code Commented for LRT-4117'
        print('looping_line1 :')
        lp1 = reduce_space(str(looping_line1).lower(), trim_characters=['--'], developer_mode=True,check_in_start=True)
        lp2 = reduce_space(str(looping_line2).lower(), trim_characters=['--'], developer_mode=True,check_in_start=True)
        if lp1 in lp2 or lp2 in lp1:
            print('Presence : True')
        else:
            print('Presence : False')
        # print('looping_line2 :',reduce_space(str(looping_line2).lower(), trim_characters=['--'], developer_mode=True,check_in_start=True))
    if False:
        file_name = sys.argv[1]
        get_input_excel_object_merge(file_name, developer_mode= False)['sp_list']

    if False:
        #  to validate the procedure automatically , tried on 28-sep-2020
        file_name = sys.argv[1]
        directory = sys.argv[2]
        print(validate_sp(directory = directory,sp_list = [file_name] ))
    if True:
        arg = argparse.ArgumentParser('Program to add the missing Fixes  !!', add_help=True)
        arg.add_argument('-i', '--input_directory', help='Input directory which contains the updated objects',
                         required=True)
        arg.add_argument('-o', '--output_directory', help='Output directory for the modified files', required=False)
        arg.add_argument('--defects_file',
                         help='An excel or text file which contains Defect IDs SP_NAME<tab>DEFECT_ID1,DEFECT_ID2,DEFECT_ID3 ',
                         required=False)
        arg.add_argument('--get_help_text', help='If the keyword is mentioned, then the text will be extracted from DB',
                         nargs='?', const=True, default=False, required=False)
        arg.add_argument('-dev_mode', '--developer_mode',help='This will enable the developer mode which helps the developer', nargs='?', const=True,default=False, required=False)
        arg.add_argument('--strict_mode',help='This will enable the developer mode which helps the developer', nargs='?', const=True,default=False, required=False)
        arg.add_argument('--skip_git_input',help='This options will disable the preparation of GIT Automation Input ', nargs='?', const=True,default=False, required=False)
        arg.add_argument('--skip_object_merge',help='This option will disable the execution of object merge process', nargs='?', const=True,default=False, required=False)
        arg.add_argument('--consolidate_files',help='This option will enable only file consolidation', nargs='?', const=True,default=False, required=False)
        arg.add_argument('--voice_mode',help='This option enables the voice mode ', nargs='?', const=True,default=False, required=False)
        args = arg.parse_args()
        print('/nUser inputs :', args)
        input('Proceed ?')

        input_directory = args.input_directory
        output_directory = args.output_directory
        if not output_directory: output_directory = os.path.join(input_directory, 'Extracted_objects')
        get_help_text = args.get_help_text
        developer_mode = args.developer_mode
        defects_file = args.defects_file
        strict_mode = args.strict_mode
        skip_git_input = args.skip_git_input
        skip_object_merge = args.skip_object_merge
        consolidate_files = args.consolidate_files
        voice_mode = args.voice_mode


        if defects_file:
            def_res_dict = prepare_input_from_defects_file(defects_file,developer_mode = False)
            epe_id_and_sps = def_res_dict['epe_id_and_sps'] # for GIT Input preparation
            sp_and_defects = def_res_dict['sp_and_defects']
        else:
            epe_id_and_sps = []
            sp_and_defects = []

        # process getting started here
        # file_list = Get_files_list(input_directory)['file_names']
        file_list = Get_files_list(input_directory,defects_file = sp_and_defects)['file_names'] # added on 10/10/2020 tot handle if no input files are in the input directory
        if get_help_text:

            # extracting sps from source db

            help_text_dict1 = Get_helptext_from_server(SERVER_DETAILS={'hostname': '172.27.4.198'}, SP_LIST=file_list,DIRECTORY=input_directory, developer_mode=developer_mode , strict_mode = strict_mode)
            # extracting sps from destination db
            for each in help_text_dict1:
                print('SP extraction status :',each,len(help_text_dict1[each]))
            help_text_dict2 = Get_helptext_from_server(SERVER_DETAILS={'hostname': '172.27.5.174'}, SP_LIST=file_list,DIRECTORY=output_directory, developer_mode=developer_mode , strict_mode = strict_mode)
            # print('EXTRACTION STATUS :\nSuccess : {0}\nFailed  : {1}'.format(len(help_text_dict['success']),len(help_text_dict['failed'])))
            for each2 in help_text_dict2:
                print('SP extraction status :',each2,len(help_text_dict2[each2]))
            if voice_mode:
                speak_words('procedure definitions are extracted in files')




        if not sp_and_defects:
            print('\n DEFECTS IDs/ EPE ID are not provided ! \n Processing based on the input directory :', defects_file)
            file_list = Get_files_list(input_directory)['file_names']
            sp_and_defects = get_dict_from_filelines(file_list)
        modified_file_path = 'modified'
        modified_files_directory = os.path.join(output_directory, modified_file_path)
        write_into_file(file_name=OBJECT_MERGE_CONSOLIDATED_FILE, contents='', mode='w')
        if skip_object_merge == False:
            for index, each_dict in enumerate(sp_and_defects): # processed inputs
                if developer_mode:
                    developer_print('Type: ',type(each_dict))

                if type(each_dict)==dict:
                    sp_file_name = each_dict['sp_name']
                    defects_to_be_added = each_dict['defect_ids']
                    epe_id = ''
                else:
                    if developer_mode:
                        developer_print('each_dict :',each_dict)
                        developer_print('sp_and_defects[each_dict] :',sp_and_defects[each_dict])
                    sp_file_name = each_dict
                    defects_to_be_added = sp_and_defects[each_dict]['defects']
                    epe_id = sp_and_defects[each_dict]['epe_id']

                # if not sp_file_name.lower().endswith('.sql'): sp_file_name += '.sql'
                sp_file_name = handle_extension(sp_file_name)['new_extension']


                # added on oct-29 to get the consolidated list
                cons_full_log = [','.join(defects_to_be_added),sp_file_name,epe_id]
                cons_full_log_text = '\t'.join(apply_to_list(cons_full_log, make_string=True))+'\n'
                write_into_file(file_name=OBJECT_MERGE_CONSOLIDATED_FILE, contents= cons_full_log_text, mode='a')
                write_into_file(file_name=OBJECT_MERGE_CONSOLIDATED_LOG, contents=add_timestamp(cons_full_log_text), mode='a')
                if consolidate_files: continue
                if len(get_all_fix_id(file_content=sp_file_name, extract_from_header=False, developer_mode=developer_mode)['valid_fixes'])>0:
                    print('Skipping the patch file :',sp_file_name)
                    continue
                file_a = os.path.join(input_directory,sp_file_name)
                file_b = os.path.join(output_directory,sp_file_name)


                print('\nProcessing file ' + str(index + 1) + '/' + str(len(sp_and_defects)) + ' ..... ' + str(sp_file_name))
                # input('Proceed ??')
                if False:
                    correct_list = merge_the_files(filename_a = file_a, filename_b=file_b, defects_to_be_added=defects_to_be_added,developer_mode=developer_mode)['correct_list']
                    # print('result of merge_files :',correct_list)
                    modified_file_path = 'modified'
                    modified_files_directory = check_and_make_path(os.path.join(output_directory, modified_file_path))['directory']
                    output_file_name = os.path.join(modified_files_directory, sp_file_name)
                    print('\nBefore writing the file name :',output_file_name)
                    write_into_file(file_name = output_file_name, contents = ''.join(correct_list), mode='w')

                if True:
                    FilelinesA = get_file_content(filename = file_a,trim_spaces = True)  # This option ", " can be added to ignore the spacces
                    FilelinesB = get_file_content(filename = file_b,trim_spaces = True)

                    if not FilelinesA or not FilelinesB:
                        print('\nFiles are not found ! Skipping...',sp_file_name)
                        continue
                    correct_list = ObjectMerge(FilelinesA = FilelinesA, FilelinesB = FilelinesB, defects_to_be_added = defects_to_be_added,developer_mode = developer_mode)['updated_file_A']
                    modified_files_directory = check_and_make_path(os.path.join(output_directory, modified_file_path))['directory']
                    output_file_name = os.path.join(modified_files_directory, sp_file_name)
                    write_into_file(file_name = output_file_name, contents = ''.join(correct_list), mode='w')
                    sys.stdout.write('\n Given fix IDs         : ' + str(defects_to_be_added))
                    sys.stdout.write('\n Lines in file A       : ' + str(len(FilelinesA)) + '\n Lines in file B       : ' + str(len(FilelinesB)))
                    sys.stdout.write('\n Lines in updated file : ' + str(len(correct_list)) + ' check the path : ' + str(modified_files_directory))
                    print('\n...............................................................................................................')
                
                # file log
                # headers = 'TIME_STAMP \t INPUT_DIRECTORY \t OBJECT_NAME \t NO_OF_LINES_A \t NO_OF_LINES_b \t NO_OF_LINES_MODIFIED_FILE \n'
                # write_into_file(file_name=OBJECT_MERGE_FULL_LOG, contents=headers, mode='w')
                full_log =  [input_directory,sp_file_name,','.join(apply_to_list(defects_to_be_added,make_string=True)),len(FilelinesA),len(FilelinesB),len(correct_list)]
                full_log_text = '\t'.join(apply_to_list(full_log,make_string=True))
                write_into_file(file_name=OBJECT_MERGE_FULL_LOG, contents=add_timestamp(full_log_text), mode='a')
            if voice_mode:
                if consolidate_files:
                    speak_words('Procedures and defects ids are consolidated ')
                else:
                    speak_words('Object merging is completed ')

        if skip_git_input==False and not consolidate_files:
            print('Preparing GIT input...........')
            res = prepare_GITAutomation_input(epe_id_dict = epe_id_and_sps, directory=modified_files_directory, developer_mode=developer_mode,git_input_file = defects_file,sp_and_defects = sp_and_defects)
            print( 'GITAutomation input is prepared at :',res['git_input_file'])
            if voice_mode:
                speak_words('Git inputs are prepared')

    print('Consolidated defects file :',OBJECT_MERGE_CONSOLIDATED_FILE)
    end = time.time()

    print()
    print('Total Time taken in seconds : {:.1f}'.format(end - start))
    print('Total Time taken in Minutes : {:.2f}'.format((end - start) / 60))
    if voice_mode:
        speak_words('Code execution is completed ')

# python ObjectMerge.py -i G:\Ajith\Logistics\2020\Pss-Enhancement-Merge\Automation-test -o G:\Ajith\Logistics\2020\Pss-Enhancement-Merge\Automation-test\Extracted_objects --defects_file G:\Ajith\Excel\Object-merge-sample-input.xlsx
# 06/10/2020 - exhausted about the logic
# python ObjectMerge.py -i G:\Ajith\Logistics\2020\Prasath_object_merge_set2_set3\112_bulk_test\188 --defects_file g:\Ajith\Excel\Total_merge_status.xlsx --skip_git_input
# 10/10/2020
#python ObjectMerge.py -i G:\Ajith\Logistics\2020\Prasath_object_merge_set4\188 --skip_git_input --defects_file g:\Ajith\Excel\Object_merge_testing.xlsx
# python ObjectMerge.py -i G:\Ajith\Logistics\2020\Prasath_object_merge_set2_set3\112_bulk_test\188 --defects_file g:\Ajith\Excel\Total_merge_status.xlsx --skip_git_input