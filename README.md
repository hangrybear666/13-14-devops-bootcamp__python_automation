# 13-14-devops-bootcamp__python_automation
coming up

<b><u>The course examples are:</u></b>
1. Simple Python scripts for parsing cli user inputs, manipulating xlsx files and interacting with REST APIs
2. Create VPC & several EC2 instances with terraform, monitor state and add tags /w aws boto3 sdk for python
3. Provision AWS EKS cluster /w Terraform and execute basic cluster monitoring /w aws boto3 sdk for python
4. Create Volume Snapshots for EC2 instances, then restore from backup and cleanup old backups /w aws boto3 sdk for python
5. Provision a Linode VPS & run dockerized website & monitor for downtime. Then restart VPS and notify via email /w linode_api4 for python

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

#### a. 


#### b. Enter venv and install dependencies
```bash
# has to be created only once
python3 -m venv $HOME/.venv
source $HOME/.venv/bin/activate
cd 04-ec2-volume-snapshot-restoration/
pip install -r requirements.txt
```

#### c. Execute ec2 volume creation, restoration and cleanup (deletion) scripts
```bash
python src/ec2-create-volume-snapshot.py
python src/ec2-delete-volume-snapshot.py
python src/ec2-restore-volume-snapshot.py
```

#### d. Freeeze dependencies in requirements file in case you made any changes and exit venv

```bash
cd 04-ec2-volume-snapshot-restoration/
pip freeze > requirements.txt
deactivate
```
</details>

-----

<details closed>
<summary><b>5. Provision a Linode VPS & run dockerized website & monitor for downtime. Then restart VPS and notify via email /w linode_api4 for python</b></summary>

#### a.


#### b. Enter venv and install dependencies
```bash
# has to be created only once
python3 -m venv $HOME/.venv
source $HOME/.venv/bin/activate
cd 05-monitor-and-restart-vps/
pip install -r requirements.txt
```

#### c. Execute monitoring script that restarts the VPS server once website downtime has been detected
```bash
python src/monitor-and-restart-vps.py
```

#### d. Freeeze dependencies in requirements file in case you made any changes and exit venv

```bash
cd 05-monitor-and-restart-vps/
pip freeze > requirements.txt
deactivate
```

</details>

-----
