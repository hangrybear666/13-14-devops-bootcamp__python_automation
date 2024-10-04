import requests
import os
import schedule
import pprint
import paramiko
import linode_api4
import time
import os
from requests.exceptions import ConnectionError, HTTPError
from dotenv import load_dotenv

# WARNING: This entire course demo is cursed, don't use any of this in production

user_input = input(f"provide absolute path to your ssh key to connect to remote VPS.\n" \
                          f"default without provided value is /home/admin/.ssh/id_ed25519\n")
ssh_key_file_path = user_input if user_input else '/home/admin/.ssh/id_ed25519'
#   ___              __   __              ___      ___               __          __        ___  __
#  |__  |\ | \  / | |__) /  \ |\ |  |\/| |__  |\ |  |     \  /  /\  |__) |  /\  |__) |    |__  /__`
#  |___ | \|  \/  | |  \ \__/ | \|  |  | |___ | \|  |      \/  /~~\ |  \ | /~~\ |__) |___ |___ .__/
file_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=file_path)

LINODE_TOKEN = os.getenv('LINODE_TOKEN')
LINODE_VPS_ID = os.getenv('LINODE_VPS_ID')
REMOTE_ADDRESS = os.getenv('REMOTE_ADDRESS')
SERVICE_USER_PW = os.getenv('SERVICE_USER_PW')
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
SERVICE_USER = os.getenv('SERVICE_USER')

#        __   __   __          __
#  |    /  \ / _` / _` | |\ | / _`
#  |___ \__/ \__> \__> | | \| \__>
def logEnvironmentVariables():
  print(f"LINODE_TOKEN {LINODE_TOKEN}")
  print(f"LINODE_VPS_ID {LINODE_VPS_ID}")
  print(f"REMOTE_ADDRESS {REMOTE_ADDRESS}")
  print(f"SERVICE_USER_PW {SERVICE_USER_PW}")
  print(f"SERVICE_USER {SERVICE_USER}")
  print(f"EMAIL_ADDRESS {EMAIL_ADDRESS}")
  print(f"EMAIL_PASSWORD {EMAIL_PASSWORD}")

def logServerInfo():
  client = linode_api4.LinodeClient(LINODE_TOKEN)
  nginx_server = client.load(linode_api4.Instance, LINODE_VPS_ID)
  print(f"--SERVER INFO-----------------------------")
  print(f"----------------image: {nginx_server.image}")
  print(f"----------------created: {nginx_server.created}")
  print(f"----------------region: {nginx_server.region}")
  print(f"----------------disk: {nginx_server.specs.disk}---------------")
  print(f"----------------memory: {nginx_server.specs.memory}--------------")
  print(f"----------------vcpus: {nginx_server.specs.vcpus}------------------")
  print(f"----------------gpus: {nginx_server.specs.gpus}-------------------")
  print(f"----------------transfer: {nginx_server.specs.transfer}------------")
  print(f"----------------status: {nginx_server.status}-----------")

#   __   ___  __  ___       __  ___     __   ___  __        ___  __    /  __   __       ___              ___  __
#  |__) |__  /__`  |   /\  |__)  |     /__` |__  |__) \  / |__  |__)  /  /  ` /  \ |\ |  |   /\  | |\ | |__  |__)
#  |  \ |___ .__/  |  /~~\ |  \  |     .__/ |___ |  \  \/  |___ |  \ /   \__, \__/ | \|  |  /~~\ | | \| |___ |  \
def restart_server_and_container():
    # restart linode server
    print('Rebooting the server...')
    client = linode_api4.LinodeClient(LINODE_TOKEN)
    nginx_server = client.load(linode_api4.Instance, LINODE_VPS_ID)
    nginx_server.reboot()

    # restart the application
    while True:
        nginx_server = client.load(linode_api4.Instance, LINODE_VPS_ID)
        if nginx_server.status == 'running':
            time.sleep(5)
            restart_container()
            break
        else:
            time.sleep(2)

def restart_container():
    print('Restarting the application...')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=REMOTE_ADDRESS, username=SERVICE_USER, key_filename=ssh_key_file_path)
    stdin, stdout, stderr = ssh.exec_command('docker stop my-nginx | true && docker rm my-nginx | true && docker run -d --name my-nginx -p 8081:80 nginx')
    print(f"Restarted {stdout.readlines()}")
    ssh.close()
    time.sleep(10)

#         __         ___  __   __          __           __   __   __
#   |\/| /  \ |\ | |  |  /  \ |__) | |\ | / _`    |    /  \ /  \ |__)
#   |  | \__/ | \| |  |  \__/ |  \ | | \| \__>    |___ \__/ \__/ |
def monitor_application():
    try:
        response = requests.get(f"http://{REMOTE_ADDRESS}:8081/")
        if response.status_code == 200:
            print('Website returned Status 200 OK')
        else:
            print('Website not reachable.')
            print('Restarting container.')
            restart_container()
    except ConnectionError as connErr:
        print(f'Connection error occured: {connErr}')
        print('Restarting container.')
        restart_container()
    except HTTPError as e:
      print(f"HTTP error occurred: {e}")
      print('Restarting container.')
      restart_container()
    except Exception as ex:
        print(f'Generic Exception occured: {ex}')
        print(f'Rebooting server and then restarting container.')
        restart_server_and_container()

#   ___            __  ___    __           __                  __
#  |__  |  | |\ | /  `  |  | /  \ |\ |    /  `  /\  |    |    /__`
#  |    \__/ | \| \__,  |  | \__/ | \|    \__, /~~\ |___ |___ .__/
# logEnvironmentVariables()
# logServerInfo()

schedule.every(5).seconds.do(monitor_application)
while True:
    schedule.run_pending()
    time.sleep(2)
