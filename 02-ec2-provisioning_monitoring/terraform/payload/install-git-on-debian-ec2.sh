#/bin/bash

which_git=$(which git)

echo "Git Installation:"
echo "-----------------"
if [ ! -z "$which_git" ]
  then
    echo "git install path: $which_git"
    echo "$(git --version)"
  else
    echo "Installting git
    "
    sudo apt update
    sudo apt -y install git
fi

# Save path for copying .env later
git_script_path=$(pwd)
# Set Environment Secrets
source .env

cd $HOME
if [ -d git/ ]
  then
    echo "" && echo "git directory found." && echo ""
  else
    mkdir git
fi

cd git

# Clone ec2-debian-init repository
if [ -d ec2-debian-init ]
then
  echo "" && echo "ec2-debian-init repository found"
  exit 1
else
  git clone https://$GIT_TOKEN@github.com/hangrybear666/ec2-debian-init.git
  cd ec2-debian-init
  cp $git_script_path/.env .
  git remote set-url origin https://$GIT_TOKEN@github.com/hangrybear666/ec2-debian-init.git
  git remote set-url origin --push https://$GIT_TOKEN@github.com/hangrybear666/ec2-debian-init.git
  echo ""
  echo "Initialized Git Repository and moved .env file"
fi

# Configure Git
sudo git config --system user.name "$GIT_USER_NAME"
sudo git config --system user.email "$GIT_USER_EMAIL"
#sudo git config --system core.editor vim

echo "Git Configured:"
echo "---------------"
git config --list
