from pynse import * 
import datetime 
import logging 
from datetime import timedelta, date


from sqlalchemy import create_engine
engine = create_engine('sqlite://', echo=False)

# logging.basicConfig(level = logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG)

nse = Nse()

market_status = nse.market_status()
with open('market_status.txt','w') as fp:
    fp.write(str(market_status))

# print ( nse.info('SBIN')) 

# print ( nse.info('TCS')) 


# print ( nse.get_quote('RELIANCE',Segment.FUT)) 


# print ( nse.get_quote('RELIANCE',Segment.FUT)) 

# dates = ['']
# for 
def get_all_weekdays(start_date,end_date,ignore_weekend=True):
    outlist = []
    def daterange(date1, date2):
        for n in range(int ((date2 - date1).days)+1):
            yield date1 + timedelta(n)

    # start_dt = date(2019,1,21)
    # end_dt = date(2019,2,4)
    start_dt = start_date
    end_dt = end_date
    weekends = [5,6] 
    
    for dt in daterange(start_dt, end_dt):
        
        # if ignore_weekend:
        if dt.weekday() not in weekends:                    # to print only the weekdates
            full_date = dt.strftime("%Y-%m-%d")
            year = dt.strftime("%Y")
            month = dt.strftime("%m")
            date = dt.strftime("%d")
            outlist.append({'year':year,'month':month,'date':date,'full_date':full_date})
    return outlist


# res=  get_all_weekdays(start_date  = date(2021,6,1),end_date= date(2021,6,30)) 

# for i in res:
#     print(i['full_date'])
#     try:
#         bhav_copy = nse.bhavcopy(datetime.date(int(i['year']),int(i['month']),int(i['date'])))
#         bhav_copy.to_csv(os.path.join('G:\\Ajith\\Others\\Ajith-self-instresed\\NSE\\Downloaded-files',str(i['full_date'])+'.csv'))
#     except Exception as e :
#         print ('Exception while bhav copy : ',e)
    
    
bhav_copy = nse.bhavcopy(datetime.date(2021,6,21))
# print (bhav_copy)
# print (bhav_copy.to_dict())
# print ( bhav_copy.to_dict('records'))
main_dict = bhav_copy.to_dict('index')

for each_dict in main_dict:
    print (each_dict)
    print (main_dict[each_dict])
    input('---------------')
    #  just format the data using company wise thats all. 




# print ( bhav_copy.to_dict('split'))
    # each company_data and store it into dict based on the company structure. 

# bhav_copy.to_sql('users', con=engine)
# print ( engine.execute("SELECT top 10 * FROM users").fetchall())





# print (bhav_copy.to_dict())

# for index, row in bhav_copy.iterrows():
#     # print(index,row['c1'], row['c2'])
#     print('index :',index,type(index))
#     print('row :',row,type(row))
#     input('proceeed to next line ')


# print(type(bhav_copy))

# bhav_copy.to_csv('file_name.csv')




