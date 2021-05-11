# from pytube import YouTube 
import pytube
import datetime
  
#where to save 
# SAVE_PATH = 'G:\\Ajith\\Others\\Ajith-self-instresed\\YoutubeDowloaded\\DownloadedVideos'
SAVE_PATH = 'G:\\Ajith\\Others\\Ajith-self-instresed\\YoutubeDowloaded\\DownloadedVideos\\selectedResolution'
ERROR_LOG = 'Error_log.txt'
FILE_LOG = 'general_log.txt'
#link of the video to be downloaded 
# link=["https://www.youtube.com/watch?v=xWOoBJUqlbI", 
#     "https://www.youtube.com/watch?v=xWOoBJUqlbI"
#     ]
link  =  ['https://www.youtube.com/watch?v=rnHWzPzEnEE&ab_channel=Ulchemy']

# yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
def download_yt_video(input_link,SAVE_PATH,extension ='mp4'):
    yt = pytube.YouTube(input_link)
    print('Connection established')
    # stream = yt.streams.first() 
    stream = yt.streams.get_by_resolution('720p')
    print('Downloading started....')
    stream.download(SAVE_PATH)
    print('Downloading compeleted....')
    # try:
    #     yt.streams.filter(progressive=True, file_extension=extension).order_by('resolution').desc().first().download(SAVE_PATH)
    #     status = True
    # except Exception as e:
    #     print('Error while downloading :',e)
    #     status = False
    #     with open(ERROR_LOG,'a') as fp:
    #         fp.write('\t'.join([str(datetime.datetime.now()),input_link,SAVE_PATH,extension,str(e)]))
    status = True
    return status


# for i in link: 
#     try: 
          
#         # object creation using YouTube
#         # which was imported in tcdhe beginning 
#         # # yt = YouTube(i) 
#         # print('Connection success!')
#         status = download_yt_video(input_link= i ,SAVE_PATH,extension ='mp4')
#         with open(FILE_LOG,'a') as fp:
#             fp.write('\t'.join([str(datetime.datetime.now()),input_link,SAVE_PATH,extension,status]))
        
        
#     except Exception as ec: 
#         print("Error while establishing connection :",ec)
      
    #filters out all the files with "mp4" extension 
    # print('yt:',yt)
    # mp4files = yt.filter('mp4') 
  
    # # get the video with the extension and
    # # resolution passed in the get() function 
    # print('mp4files :',mp4files)
    # d_video = yt.get(mp4files[-1].extension,mp4files[-1].resolution) 
    # try: 
    #     # downloading the video 
    #     d_video.download(SAVE_PATH) 
    # except Exception as e: 
    #     print("Error while saving the file :",e)
# print('Task Completed!') 

if __name__=="__main__":
    # file_lines = open(sys.argv[1]).readlines()
    # source_directory = sys.argv[2]
    file_lines  =  ['https://www.youtube.com/watch?v=rnHWzPzEnEE&ab_channel=Ulchemy']
    source_directory = 'G:\\Ajith\\Others\\Ajith-self-instresed\\YoutubeDowloaded\\DownloadedVideos\\selectedResolution'
    try:
        for each_link in file_lines:
            status = download_yt_video(input_link=each_link,SAVE_PATH = source_directory)
            with open(FILE_LOG,'a') as fp:
                fp.write('\t'.join([str(datetime.datetime.now()),each_link,SAVE_PATH,extension,status]))
    except Exception as e:
        print('Error downloading youtube video :',e)
    
