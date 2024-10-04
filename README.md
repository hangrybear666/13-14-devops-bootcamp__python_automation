# 13-14-devops-bootcamp__python_automation
Boto3 SDK Python scripts for automating AWS tasks like monitoring EC2 instances & EKS clusters. Creating backups, restoring from backups, notifications and restarting servers.

<b><u>The course examples are:</u></b>
1. Simple Python scripts for parsing cli user inputs, manipulating xlsx files and interacting with REST APIs
2. Create VPC & several EC2 instances with terraform, monitor state and add tags /w aws boto3 sdk for python
3. Provision AWS EKS cluster /w Terraform and execute basic cluster monitoring /w aws boto3 sdk for python
4. Create Volume Snapshots for EC2 instances, then restore from backup and cleanup old backups /w aws boto3 sdk for python
5. Provision a Linode VPS & run dockerized website & monitor for downtime. Then restart VPS & container /w linode_api4 for python

<!-- <b><u>The exercise projects are:</u></b> -->

## Setup

### 1. Pull SCM

Pull the repository locally by running
```bash
git clone https://github.com/hangrybear666/13-14-devops-bootcamp__python_automation.git
```
### 2. Install python3 on your development machine

For debian 12 it is already preinstalled.

### 3. Install terraform on your development machine

For debian 12 you can use the following installation script, otherwise follow https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli
```bash
cd scripts/ && ./install-terraform.sh
```

## Usage (course examples)

<details closed>
<summary><b>1. Simple Python scripts for parsing cli user inputs, manipulating xlsx files and interacting with REST APIs</b></summary>

#### a. Enter venv and install dependencies
```bash
# has to be created only once
python3 -m venv $HOME/.venv
source $HOME/.venv/bin/activate
cd 01-python-basics/
pip install -r requirements.txt
```

#### b. Execute basic demo modules
```bash
python src/countdown.py
python src/csv-manipulation.py
python src/http-requests.py
```

#### c. Freeeze dependencies in requirements file in case you made any changes and exit venv

```bash
cd 01-python-basics/
pip freeze > requirements.txt
deactivate
```

</details>

-----


<details closed>
<summary><b>2. Create VPC & several EC2 instances with terraform, monitor state and add tags /w aws boto3 sdk for python</b></summary>

#### a. Create .env file with AWS credentials, Git credentials for remote server setup and any manual terraform overwrites
```bash
cd scripts/
./setup-env-vars.sh
```

#### b. Associate SSH Key to Instance
Create Public/Private Key pair so ec2-instance can add the public key to its ssh_config or use an existing key pair.

#### c. Provide custom variables and launch AWS resources
Create `02-ec2-provisioning_monitoring/terraform/terraform.tfvars` file and change any desired variables by overwriting the default values within `variables.tf`
```bash
my_ips               = ["62.xxx.xxx.251/32", "3.xxx.xxx.109/32"]
public_key_location  = "~/.ssh/id_ed25519.pub"
private_key_location = "~/.ssh/id_ed25519"
instance_count       = 3
```

```bash
# source environment variables, especially AWS access keys
cd 02-ec2-provisioning_monitoring/terraform/
source .env
terraform init
terraform apply
```

#### d. Enter venv and install dependencies
```bash
# has to be created only once
python3 -m venv $HOME/.venv
source $HOME/.venv/bin/activate
cd 02-ec2-provisioning_monitoring/
pip install -r requirements.txt
```

#### e. Execute ec2 monitoring script and script to add incremental tags to ec2-instances
```bash
python src/monitor-ec2.py
python src/add-ec2-tags.py
```

#### f. Freeeze dependencies in requirements file in case you made any changes and exit venv

```bash
cd 02-ec2-provisioning_monitoring/
pip freeze > requirements.txt
deactivate
```

</details>

-----

<details closed>
<summary><b>3. Provision AWS EKS cluster /w Terraform and execute basic cluster monitoring /w aws boto3 sdk for python</b></summary>

#### a. Create EKS cluster with terraform by following project 3 in the terraform repo

Follow the instructions for provisioning EKS cluster with terraform
https://github.com/hangrybear666/12-devops-bootcamp__terraform.git


