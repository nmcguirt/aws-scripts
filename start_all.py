import os
import botocore.session
import sys

AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_DEFAULT_REGION = os.environ['AWS_DEFAULT_REGION']

def main():
	session = botocore.session.Session()
	session.set_credentials(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY)
	ec2 = session.get_service('ec2')
	endpoint = ec2.get_endpoint(AWS_DEFAULT_REGION)
	op_din = ec2.get_operation('DescribeInstances')
	op_start = ec2.get_operation('StartInstances')

	http_response, reservation_data = op_din.call(endpoint, filters=[{"Name":"instance-state-name","Values":["stopped"]}] )
	if not http_response.ok:
		print(reservation_data['Errors'])
		sys.exit(2)
	else:
		reservations = reservation_data['Reservations']

	#Pull the instances out of reservations
	instances = []
	for reservation in reservations:
		instances += reservation['Instances']

	print("Found %i instances in stopped state" % len(instances))
	instance_ids = [instance['InstanceId'] for instance in instances]

	http_response, data = op_start.call(endpoint, instance_ids = instance_ids)
	if not http_response.ok:
		print(data['Errors'])
		sys.exit(2)

	for instance in data['StartingInstances']:
		print("Instance %s now starting" % instance['InstanceId'])	
	
if __name__ == '__main__':
	main()