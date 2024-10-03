import boto3
import schedule
import datetime
import pprint
import time
import sys

ec2_client = boto3.client('ec2', region_name="eu-central-1")

instance_ids = []
volume_ids = []
instance_volume_map = {}
all_instances_stopped = False
all_volumes_detached = False
all_volumes_reattached = False
all_instances_restarted = False

#   __   ___ ___       __
#  /__` |__   |  |  | |__)
#  .__/ |___  |  \__/ |
def query_instances():
  return ec2_client.describe_instances(
    Filters=[
      {
        'Name': 'tag:Name',
        'Values': ['dev-server'] # set by terraform apply in project 2)
      },
    ],
  )['Reservations']

instance_reservations = query_instances()

for res in instance_reservations:
  instances = res['Instances']
  for ins in instances:
    instance_id = ins['InstanceId']
    volume_id = ins.get('BlockDeviceMappings')[0].get('Ebs').get('VolumeId')
    # pprint.pprint(ins) # debug
    instance_ids.append(instance_id)
    volume_ids.append(volume_id)
    instance_volume_map[instance_id] = volume_id

#   __  ___  __   __             __  ___            __   ___  __
#  /__`  |  /  \ |__)    | |\ | /__`  |   /\  |\ | /  ` |__  /__`
#  .__/  |  \__/ |       | | \| .__/  |  /~~\ | \| \__, |___ .__/
response = ec2_client.stop_instances(
  InstanceIds=instance_ids,
  Hibernate=False,
  DryRun=False,
  Force=False # not recommended, can lead to data loss
)

def check_instance_status(isStart):
  instance_count = len(instance_ids)
  stopped_instance_count = 0
  statuses = ec2_client.describe_instance_status(
    InstanceIds=instance_ids,
    IncludeAllInstances=True
  )
  for status in statuses['InstanceStatuses']:
    state = status['InstanceState']['Name']
    if (state == 'stopped'):
      stopped_instance_count += 1
    print(f"Instance '{status['InstanceId']}' is [{state}] with instance status [{status['InstanceStatus']['Status']}] and system status [{status['SystemStatus']['Status']}]")
  if isStart and stopped_instance_count == instance_count:
    global all_instances_stopped
    all_instances_stopped = True
    print(f"----------All instances successfully stopped.----------")
  elif not isStart and stopped_instance_count == 0:
    global all_instances_restarted
    all_instances_restarted = True
    print(f"----------All instances successfully restarted.--------")

schedule.every(5).seconds.do(check_instance_status, True)

while not all_instances_stopped:
  schedule.run_pending()

#   __   ___ ___       __                __                   ___  __
#  |  \ |__   |   /\  /  ` |__|    \  / /  \ |    |  |  |\/| |__  /__`
#  |__/ |___  |  /~~\ \__, |  |     \/  \__/ |___ \__/  |  | |___ .__/
for instance_id in instance_ids:
  response = ec2_client.detach_volume(
      VolumeId=instance_volume_map[instance_id],
  )
  # pprint.pprint(response) # debug

def check_detachment_status():
    volume_count = len(volume_ids)
    detached_volume_count = 0
    volumes = ec2_client.describe_volumes(
        VolumeIds=volume_ids
    )
    for volume in volumes['Volumes']:
      if len(volume.get('Attachments')) == 0:
        detached_volume_count += 1
      # pprint.pprint(volume) # debug
    if detached_volume_count == volume_count:
      global all_volumes_detached
      all_volumes_detached = True
      print(f"----------All volumes successfully detached.-----------")

schedule.every(5).seconds.do(check_detachment_status)

while not all_volumes_detached:
    schedule.run_pending()

#   __   __   ___      ___  ___     __             __   __        __  ___
#  /  ` |__) |__   /\   |  |__     /__` |\ |  /\  |__) /__` |__| /  \  |
#  \__, |  \ |___ /~~\  |  |___    .__/ | \| /~~\ |    .__/ |  | \__/  |
for volume_id in instance_volume_map.values():
  new_snapshot = ec2_client.create_snapshot(
      Description=f"Snapshot at {datetime.datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} for {volume_id}",
      VolumeId=volume_id,
      TagSpecifications=[
          {   'ResourceType': 'snapshot',
              'Tags': [
                  {
                      'Key': 'created_by',
                      'Value': 'boto3-sdk'
                  },
                  {
                      'Key': 'volume_id',
                      'Value': f"{volume_id}"
                  },
              ]
          },
      ],
  )
  # pprint.pprint(new_snapshot) # debug

for n in range(1, 4):
  time.sleep(5)
  print(f"waiting for snapshot creation...")

response = ec2_client.describe_snapshots(
  Filters=[
    {
      'Name': 'tag:created_by',
      'Values': ['boto3-sdk']
    },
  ],
)
pprint.pprint(response) # debug

#   __   ___      ___ ___       __                __                   ___  __
#  |__) |__   /\   |   |   /\  /  ` |__|    \  / /  \ |    |  |  |\/| |__  /__`
#  |  \ |___ /~~\  |   |  /~~\ \__, |  |     \/  \__/ |___ \__/  |  | |___ .__/
for instance_id in instance_ids:
  response = ec2_client.attach_volume(
      Device='/dev/xvda', # for root device
      InstanceId=instance_id,
      VolumeId=instance_volume_map[instance_id],
  )
  # pprint.pprint(response) # debug

for n in range(1, 4):
  time.sleep(3)
  print(f"waiting for volume attachment...")

def check_reattaachment_status():
    volume_count = len(volume_ids)
    reattached_volume_count = 0
    volumes = ec2_client.describe_volumes(
        VolumeIds=volume_ids
    )
    for volume in volumes['Volumes']:
      if len(volume.get('Attachments')) > 0:
        reattached_volume_count += 1
      # pprint.pprint(volume) # debug
    if reattached_volume_count == volume_count:
      global all_volumes_reattached
      all_volumes_reattached = True
      print(f"----------All volumes successfully reattached.---------")

schedule.every(5).seconds.do(check_reattaachment_status)

while not all_volumes_reattached:
    schedule.run_pending()

#   __   ___  __  ___       __  ___            __  ___            __   ___  __
#  |__) |__  /__`  |   /\  |__)  |     | |\ | /__`  |   /\  |\ | /  ` |__  /__`
#  |  \ |___ .__/  |  /~~\ |  \  |     | | \| .__/  |  /~~\ | \| \__, |___ .__/
response = ec2_client.start_instances(
    InstanceIds=instance_ids
)
#pprint.pprint(response) #debug

schedule.every(5).seconds.do(check_instance_status, False)

while not all_instances_restarted:
  schedule.run_pending()