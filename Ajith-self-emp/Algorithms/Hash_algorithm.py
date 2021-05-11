# [sha1, sha224, sha256, sha384, sha512, md5]
# https://www.freelancer.in/projects/python/Hash-Generator-only-Python/details
import hashlib,random,string
import sys,os

sys.path.insert(1, 'G:\\Ajith\\OtherFiles\\common')
from Help_print import *
from CustomisedFileOperation import *
from Datastructure_help import *
from CompareAndUpdate import *
from TimeStamp import *


SHA_DICT = {
            64:'sha256'
            ,96:'sha384'
            ,56:'sha224'
            ,128:'sha512'
            ,40:'sha1'
            ,32:'md5'
            }

def get_hash_type(input_str,developer_mode = False):
    input_str_temp = str(input_str).strip()
    input_str_len = len(input_str_temp)
    if developer_mode:
        print('length of the input string :',input_str_len)
    detected_hash_type = ''
    comments = ''
    try:
        detected_hash_type = SHA_DICT[input_str_len]
        if developer_mode:
            print('detected hash type:', detected_hash_type)
    except Exception as e:
        print('Error in finding hash algorithm :',e)
        comments = str(e)

    return {
        'hash_type': detected_hash_type
        ,'comments': comments
    }
#

def get_hashed_string(random_str, hash_type, developer_mode=False):
    if hash_type == 'sha1':
        random_str_encoded = hashlib.sha1(random_str.encode()).hexdigest()
    elif hash_type == 'sha224':
        random_str_encoded = hashlib.sha224(random_str.encode()).hexdigest()
    elif hash_type == 'sha256':
        random_str_encoded = hashlib.sha256(random_str.encode()).hexdigest()
    elif hash_type == 'sha384':
        random_str_encoded = hashlib.sha384(random_str.encode()).hexdigest()
    elif hash_type == 'sha512':
        random_str_encoded = hashlib.sha512(random_str.encode()).hexdigest()
    elif hash_type == 'md5':
        random_str_encoded = hashlib.md5(random_str.encode()).hexdigest()
    else:
        random_str_encoded = ''
    if developer_mode:
        print('hash type :')

    log_text =[random_str,len(random_str),hash_type,len(random_str_encoded),random_str_encoded]
    temp_str = str('\t'.join(apply_to_list(log_text, make_string=True))).strip() + '\n'
    write_into_file(file_name='HASHED_LOG.txt', contents=add_timestamp(str(temp_str)), mode='a')

    return {'hashed_string': random_str_encoded}
def get_random_string(length=12):
    letters = string.ascii_lowercase
    random_str = ''.join(random.choice(letters) for i in range(length))
    return {'random_str':random_str}

def generate_hashes(input_str, no_of_keys=5,developer_mode = False):
    hash_type = get_hash_type(input_str)['hash_type']
    print('detected hash type : ',hash_type)
    status = False
    generated_hashes = {}
    if hash_type:
        for i in range(0, no_of_keys):
            random_str = get_random_string(12)['random_str']
            random_str_encoded = get_hashed_string(random_str = random_str,hash_type = hash_type)['hashed_string']
            # generated_hashes.append({random_str_encoded: random_str})
            generated_hashes[random_str_encoded]= random_str
        status = True

    print('Total generated hashes', len(generated_hashes))
    return {
        'generated_hashes': generated_hashes
        , 'hash_type': hash_type
        , 'status': status
    }

if __name__ == "__main__":
    sha256 = '31e1ba67a3624d93c3d307f09ac730321ec96cf2a99e57e29187e50f8c5fc53a'  # 64
    sha384 = '9c9b9d603b564c01ec66f9f933970fed57496b998b3dfe3edacf1d54509476f8bc8f0365327b574373aa893f6c6c7cfb'  # 96
    sha224 = '839e4eeffeb1a69b1174d62db53bdc9f429f8bbb614fd1aa9eb6e531'  # 56
    sha512 = '1f7ace74cfd75fbb3a51367191e72661779879c552c4cfcc6cabfca0cb3855586c072f630eda73d5364171b6bd7758229c4872471989ca63b7de7a4235944aee'  # 128
    sha1 = 'e78d73a7d32b556c300c181310d1d52e363e7bfc'  # 40
    md5 = '2719fc05f4346489bfbcd11b7fb31f31'  # 32
    for input_test in [md5,sha384,sha1, sha224, sha256, sha384, sha512]:
        gen_dict  = generate_hashes(input_str=input_test,no_of_keys=100)
        gen = gen_dict['generated_hashes']
        hash_detected = gen_dict['hash_type']
        print('Processing hash....',hash_detected)
        for index,each_dict in enumerate(gen):
            # print(index,each_dict,gen[each_dict])
            log_text = [gen[each_dict], len(gen[each_dict]), hash_detected, len(each_dict), each_dict]
            temp_str = str('\t'.join(apply_to_list(log_text, make_string=True))).strip() + '\n'
            write_into_file(file_name='Generated_hashes.txt', contents=str(temp_str), mode='a')

    # get_random_string(5)
    # get_random_string(10)
    # get_random_string(12)
    # sha256 = '31e1ba67a3624d93c3d307f09ac730321ec96cf2a99e57e29187e50f8c5fc53a'  # 64
    # sha384 = '9c9b9d603b564c01ec66f9f933970fed57496b998b3dfe3edacf1d54509476f8bc8f0365327b574373aa893f6c6c7cfb'  # 96
    # sha224 = '839e4eeffeb1a69b1174d62db53bdc9f429f8bbb614fd1aa9eb6e531'  # 56
    # sha512 = '1f7ace74cfd75fbb3a51367191e72661779879c552c4cfcc6cabfca0cb3855586c072f630eda73d5364171b6bd7758229c4872471989ca63b7de7a4235944aee'  # 128
    # sha1 = 'e78d73a7d32b556c300c181310d1d52e363e7bfc'  # 40
    # md5 = '2719fc05f4346489bfbcd11b7fb31f31'  # 32
    #
    # input_list = [sha1, sha224, sha256, sha384, sha512, md5]
    # for i in input_list:
    #     # print (len(i),get_hash_type(i,developer_mode=False)['hash_type'])
    #     print (get_hash_type(i,developer_mode=False)['hash_type'])

    # input_str = sys.argv[1]
    # input1 = "Ajithkumar M"
    # input2 = "Vijay"
    # input3 = "V"
    # input4 = "v"
    # input5 = "."
    # for input_str in [input1,input2,input3,input4,input5,'']:
    #     print('Input string :',input_str)
    #     print('sha256  :',len((hashlib.sha256(input_str.encode())).hexdigest()),(hashlib.sha256(input_str.encode())).hexdigest())
    #     print('sha384  :',len((hashlib.sha384(input_str.encode())).hexdigest()),(hashlib.sha384(input_str.encode())).hexdigest())
    #     print('sha224  :',len((hashlib.sha224(input_str.encode())).hexdigest()),(hashlib.sha224(input_str.encode())).hexdigest())
    #     print('sha512  :',len((hashlib.sha512(input_str.encode())).hexdigest()),(hashlib.sha512(input_str.encode())).hexdigest())
    #     print('sha1    :',len((hashlib.sha1(input_str.encode())).hexdigest()),(hashlib.sha1(input_str.encode())).hexdigest())
    #     print('md5     :',len((hashlib.md5(input_str.encode())).hexdigest()),(hashlib.md5(input_str.encode())).hexdigest())
