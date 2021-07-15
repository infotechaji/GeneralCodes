"""
Functionality : Downloading bhav copy in bulk.
Version : v1.0
History:
        v1.0 - 26/06/2021 - initial version 

Cases to handle : 
        1. Download as zip file.


"""
from pynse import * 
import datetime 

from datetime import timedelta, date
import ast
import json
import csv

# import logging 
# logging.basicConfig(level = logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG)

nse = Nse()

# market_status = nse.market_status()
# with open('market_status.txt','w') as fp:
#     fp.write(str(market_status))

def get_all_weekdays(start_date,end_date,ignore_weekend=True):
    # if start_date == end_date: return [end_date]
    outlist = []
    from datetime import date
    today = date.today()
    # print ('Given end_date :',end_date)
    if start_date>today:
        start_date = today
        print ('start date is changed to today :',end_date)
    if end_date>today:
        end_date = today
        print ('end date is changed to today :',end_date)
    def daterange(date1, date2):
        for n in range(int ((date2 - date1).days)+1):
            yield date1 + timedelta(n)
    start_dt = start_date
    end_dt = end_date
    weekends = [5,6] 
    
    for dt in daterange(start_dt, end_dt):
        
        if dt.weekday() not in weekends:                    # to print only the weekdates
            full_date = dt.strftime("%Y-%m-%d")
            year = dt.strftime("%Y")
            month = dt.strftime("%m")
            date = dt.strftime("%d")
            outlist.append({'year':year,'month':month,'date':date,'full_date':full_date})
    return outlist


def download_bhav_copy(start_date,end_date,date_requirements= ['company_wise'],output_format = 'zip',developer_mode= False,output_directory=os.getcwd(),selected_companies = [],overrite = False): # date_requirement= ['company_wise','date_wise']  , output_format = 'single_files'
    res=  get_all_weekdays(start_date  = start_date,end_date= end_date) 
    # tot_comp_res = [] 
    if selected_companies:
        selected_companies = list(map(lambda x:x.upper(), selected_companies))
    if developer_mode:
        print ('download_bhav_copy : res ',res)
    main_results = {}
    comment = ''
    status = True
    total_files=0
    errored = 0
    for each_date in res:
        print('processing :',each_date['full_date'])
        try:
            bhav_copy = nse.bhavcopy(datetime.date(int(each_date['year']),int(each_date['month']),int(each_date['date'])))
            # if 'date_wise' in date_requirements:
            #     bhav_copy.to_csv(os.path.join(output_directory,str(each_date['full_date'])+'.csv'))
            bhav_copy.to_csv(os.path.join('G:\\Ajith\\Others\\Ajith-self-instresed\\NSE\\Bulk-test\\dailyreport',str(each_date['full_date'])+'.csv'))
            if 'company_wise' in date_requirements:
                temp_dict = bhav_copy.to_dict('index') 
                for i in temp_dict:
                    # print ('each key in dict i:',i,'\n',temp_dict[i])

                    dict_key = i[0]
                    dict_val = temp_dict[i]
                    dict_val['COMPANY_NAME'] = dict_key
                    dict_val['DATE1'] = dict_val['DATE1']
                    if selected_companies:
                        if developer_mode:
                            print ('Looping inside selected companies...')
                        
                        if dict_key.upper() in selected_companies:
                            if developer_mode:
                                print ('Selected companies got passed ')
                            pass
                        else: 
                            if developer_mode:
                                print ('Skipping Company .. :',dict_key)
                            if len(main_results)>= len(selected_companies):
                                break
                            continue
                    if dict_key not in main_results:
                        main_results[dict_key]= []
                        total_files+=1
                    main_results[dict_key].append(dict_val)
            # elif 'date_wise' in date_requirements:
            #     bhav_copy.to_csv((each_date['full_date'])+'.csv'))

        except Exception as e :
            print ('Error while getting bhav copy : ',e)
            comment= str(e)
            status = False
            errored +=1
            pass
    
    try:
        if developer_mode:
            print ('************************************************************************')
            print ('Total results found :',len(main_results))
        for each_company in sorted (main_results.keys()):
            if developer_mode:
                print ('Looping :',each_company,main_results[each_company])
            
            if 'company_wise' in date_requirements:
                # headers  = ['COMPANY_NAME', 'DATE1', 'OPEN_PRICE','HIGH_PRICE','LOW_PRICE','LAST_PRICE','CLOSE_PRICE'
                            # 'AVG_PRICE','TTL_TRD_QNTY','TURNOVER_LACS','NO_OF_TRADES','DELIV_QTY','DELIV_PER']
                headers  = ['COMPANY_NAME', 'DATE1', 'OPEN_PRICE','HIGH_PRICE','LOW_PRICE','LAST_PRICE','CLOSE_PRICE']
                filename = str(each_company).upper()+'.csv'
                filename = os.path.join(output_directory,filename)
                if overrite:
                    if os.path.exists(filename):
                        os.remove(filename)
                        if developer_mode:
                            print ('Existing file deleted :',filename)
                write_csv(filename= filename,fields = headers, mydict = main_results[each_company])
    
    except Exception as e :
            print ('Error while writing results : ',e)
            comment= str(e)
            status = False
        # zip_file= get_zip_file(comp_wise_data)
        # company_data = get_company_wise_split(total_results)
    return {'status' :status,'comments' : comment,'total_files': total_files }


def write_csv(filename,fields, mydict,developer_mode = False):
    try:
        if developer_mode:
            print ('write_csv:\t filename :',filename)
            print ('write_csv:\t fields :',fields)
            print ('write_csv:\t mydict :',mydict)
        with open(filename, 'w',newline='') as csvfile: 
            # writer = csv.DictWriter(csvfile, fieldnames = fields,extrasaction='raise') 
            writer = csv.DictWriter(csvfile, fieldnames = fields,extrasaction='ignore') 
            writer.writeheader()
            writer.writerows(mydict)
    except Exception as e:
        print ('Error while writing csv file :',e)

        return False
    return True


if __name__ == "__main__":
    start = time.time()
    start_date = date(2021,5,1)
    end_date = date(2021,6,20)
    output_directory = 'G:\\Ajith\\Others\\Ajith-self-instresed\\NSE\\Bulk-test\\june-26'
    print (download_bhav_copy(start_date=start_date,end_date=end_date,output_directory= output_directory,selected_companies= [],developer_mode=False,overrite= True,output_format = 'zip'))
    # print (download_bhav_copy(start_date=start_date,end_date=end_date,output_directory= output_directory,selected_companies= [],developer_mode=False,overrite= True))
    # download_bhav_copy(start_date=start_date,end_date=end_date,output_directory= output_directory,selected_companies= ['20MICRONS','ABSLNN50ET','ZYDUSWELL'],developer_mode=True,overrite= True)
    end = time.time()
    print('Total Time taken in seconds : {:.1f}'.format(end - start))
    print('Total Time taken in Minutes : {:.2f}"'.format((end - start) / 60))
    exit()
