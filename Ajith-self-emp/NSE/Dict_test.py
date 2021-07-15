import datetime
main_results = {}
developer_mode = True
temp_list = [{'ajith':[{'DATE1': datetime.date(2021, 6, 1), 'PREV_CLOSE': 105.35, 'OPEN_PRICE': 106.0, 'HIGH_PRICE': 107.35, 'LOW_PRICE': 100.7, 'LAST_PRICE': 102.2, 'CLOSE_PRICE': 102.05, 'AVG_PRICE': 103.06, 'TTL_TRD_QNTY': 63748, 'TURNOVER_LACS': 65.7, 'NO_OF_TRADES': 1930, 'DELIV_QTY': '32944', 'DELIV_PER': '51.68'}],
            'vijay':[{'DATE1': datetime.date(2021, 6, 1), 'PREV_CLOSE': 105.35, 'OPEN_PRICE': 106.0, 'HIGH_PRICE': 107.35, 'LOW_PRICE': 100.7, 'LAST_PRICE': 102.2, 'CLOSE_PRICE': 102.05, 'AVG_PRICE': 103.06, 'TTL_TRD_QNTY': 63748, 'TURNOVER_LACS': 65.7, 'NO_OF_TRADES': 1930, 'DELIV_QTY': '32944', 'DELIV_PER': '51.68'}],
            'sivaji':[{'DATE1': datetime.date(2021, 6, 1), 'PREV_CLOSE': 105.35, 'OPEN_PRICE': 106.0, 'HIGH_PRICE': 107.35, 'LOW_PRICE': 100.7, 'LAST_PRICE': 102.2, 'CLOSE_PRICE': 102.05, 'AVG_PRICE': 103.06, 'TTL_TRD_QNTY': 63748, 'TURNOVER_LACS': 65.7, 'NO_OF_TRADES': 1930, 'DELIV_QTY': '32944', 'DELIV_PER': '51.68'}],
            },
            {'ajith':[{'DATE1': datetime.date(2021, 6, 2), 'PREV_CLOSE': 105.35, 'OPEN_PRICE': 106.0, 'HIGH_PRICE': 107.35, 'LOW_PRICE': 100.7, 'LAST_PRICE': 102.2, 'CLOSE_PRICE': 102.05, 'AVG_PRICE': 103.06, 'TTL_TRD_QNTY': 63748, 'TURNOVER_LACS': 65.7, 'NO_OF_TRADES': 1930, 'DELIV_QTY': '32944', 'DELIV_PER': '51.68'}],
            'vijay':[{'DATE1': datetime.date(2021, 6, 2), 'PREV_CLOSE': 105.35, 'OPEN_PRICE': 106.0, 'HIGH_PRICE': 107.35, 'LOW_PRICE': 100.7, 'LAST_PRICE': 102.2, 'CLOSE_PRICE': 102.05, 'AVG_PRICE': 103.06, 'TTL_TRD_QNTY': 63748, 'TURNOVER_LACS': 65.7, 'NO_OF_TRADES': 1930, 'DELIV_QTY': '32944', 'DELIV_PER': '51.68'}],
            'sivaji':[{'DATE1': datetime.date(2021, 6, 2), 'PREV_CLOSE': 105.35, 'OPEN_PRICE': 106.0, 'HIGH_PRICE': 107.35, 'LOW_PRICE': 100.7, 'LAST_PRICE': 102.2, 'CLOSE_PRICE': 102.05, 'AVG_PRICE': 103.06, 'TTL_TRD_QNTY': 63748, 'TURNOVER_LACS': 65.7, 'NO_OF_TRADES': 1930, 'DELIV_QTY': '32944', 'DELIV_PER': '51.68'}],
                }
                ,
        {'ajith':[{'DATE1': datetime.date(2021, 6, 3), 'PREV_CLOSE': 105.35, 'OPEN_PRICE': 106.0, 'HIGH_PRICE': 107.35, 'LOW_PRICE': 100.7, 'LAST_PRICE': 102.2, 'CLOSE_PRICE': 102.05, 'AVG_PRICE': 103.06, 'TTL_TRD_QNTY': 63748, 'TURNOVER_LACS': 65.7, 'NO_OF_TRADES': 1930, 'DELIV_QTY': '32944', 'DELIV_PER': '51.68'}],
        'vijay':[{'DATE1': datetime.date(2021, 6, 3), 'PREV_CLOSE': 105.35, 'OPEN_PRICE': 106.0, 'HIGH_PRICE': 107.35, 'LOW_PRICE': 100.7, 'LAST_PRICE': 102.2, 'CLOSE_PRICE': 102.05, 'AVG_PRICE': 103.06, 'TTL_TRD_QNTY': 63748, 'TURNOVER_LACS': 65.7, 'NO_OF_TRADES': 1930, 'DELIV_QTY': '32944', 'DELIV_PER': '51.68'}],
        'sivaji':[{'DATE1': datetime.date(2021, 6, 3), 'PREV_CLOSE': 105.35, 'OPEN_PRICE': 106.0, 'HIGH_PRICE': 107.35, 'LOW_PRICE': 100.7, 'LAST_PRICE': 102.2, 'CLOSE_PRICE': 102.05, 'AVG_PRICE': 103.06, 'TTL_TRD_QNTY': 63748, 'TURNOVER_LACS': 65.7, 'NO_OF_TRADES': 1930, 'DELIV_QTY': '32944', 'DELIV_PER': '51.68'}],
                }
                ]

for temp_dict in temp_list:

    for i in temp_dict:
        print ('each key in dict i:',i,'\n',temp_dict[i])

        dict_key = i[0]
        dict_val = temp_dict[i]
        if dict_key not in main_results:
            if developer_mode:
                print('New key added ')
            main_results[dict_key]= [dict_val]
            print ('After adding ...main_results[dict_key] :',main_results[dict_key])
            print ('After adding ...type(main_results[dict_key]) :',type(main_results[dict_key]))
        else:
            print ('dict_key :',dict_key)
            print ('before updating main_results[i[0]]:',main_results[dict_key])
            print ('before updating temp_dict[i] :',dict_val)
            # print (main_results[i[0]].append)
            main_results[dict_key]= main_results[dict_key].append(dict_val)
            print ('after updating main_results[i[0]]:',main_results[dict_key])
            input('updating main results ')
