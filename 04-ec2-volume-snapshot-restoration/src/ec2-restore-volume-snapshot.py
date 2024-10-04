import boto3
import schedule
import datetime
from operator import itemgetter
import pprint
import time


#   __        __   __                          __   __
#  / _` |    /  \ |__)  /\  |       \  /  /\  |__) /__`
#  \__> |___ \__/ |__) /~~\ |___     \/  /~~\ |  \ .__/
instance_id = input("Enter the ec2 server's instance id to restore to the newest snapshot: ")
instance_stopped = False
instance_restarted = False
new_volume_available = False
volume_detached = False
volume_reattached = False
region = "eu-central-1"

ec2_client = boto3.client('ec2', region_name=region)
ec2_resource = boto3.resource('ec2', region_name=region)

#   __   ___ ___       __
#  /__` |__   |  |  | |__)
#  .__/ |___  |  \__/ |
def query_instances():
  return ec2_client.describe_instances(
    InstanceIds=[instance_id],
  )['Reservations']

instance_reservations = query_instances()
volume_id = instance_reservations[0].get('Instances')[0].get('BlockDeviceMappings')[0].get('Ebs').get('VolumeId')
print(f"----------ID of old volume is {volume_id}----")
availability_zone = instance_reservations[0].get('Instances')[0].get('Placement').get('AvailabilityZone')
print(f"----------availab. zone of instance: {availability_zone}-----")

#   __  ___  __   __             __  ___            __   ___
#  /__`  |  /  \ |__)    | |\ | /__`  |   /\  |\ | /  ` |__
#  .__/  |  \__/ |       | | \| .__/  |  /~~\ | \| \__, |___
response = ec2_client.stop_instances(
  InstanceIds=[instance_id],
  Hibernate=False,
  DryRun=False,
  Force=False # not recommended, can lead to data loss
)

def check_instance_status(isStop):
  instance_count = 1
  stopped_instance_count = 0
  running_instance_count = 0
  statuses = ec2_client.describe_instance_status(
    InstanceIds=[instance_id],
    IncludeAllInstances=True
  )
  for status in statuses['InstanceStatuses']:
    state = status['InstanceState']['Name']
    if state == 'stopped':
      stopped_instance_count += 1
    elif state == 'running':
      running_instance_count +=1
    if isStop:
      print(f"----------Instance '{status['InstanceId']}' is [{state}]")
    else:
      print(f"Instance '{status['InstanceId']}' is [{state}] with instance status [{status['InstanceStatus']['Status']}] and system status [{status['SystemStatus']['Status']}]")
  if isStop and stopped_instance_count == instance_count:
    global instance_stopped
    instance_stopped = True
    print(f"----------All instances successfully stopped.----------")
  elif not isStop and running_instance_count == instance_count:
    global instance_restarted
    instance_restarted = True
    started_instances = query_instances()
    for res in started_instances:
      instances = res['Instances']
      for ins in instances:
        print(f"Instance '{ins['InstanceId']}' has the following IPv4 address: [{ins.get('PublicIpAddress')}]")
    print(f"----------All instances successfully restarted.--------")

schedule.every(8).seconds.do(check_instance_status, True)

while not instance_stopped:
  schedule.run_pending()
  time.sleep(1)
else:
  schedule.clear()

#   __   ___ ___       __                __                   ___
#  |  \ |__   |   /\  /  ` |__|    \  / /  \ |    |  |  |\/| |__
#  |__/ |___  |  /~~\ \__, |  |     \/  \__/ |___ \__/  |  | |___
response = ec2_client.detach_volume(
  VolumeId=volume_id,
)
# pprint.pprint(response) # debug

def check_detachment_status():
  volume_count = 1
  detached_volume_count = 0
  volumes = ec2_client.describe_volumes(
      VolumeIds=[volume_id]
  )
  for volume in volumes['Volumes']:
    if len(volume.get('Attachments')) == 0:
      detached_volume_count += 1
    # pprint.pprint(volume) # debug
  if detached_volume_count == volume_count:
    global volume_detached
    volume_detached = True
    print(f"----------All volumes successfully detached.-----------")

schedule.every(5).seconds.do(check_detachment_status)

while not volume_detached:
  schedule.run_pending()
  time.sleep(1)
else:
  schedule.clear()

