import json,os,sys
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS, GPSTAGS
import datetime
import calendar

"""
Version : v2.1 

Modifications :
                v2.0 20/07/2020 'IMG%Y%m%d%H%M%S' this pattern is added 
                v2.1 20/07/2020 'Screenshot_2018-03-11-19-16-59' this pattern is also added 
"""

# from datetime import datetime
def get_details_from_dateobj(date_obj):
    year=date_obj.strftime('%Y')
    month = date_obj.strftime('%m')
    day = date_obj.strftime('%d')
    hour = date_obj.strftime('%H')
    minute = date_obj.strftime('%M')
    second = date_obj.strftime('%S')
    try:
        month_txt = calendar.month_name[int(month)]
    except Exception as e:
        print('Error in mapping month :', e)
        try:
            month_txt = LOCAL_DATE_MAPPER[month]
        except:
            month_txt = month
    return_dict = {
        'year': year,
        'month': month,
        'month_text': month_txt,
        'date': day,
        'hours': hour,
        'mins': minute,
        'seconds': second
    }
    return return_dict


def get_image_details(filename,developer_mode=False):


    image_exif = Image.open(filename)._getexif()

    # image = Image.open(filename)
    # print('Image opened')
    # # image.verify()
    # print('Image verified ')
    # # print( image._getexif() )
    # info= image.info
    # for tag, value in info.items():
    #     key = TAGS.get(tag, tag)
    #     print(key + " " + str(value))
    # input()
    if developer_mode: print('get_image_details:\timage_exif :',image_exif)
    date_obj=''
    if False:
        # Make a map with tag names
        exif = { ExifTags.TAGS[k]: v for k, v in image_exif.items() if k in ExifTags.TAGS and type(v) is not bytes }
        if developer_mode : print('get_image_details:\t exif :',exif)
        # print(json.dumps(exif, indent=4))
        # Grab the date
        import calendar
        try:date_obj = datetime.datetime.strptime(exif['DateTimeOriginal'], '%Y:%m:%d %H:%M:%S')
        except :
            try:date_obj = datetime.datetime.strptime(exif['DateTime'], '%Y:%m:%d %H:%M:%S')
            except:pass
    else:
        
        temp_file_name = (filename.split(os.sep)[-1]).split('.')[0]
        if len(temp_file_name.strip())==66 and len(temp_file_name.strip().split('_'))==3:
            # PAttern Screenshot_2020-07-29-12-06-52-59_f2cb81fb7cf38af7978f186f2a61634a
            # temp_file_name=temp_file_name.strip().split('_')[:-1]
            temp_file_name='_'.join(temp_file_name.strip().split('_')[:-1])
            if developer_mode: print('get_image_details:\tLengthy pattern matches ',temp_file_name)
        if developer_mode: print('temp_file_name :',temp_file_name)
        MATCHING_PATTERNS=['Screenshot_%Y-%m-%d-%H-%M-%S','Screenshot_%Y-%m-%d-%H-%M-%S-%f','%Y%m%d_%H%M%S','IMG_%Y%m%d_%H%M%S','IMG%Y%m%d%H%M%S']
        for each_pattn in MATCHING_PATTERNS:
            try:
                date_obj = datetime.datetime.strptime(temp_file_name,each_pattn)
                if developer_mode : print ('Matched pattern found !',each_pattn,temp_file_name)
                break
            except Exception as e:            
                if developer_mode : print('get_image_details:\t pattern not Found !',each_pattn)
                pass
    if developer_mode : print('get_image_details:\t date_obj :',date_obj)
    if date_obj:
        return get_details_from_dateobj(date_obj)
    else:
        return {}



# print (get_image_details('G:\\Ajith\\OtherFiles\\Categrise-File\\Test-case\\20171008_195417.jpg'))
# print (get_image_details('G:\\Ajith\\Others\\MyImages\\DCIM\\Screenshots\\IMG_20200423_194412.jpg',True))
# print(get_image_details('G:\\Ajith\\Others\\MyImages\\DCIM\\Screenshots\\Screenshot_2018-03-11-19-17-03.png',True))