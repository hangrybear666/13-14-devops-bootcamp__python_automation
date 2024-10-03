import boto3
import pprint
import time
import random

ec2_client = boto3.client('ec2', region_name="eu-central-1")
ec2_resource = boto3.resource('ec2', region_name="eu-central-1")

instance_ids_frankfurt = []

reservations_frankfurt = ec2_client.describe_instances()['Reservations']
for res in reservations_frankfurt:
    instances = res['Instances']
    for ins in instances:
        if ins['KeyName'] == "tf-server-key":
          # pprint.pprint(ins)
          instance_ids_frankfurt.append(ins['InstanceId'])

def printTags():
  reservations_frankfurt = ec2_client.describe_instances()['Reservations']
  for res in reservations_frankfurt:
      instances = res['Instances']
      for ins in instances:
        if ins['KeyName'] == "tf-server-key":
          print(ins['Tags'])

randomNr = random.randrange(1,100,1)

print("-------------------------------")
print("------------BEFORE-------------")
print("-------------------------------")
printTags()

for ec2_instance_id in instance_ids_frankfurt:
  response = ec2_resource.create_tags(
      Resources=[ec2_instance_id],
      Tags=[
          {
              'Key': 'changed_by',
              'Value': f"python"
          },
          {
              'Key': 'Name',
              'Value': f"dev-sever{randomNr}"
          },
      ]
  )
  randomNr +=1

for n in range(1, 6):
  time.sleep(1)
  print(f"waiting for tag change for {n} seconds")
print("-------------------------------")
print("------------AFTER--------------")
print("-------------------------------")
printTags()