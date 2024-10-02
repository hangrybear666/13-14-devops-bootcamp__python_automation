#!/bin/bash

# extract the current directory name from pwd command (everything behind the last backslash
CURRENT_DIR=$(pwd | sed 's:.*/::')
if [ "$CURRENT_DIR" != "scripts" ]
then
  echo "please change directory to scripts folder and execute the shell script again."
  exit 1
fi

read -p "Please provide your AWS_ACCESS_KEY_ID: " ACCESS_KEY
read -p "Please provide your AWS_SECRET_ACCESS_KEY: " SECRET_KEY
read -p "Please provide your GIT_USER_NAME: " GIT_USER_NAME
read -p "Please provide your GIT_USER_EMAIL: " GIT_USER_EMAIL
read -p "Please provide your GIT_TOKEN: " GIT_TOKEN

AWS_REGION="eu-central-1"
AWS_OUTPUT_FORMAT="json"
cd ..
# create terraform .env file for ec2 project
touch 02-ec2-provisioning_monitoring/terraform/.env
echo "# AWS CONFIG
AWS_ACCESS_KEY_ID=$ACCESS_KEY
AWS_SECRET_ACCESS_KEY=$SECRET_KEY
AWS_REGION=$AWS_REGION
# TF VARS
TF_VAR_EXAMPLE_VAR="example-env-var"
" > 02-ec2-provisioning_monitoring/terraform/.env
echo "Created .env file with terraform secrets in" && echo "$(pwd)/02-ec2-provisioning_monitoring/terraform/" && echo "--------------------------------"

#create ec2 .env file deployed on remote instance
touch 02-ec2-provisioning_monitoring/terraform/payload/.env
echo "# GIT CONFIG
GIT_USER_NAME=$GIT_USER_NAME
GIT_USER_EMAIL=$GIT_USER_EMAIL
GIT_TOKEN=$GIT_TOKEN
# AWS CONFIG
AWS_ACCESS_KEY_ID=$ACCESS_KEY
AWS_ACCESS_KEY_SECRET=$SECRET_KEY
AWS_REGION=$AWS_REGION
AWS_OUTPUT_FORMAT=$AWS_OUTPUT_FORMAT
" > 02-ec2-provisioning_monitoring/terraform/payload/.env
echo "Created .env file with ec2 secrets in" && echo "$(pwd)/02-ec2-provisioning_monitoring/terraform/payload/" && echo "--------------------------------"
