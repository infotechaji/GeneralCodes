import math
# Pool	40
# Nodes	1
# Machines	40
# InputCompanies	578
# CompaniesProcessedPerHr	20
# TotalHrs- SingleMachine	28.9
# SplittedMachines	0.7225
# Minutes	43.35
# MinutesRounded	44



def GetEstimatedTime(input_companies=1,companies_processed_per_hr=20,pool_count=1,node_count=1,DEVELEOPER_MODE=False):
	total_machines=pool_count*node_count
	total_companies=input_companies
	if DEVELEOPER_MODE: print 'total_companies:',total_companies
	total_hrs=float(input_companies/companies_processed_per_hr)
	if DEVELEOPER_MODE: print "total_hrs:",total_hrs
	total_hrs_all=int(math.ceil(total_hrs/total_machines))
	if DEVELEOPER_MODE: print 'total_hrs_splitted :',total_hrs_all
	total_minutes=total_hrs_all*60
	if DEVELEOPER_MODE: print 'total_minutes :',total_minutes
	total_minutes_rounded=int(math.ceil(total_minutes))
	if DEVELEOPER_MODE: print 'rounded_minutes :',total_minutes_rounded
	return {
			'total_minutes_rounded':total_minutes_rounded,
			'total_minutes':total_minutes,
			'hrs_single_machines':total_hrs,
			'hrs_all_machines':total_hrs_all,
			'input_companies':input_companies
	}

if __name__=="__main__":
	input_companies=8505
	node_count=90
	print GetEstimatedTime(node_count=node_count,input_companies=input_companies)