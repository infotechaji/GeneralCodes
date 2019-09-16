"""
Functionality: Monitor All the nodes in the batch accounts and deletes the Ideal Machines 
Version : v1.0
History :
		  v1.0 - 12/26/2018 - initial version 

Issues  :
Pending :
"""
import time
import argparse
import azure.batch as batch
import azure.batch.models as batchmodels
import azure.batch.batch_auth as batchauth

class Monitoring_batch():

	def __init__(self,BATCH_ACCOUNT_NAME='fiindcompute',BATCH_ACCOUNT_KEY='iQCfu+gBMWX6jwj33l86pfqtLDVrDGf4lKktAt2SpkVVT08WHb3Q4JyjguZf3WcOJMka++Rlc/IMZeVg1m51Eg==',BATCH_ACCOUNT_URL='https://fiindcompute.southcentralus.batch.azure.com',waiting_seconds=5):
		credentials = batchauth.SharedKeyCredentials(BATCH_ACCOUNT_NAME,BATCH_ACCOUNT_KEY)
		batch_client = batch.BatchServiceClient(credentials,base_url=BATCH_ACCOUNT_URL)
		self.batch_client=batch_client
		self.seconds=waiting_seconds

	def nodes_state(self):
		pool_list = self.batch_client.pool.list()
		pool_id_list = [p.id for p in pool_list]
		# print pool_id_list
		print 'Total pools : ',len(pool_id_list)
		test_node_list=[]
		idle_node_list=[]
		for each_pool_id in pool_id_list:
			# print str(each_pool_id)
			idle_node_count=0
			nodes = list(self.batch_client.compute_node.list(str(each_pool_id)))
			# nodes=[node for node in nodes if node.state == batch.models.ComputeNodeState.idle]
			print str(len(nodes))+' nodes in '+str(each_pool_id)+' pool'
			for node in nodes:
				if node.state == batch.models.ComputeNodeState.idle:
					idle_node_count+=1
					test_node_list.append(node)
			print str(idle_node_count)+' idle nodes in '+str(each_pool_id)+' pool'
		time.sleep(self.seconds)
		for each_node in test_node_list:
			if each_node.state == batch.models.ComputeNodeState.idle:
				idle_node_list.append(each_node.id)
		return idle_node_list

	def jobs_state(self):
		completed_task_list=[]
		job_list = self.batch_client.job.list()
		job_id_list = [j.id for j in job_list]
		print 'Total jobs : ',len(job_id_list)
		for each_job_id in job_id_list:
			completed_task_count=0
			task_list = list(self.batch_client.task.list(str(each_job_id)))
			print str(len(task_list))+' tasks in '+str(each_job_id)+' job'
			for each_task in task_list:
				if each_task.state == batch.models.TaskState.completed:
					completed_task_list.append(each_task.id)
					completed_task_count+=1
			print str(completed_task_count)+' completed tasks in '+str(each_job_id)+' job'
		return completed_task_list

if __name__ == '__main__':
	arg = argparse.ArgumentParser('Program to Trigger Status Process',add_help=True)
	arg.add_argument('-n','--BATCH_ACCOUNT_NAME', nargs='?',help='Azure account name for queue and blob',default='fiindcompute', required=False)
	arg.add_argument('-k','--BATCH_ACCOUNT_KEY', nargs='?',help='Azure account key for queue and blob',default='iQCfu+gBMWX6jwj33l86pfqtLDVrDGf4lKktAt2SpkVVT08WHb3Q4JyjguZf3WcOJMka++Rlc/IMZeVg1m51Eg==',required=False)
	arg.add_argument('-u','--BATCH_ACCOUNT_URL', nargs='?',help='Azure account key for queue and blob',default='https://fiindcompute.southcentralus.batch.azure.com',required=False)
	arg.add_argument('-s','--SECOND',help='seconds for idle node check',nargs='?', const=10, default=10, required=False,type=int,)
	args = arg.parse_args()
	BATCH_ACCOUNT_NAME = args.BATCH_ACCOUNT_NAME
	BATCH_ACCOUNT_KEY = args.BATCH_ACCOUNT_KEY
	BATCH_ACCOUNT_URL = args.BATCH_ACCOUNT_URL
	# credentials = batchauth.SharedKeyCredentials(BATCH_ACCOUNT_NAME,BATCH_ACCOUNT_KEY)
	# batch_client = batch.BatchServiceClient(credentials,base_url=BATCH_ACCOUNT_URL)
	batch_obj=Monitoring_batch(BATCH_ACCOUNT_NAME=args.BATCH_ACCOUNT_NAME,BATCH_ACCOUNT_KEY=args.BATCH_ACCOUNT_KEY,BATCH_ACCOUNT_URL=args.BATCH_ACCOUNT_KEY,args.SECOND)
	idle_nodes = batch_obj.nodes_state()
	print 'Total idel nodes '+str(len(idle_nodes))
	print 'idle nodes :',idle_nodes
	completed_jobs=batch_obj.jobs_state()
	print 'Total completed tasks '+str(len(completed_jobs))
	print 'completed tasks :',completed_jobs
	

