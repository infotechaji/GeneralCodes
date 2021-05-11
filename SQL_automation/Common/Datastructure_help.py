def get_presence_missing_data(list1,list2):
    presence = []
    missing = []
    for ele1 in list1:
        if ele1 in list2:
            presence.append(ele1)
        else:
            missing.append(ele1)
    return {
        'presence': presence
        , 'missing': missing
    }

def get_list_difference(list1, list2,consider_case = False):

    if consider_case == False:
        list1 = [i.lower() for i in list1]
        list2 = [i.lower() for i in list2]
    list1_presence = []
    list1_missing = []

    list2_presence = []
    list2_missing = []

    res1 = get_presence_missing_data(list1,list2)
    list1_presence = res1['presence']
    list1_missing = res1['missing']

    res2 = get_presence_missing_data(list2, list1)
    list2_presence = res2['presence']
    list2_missing = res2['missing']

    return {
            'list1_presence': list1_presence
            ,'list1_missing': list1_missing
            ,'list2_presence': list2_presence
            ,'list2_missing': list2_missing
            }

def apply_to_list(input_list,make_upper = False, make_lower= False,make_int= False,make_string=False):
    # added to make the list comprehension process easy  , added on 15/10/2020
    temp_list = input_list
    if make_string: return [str(i) for i in temp_list]
    elif make_upper: return [str(i).upper() for i in temp_list]
    elif make_lower: return [str(i).lower() for i in temp_list]
    elif make_int: return [int(i) for i in temp_list]
    return temp_list



if __name__ =='__main__':
    li1 = [10, 15, 20, 25, 30, 35, 40]
    li2 = [25, 40, 35,1]
    print('List 1 :',li1)
    print('List 2 :',li2)
    print('list1 - list2 :', get_list_difference(li1, li2))
    # print('list2 - list1 :', get_list_difference(li2, li1))