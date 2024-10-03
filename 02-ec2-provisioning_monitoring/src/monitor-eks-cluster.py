import boto3
import pprint
from datetime import datetime, timezone

client = boto3.client('eks', region_name="eu-central-1")
clusters = client.list_clusters()['clusters']
KEY_ERROR_DEFAULT_FALLBACK = 'Not available.'
for cluster in clusters:
    response = client.describe_cluster(
        name=cluster
    )
    cluster_info = response['cluster']
    time_difference = datetime.now(timezone.utc) - cluster_info.get('createdAt', datetime.now())
    print(f"Cluster version      : {cluster_info.get('version', KEY_ERROR_DEFAULT_FALLBACK)}")
    print(f"Cluster name         : {cluster_info.get('name', KEY_ERROR_DEFAULT_FALLBACK)}")
    print(f"Cluster status       : {cluster_info.get('status', KEY_ERROR_DEFAULT_FALLBACK)}")
    print(f"Time since creation  :"
        f" {time_difference.days}days" \
        f" {int(time_difference.seconds / 3600)}hrs" \
        f" {int((time_difference.seconds % 3600) / 60)}min" \
        f" {time_difference.seconds % 60}s"
    )
    print(f"Cluster endpoint     : {cluster_info.get('endpoint', KEY_ERROR_DEFAULT_FALLBACK)}")
    print(f"---------------------------------------------------------------------------------------------------")
    print(f"Cluster tags         : {pprint.pformat(cluster_info.get('tags', KEY_ERROR_DEFAULT_FALLBACK))}")
    print(f"Amazon Resource Name : '{cluster_info.get('arn', KEY_ERROR_DEFAULT_FALLBACK)}'")
    print(f"Subnet Ids           : {cluster_info.get('resourcesVpcConfig', {}).get('subnetIds', [])}")
    print(f"Network Config       : {pprint.pformat(cluster_info.get('kubernetesNetworkConfig', {}))}")
