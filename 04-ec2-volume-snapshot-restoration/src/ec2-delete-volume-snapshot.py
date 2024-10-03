import boto3
import datetime
import pprint
import time
import os
from operator import itemgetter

ec2_client = boto3.client('ec2', region_name="eu-central-1")

#   __        __   __                          __   __
#  / _` |    /  \ |__)  /\  |       \  /  /\  |__) /__`
#  \__> |___ \__/ |__) /~~\ |___     \/  /~~\ |  \ .__/
server_tag = input("Enter the ec2 servers 'Name' Tag Value to clean up snapshots for \n(default on empty string = dev-server): ")
attached_volume_ids = []
deleted_snapshot_ids = []

#   __        ___  __          __   ___       ___                ___            __  ___            __   ___     __       ___
#  /  \ |  | |__  |__) \ /    |__) |__  |    |__  \  /  /\  |\ |  |     | |\ | /__`  |   /\  |\ | /  ` |__     |  \  /\   |   /\
#  \__X \__/ |___ |  \  |     |  \ |___ |___ |___  \/  /~~\ | \|  |     | | \| .__/  |  /~~\ | \| \__, |___    |__/ /~~\  |  /~~\
selected_tag = 'dev-server' if not server_tag or server_tag == "" else server_tag
reservations = ec2_client.describe_instances(
  Filters=[
    {
      'Name': 'tag:Name',
      'Values': [f"{selected_tag}"] # set by terraform apply in project 2)
    },
  ],
)['Reservations']

for reservation in reservations:
  for instance in reservation.get('Instances', []):
    block_device_mappings = instance.get('BlockDeviceMappings', [])
    for mapping in block_device_mappings:
      ebs = mapping.get('Ebs', {})
      volume_id = ebs.get('VolumeId')
      if volume_id:
        attached_volume_ids.append(volume_id)
attached_volume_ids_set = set(attached_volume_ids)
#   __   ___       ___ ___  ___                   ___ ___       __        ___  __      __             __   __        __  ___  __
#  |  \ |__  |    |__   |  |__     |  | |\ |  /\   |   |   /\  /  ` |__| |__  |  \    /__` |\ |  /\  |__) /__` |__| /  \  |  /__`
#  |__/ |___ |___ |___  |  |___    \__/ | \| /~~\  |   |  /~~\ \__, |  | |___ |__/    .__/ | \| /~~\ |    .__/ |  | \__/  |  .__/
initial_snapshots = ec2_client.describe_snapshots(
  OwnerIds=['self'],
  # Filters=[
  #   {
  #     'Name': 'tag:created_by',
  #     'Values': [f"boto3-sdk"]
  #   },
  # ],
).get('Snapshots', {})
print(f"-------------{len(initial_snapshots)} snapshots present initially.---------------------")
for snapshot in initial_snapshots:
  if snapshot.get('VolumeId') not in attached_volume_ids_set:
    snapshot_id = snapshot['SnapshotId']
    deleted_snapshot_ids.append(snapshot_id)
    print(f"Deleting unattached snapshot {snapshot_id} from volume {snapshot['VolumeId']}")
    response = ec2_client.delete_snapshot(
      SnapshotId=snapshot_id
    )
    # pprint.pprint(response) #debug

if len(deleted_snapshot_ids) > 0:
  for n in range(1, 6):
    time.sleep(3)
    print(f"waiting for snapshot deletion...")
  remaining_snapshots = ec2_client.describe_snapshots(
    OwnerIds=['self'],
  ).get('Snapshots', {})
  print(f"-------------{len(remaining_snapshots)} snapshots remain.------------------------------")
else:
  print(f"-------------No unattached snapshots to delete.-----------------")

#   __   ___ ___                 __                         ___       ___  __  ___     __             __   __        __  ___
#  |__) |__   |   /\  | |\ |    /  \ |\ | |    \ /    |\ | |__  |  | |__  /__`  |     /__` |\ |  /\  |__) /__` |__| /  \  |
#  |  \ |___  |  /~~\ | | \|    \__/ | \| |___  |     | \| |___ |/\| |___ .__/  |     .__/ | \| /~~\ |    .__/ |  | \__/  |
for volume_id in attached_volume_ids_set:
    individual_volume_snapshots = ec2_client.describe_snapshots(
        OwnerIds=['self'],
        Filters=[
            {
                'Name': 'volume-id',
                'Values': [volume_id]
            }
        ]
    ).get('Snapshots',{})

    sorted_by_date = sorted(individual_volume_snapshots, key=itemgetter('StartTime'), reverse=True)
    print(f"-------------{volume_id} has {len(individual_volume_snapshots)} snapshots.-------------")
    print(f"-------------deleting all but the newest snapshot.--------------")
    for snap in sorted_by_date[1:]:
        response = ec2_client.delete_snapshot(
            SnapshotId=snap['SnapshotId']
        )
        try:
          print(f"-------------delete status code: {response.get('ResponseMetadata').get('HTTPStatusCode')}----------------------------")
        except:
          print("xxxxxxxxxxxxxxxxxxxxxxxx Exception in deletion response. xxxxxxxxxxxxxxxxxxxxxxxxxx")