#### b. Enter venv and install dependencies
```bash
# has to be created only once
python3 -m venv $HOME/.venv
source $HOME/.venv/bin/activate
cd 02-ec2-provisioning_monitoring/
pip install -r requirements.txt
```

#### c. Execute ec2 monitoring script and script to add incremental tags to ec2-instances
```bash
python src/monitor-eks-cluster.py
```

#### d. Freeeze dependencies in requirements file in case you made any changes and exit venv

```bash
cd 02-ec2-provisioning_monitoring/
pip freeze > requirements.txt
deactivate
```
</details>

-----

<details closed>
<summary><b>4. Create Volume Snapshots for EC2 instances, then restore from backup and cleanup old backups /w aws boto3 sdk for python</b></summary>

#### a. Create EC2 instance/s by following step 2. Create VPC & several EC2 instances with terraform

To test scripts on a single instance first, you can overwrite defaults before applying the terraform config
```bash
export TF_VAR_instance_count=1
```

#### b. Enter venv and install dependencies
```bash
# has to be created only once
python3 -m venv $HOME/.venv
source $HOME/.venv/bin/activate
cd 04-ec2-volume-snapshot-restoration/
pip install -r requirements.txt
```

#### c. Create ec2 volume snapshots for 1-n instances

<u>The steps are:</u>

- Stop instances with user input provided name tag
- Detach Volumes & Check for successful detachment
- Create Snapshots & Check for Snapshot initialization
- Attach Volumes & Check for successful attachment
- Start instances & Check for launch status
```bash
python src/ec2-create-volume-snapshot.py
```


#### d. Cleanup (Delete) volume snapshots not needed anymore

<u>The steps are:</u>

- Read user input to limit deletion to ec2 Name tag
- Delete snapshots belonging to unattached volumes
- Delete all but the newest snapshot for each volume
```bash
python src/ec2-delete-volume-snapshot.py
```


#### e. Restore EC2 instance from snapshot
<u>The steps are:</u>

- Read user input to limit restore to ec2 instance id
- Read user input to decide whether to delete current volume after restore
- Stop instances with user input provided instance id
- Detach Volume & Check for successful detachment
- Fetch Latest Snapshot of Volume
- Create Volume from Latest Snapshot
- Attach Volume & Check for successful attachment
- Start instance & Check for launch status
- Delete prior volume if user input has confirmed
```bash
python src/ec2-restore-volume-snapshot.py
```

#### f. Freeeze dependencies in requirements file in case you made any changes and exit venv

```bash
cd 04-ec2-volume-snapshot-restoration/
pip freeze > requirements.txt
deactivate
```
</details>

-----

<details closed>
<summary><b>5. Provision a Linode VPS & run dockerized website & monitor for downtime. Then restart VPS & container /w linode_api4 for python</b></summary>

#### a. Create a Linode VPS Server by following the bonus project 1) in the terraform repo from steps a-d)

Follow the instructions for provisioning Linode VPS (while skipping the jenkins-installation script in step d)
https://github.com/hangrybear666/12-devops-bootcamp__terraform.git


#### b. Create .env file with your Linode Token, Public IP, VPS ID and PW

In the path `05-monitor-and-restart-vps/.env`
```bash
LINODE_TOKEN=xxx
LINODE_VPS_ID=1234
REMOTE_ADDRESS=172.xxx.xxx.xxx
SERVICE_USER_PW=changeit
```

#### c. Make sure to forward port 8081 in your linode remote firewall

#### d. SSH into your remote and run nginx container on port 8081

*Note:* For the python script to work, name `my-nginx` is mandatory.
```bash
ssh jenkins-runner@172.105.75.118 \
docker run -d --name my-nginx -p 8081:80 nginx
```

#### e. Enter venv and install dependencies
```bash
# has to be created only once
python3 -m venv $HOME/.venv
source $HOME/.venv/bin/activate
cd 05-monitor-and-restart-vps/
pip install -r requirements.txt
```

#### f. Execute monitoring script that restarts the VPS server once website downtime has been detected
```bash
python src/monitor-and-restart-vps.py
```

#### g. Freeeze dependencies in requirements file in case you made any changes and exit venv

```bash
cd 05-monitor-and-restart-vps/
pip freeze > requirements.txt
deactivate
```

</details>

-----
