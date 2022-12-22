#!/bin/bash

# Check if Admin
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi
# Check if focal fossa
source /etc/os-release
if [ $VERSION_CODENAME != "focal" ]
  then echo "Wrong OS. Use Ubuntu 20.04 Focal Fossa"
  exit
fi
# Update and upgrade repos
apt update && apt upgrade -y
wait
apt install -y gnupg2 gnupg wget
wait
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | apt-key add -
wait
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
apt update && apt install -y mongodb-org
wait
echo "mongodb-org hold" | dpkg --set-selections
echo "mongodb-org-database hold" | dpkg --set-selections
echo "mongodb-org-server hold" | dpkg --set-selections
echo "mongodb-mongosh hold" | dpkg --set-selections
echo "mongodb-org-mongos hold" | dpkg --set-selections
echo "mongodb-org-tools hold" | dpkg --set-selections
