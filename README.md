# 13-14-devops-bootcamp__python_automation
coming up

<b><u>The course examples are:</u></b>
1. Simple Python scripts for parsing cli user inputs, manipulating xlsx files and interacting with REST APIs
2. Create VPC & several EC2 instances with terraform and monitor state with aws boto3 sdk for python

<b><u>The exercise projects are:</u></b>

## Setup

### 1. Pull SCM

Pull the repository locally by running
```bash
git clone https://github.com/hangrybear666/13-14-devops-bootcamp__python_automation.git
```
### 2. Install python3 on your development machine

For debian 12 it is already preinstalled.

## Usage (course examples)

<details closed>
<summary><b>1. Simple Python scripts for parsing cli user inputs, manipulating xlsx files and interacting with REST APIs</b></summary>

#### a. Enter venv and install dependencies
```bash
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
<summary><b>2. Create VPC & several EC2 instances with terraform and monitor state with aws boto3 sdk for python</b></summary>

#### a. Create .env file with AWS credentials, Git credentials for remote server setup and any manual terraform overwrites
```bash
cd scripts/
./setup-env-vars.sh
```


#### a. Associate SSH Key to Instance
Create Public/Private Key pair so ec2-instance can add the public key to its ssh_config or use an existing key pair.

#### b. Provide custom variables and launch AWS resources
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

</details>

-----


13-14-devops-bootcamp__python_automation/02-ec2-provisioning_monitoring/terraform/.env