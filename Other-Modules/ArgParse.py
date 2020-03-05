import argparse
if __name__ =='__main__':
	arg = argparse.ArgumentParser('Program to collect basic details of a company',add_help=True)
	arg.add_argument('-i','--input_list',help='Enter astros(comma separated) ',default ='scorpio,pisces',required=False)
	arg.add_argument('-d','--destroy_time',help='delay time',type=int,default =10,required=False)
	args = arg.parse_args()
	astr_obj=AstroDeccan(developer_mode=False)
	astr_obj.get_prediction(args.input_list.split(','),args.destroy_time)