#   __   ___ ___              ___  ___  __  ___     __             __   __        __  ___
#  / _` |__   |     |     /\   |  |__  /__`  |     /__` |\ |  /\  |__) /__` |__| /  \  |
#  \__> |___  |     |___ /~~\  |  |___ .__/  |     .__/ | \| /~~\ |    .__/ |  | \__/  |
snapshots = ec2_client.describe_snapshots(
  OwnerIds=['self'],
  Filters=[
      {
          'Name': 'volume-id',
          'Values': [volume_id]
      }
  ]
)
latest_snapshot = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)[0]

#   __   __   ___      ___  ___          __                   ___     ___  __   __            __             __   __        __  ___
#  /  ` |__) |__   /\   |  |__     \  / /  \ |    |  |  |\/| |__     |__  |__) /  \  |\/|    /__` |\ |  /\  |__) /__` |__| /  \  |
#  \__, |  \ |___ /~~\  |  |___     \/  \__/ |___ \__/  |  | |___    |    |  \ \__/  |  |    .__/ | \| /~~\ |    .__/ |  | \__/  |
new_volume_id = ec2_client.create_volume(
  SnapshotId=latest_snapshot['SnapshotId'],
  AvailabilityZone=availability_zone,
  Iops=3000,
  Throughput=125,
  VolumeType='gp3',
  MultiAttachEnabled=False,
  TagSpecifications=[
      {
          'ResourceType': 'volume',
          'Tags': [
              {
                  'Key': 'Name',
                  'Value': 'restored-via-snapshot'
              },
              {
                  'Key': 'created_by',
                  'Value': 'boto3-sdk'
              },
              {
                  'Key': 'restored_date',
                  'Value': f"{datetime.datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}"
              },
          ]
      }
  ]
).get('VolumeId')

#       ___ ___       __                ___               __                   ___
#   /\   |   |   /\  /  ` |__|    |\ | |__  |  |    \  / /  \ |    |  |  |\/| |__
#  /~~\  |   |  /~~\ \__, |  |    | \| |___ |/\|     \/  \__/ |___ \__/  |  | |___

def check_volume_availability():
  vol = ec2_resource.Volume(new_volume_id)
  print(f"----------checking new volume's state... [{vol.state}]")
  if vol.state == 'available':
    global new_volume_available
    new_volume_available = True
    response = ec2_client.attach_volume(
        Device='/dev/xvda', # for root device
        InstanceId=instance_id,
        VolumeId=new_volume_id,
    )
    # pprint.pprint(response) # debug

schedule.every(5).seconds.do(check_volume_availability)

while not new_volume_available:
  schedule.run_pending()
  time.sleep(1)
else:
  schedule.clear()

def check_reattaachment_status():
  volume_count = 1
  reattached_volume_count = 0
  volumes = ec2_client.describe_volumes(
      VolumeIds=[new_volume_id]
  )
  for volume in volumes['Volumes']:
    if len(volume.get('Attachments')) > 0:
      reattached_volume_count += 1
    # pprint.pprint(volume) # debug
  if reattached_volume_count == volume_count:
    global volume_reattached
    volume_reattached = True
    print(f"----------All volumes successfully reattached.---------")

schedule.every(5).seconds.do(check_reattaachment_status)

while not volume_reattached:
  schedule.run_pending()
  time.sleep(1)
else:
  schedule.clear()

#   __   ___  __  ___       __  ___            __  ___            __   ___
#  |__) |__  /__`  |   /\  |__)  |     | |\ | /__`  |   /\  |\ | /  ` |__
#  |  \ |___ .__/  |  /~~\ |  \  |     | | \| .__/  |  /~~\ | \| \__, |___
response = ec2_client.start_instances(
  InstanceIds=[instance_id]
)
#pprint.pprint(response) #debug

schedule.every(8).seconds.do(check_instance_status, False)

while not instance_restarted:
  schedule.run_pending()
  time.sleep(1)
else:
  schedule.clear()

#   __   ___       ___ ___  ___     __        __           __                   ___
#  |  \ |__  |    |__   |  |__     /  \ |    |  \    \  / /  \ |    |  |  |\/| |__
#  |__/ |___ |___ |___  |  |___    \__/ |___ |__/     \/  \__/ |___ \__/  |  | |___