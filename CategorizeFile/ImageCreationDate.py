import json,os,sys
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS, GPSTAGS
import datetime
import calendar
"""
Version : 'IMG%Y%m%d%H%M%S' this pattern is added 
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
        if developer_mode: print('temp_file_name :',temp_file_name)
        try:date_obj = datetime.datetime.strptime(temp_file_name, 'Screenshot_%Y-%m-%d-%H-%M-%S')
        except Exception as e:
            if developer_mode : print('get_image_details:\t Error while looking for pattern "Screenshot_2018-03-11-11-14-33"',e)
            if developer_mode : print("get_image_details:\t Trying to look for pattern...'20171008_195417.jpg' ")
            try:date_obj = datetime.datetime.strptime(temp_file_name, '%Y%m%d_%H%M%S')
            except:
                if developer_mode : print('get_image_details:\t Error while looking for pattern "20171008_195417.jpg"', e)
                if developer_mode : print("get_image_details:\t Trying to look for pattern...'IMG_20200423_194412' ")
                try:
                    date_obj = datetime.datetime.strptime(temp_file_name, 'IMG_%Y%m%d_%H%M%S')

                except:
                    if developer_mode : print("get_image_details:\t Trying to look for pattern...'IMG20200423194412.jpg' ")
                    try:

                        date_obj = datetime.datetime.strptime(temp_file_name, 'IMG%Y%m%d%H%M%S')
                    except:
                        pass

    if developer_mode : print('get_image_details:\t date_obj :',date_obj)
    if date_obj:
        return get_details_from_dateobj(date_obj)
    else:
        return {}



# print (get_image_details('G:\\Ajith\\OtherFiles\\Categrise-File\\Test-case\\20171008_195417.jpg'))
# print (get_image_details('G:\\Ajith\\Others\\MyImages\\DCIM\\Screenshots\\IMG_20200423_194412.jpg',True))
# print(get_image_details('G:\\Ajith\\Others\\MyImages\\DCIM\\Screenshots\\Screenshot_2018-03-11-19-17-03.png',True))