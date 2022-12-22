# Python & MongoDB using FastAPI
This is a simple [Python](https://www.python.org/)/[MongoDB](https://mongodb.com/) API built using [PyMongo](https://pymongo.readthedocs.io/) and [FastAPI](https://fastapi.tiangolo.com/) to use as boilerplate code for projects.  The goal of this is to create clean, easily-readable, easily-deployed, quickly-modified, and well-handled code... with decent documentation in code and READMEs.

This is meant to get a development project off to a running start.

## Requirements
- [Python](https://www.python.org/downloads/) 
  - Version 3.10.6 was used, but any 3.10 subversion should work.
- [Pip3](https://docs.python.org/3.10/installing/)
  - Version 22.0.2 was used, but any 22.0 subversion should work.
- [MongoDB v6.0 - Community Edition (CE)](https://www.mongodb.com/try/download/community)
  - No other version of this was tested.
- [MongoDB Compass](https://www.mongodb.com/docs/compass/current/install/)
  - This is a nice to have GUI interface, but not mandatory. 
  - This will help alot of troubleshooting.
- Operating Systems:
  - Ubuntu - 20.04/22.04 LTS Compatible
    - Ubuntu/Debian variants should work with slight modifications.
    - Other Linux Distros should also work with slight variations.
    - This is what this demo is based off of.
  - MacOS - Expected to work
    - Slight variations might be needed in `pyvenv.cfg` but since it's mostly BSD, it should work.
    - Haven't tested anything BSD related.
  - Windows - Pandora's Box
    - `pyvenv.cfg` will need to be modified likely... even if all requirements are installed with exact versions.
    - There may be some other versioning issues? Toss the dice.
    - The next Windows Update could bork everything. Who knows?

## Installing MongoDB
The first things we'll want to do is make sure Ubuntu Server is up to date and we install GNU Privacy Guard and Wget.
```
apt update && apt upgrade -y
apt-get install -y gnupg2 gnupg wget
```
Now that wget is installed, we are going to download and install the apt key for MongoDB and install it on our system.
```
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
```
Now we want to add the MongoDB Repo to APT so we can install it.
```
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
```
Update APT and install MongoDB.
```
sudo apt update
sudo apt install -y mongodb-org
```
Just to be on the safe side, we are going to put a hold on upgrading any releases of MongoDB.  Just incase an unattended upgrade bumps our version up and creates a breaking change.
```
echo "mongodb-org hold" | sudo dpkg --set-selections
echo "mongodb-org-database hold" | sudo dpkg --set-selections
echo "mongodb-org-server hold" | sudo dpkg --set-selections
echo "mongodb-mongosh hold" | sudo dpkg --set-selections
echo "mongodb-org-mongos hold" | sudo dpkg --set-selections
echo "mongodb-org-tools hold" | sudo dpkg --set-selections
```
Start the MongoDB Service.
```
sudo systemctl start mongod
```
Check the status of the service to make sure it is running correctly.
```
sudo systemctl status mongod
```
Now set the service to start on boot.
```
sudo systemctl enable mongod
```

## Installing MongoDB Compass
Compass is an interactive tool for querying, optimizing, and analyzing your MongoDB data. It will make working with your database extremely easy.  Download Compass:
```
wget https://downloads.mongodb.com/compass/mongodb-compass_1.33.1_amd64.deb
```
Now install that package.
```
sudo dpkg -i mongodb-compass_1.33.1_amd64.deb
```
## Installing Python & Pip
```
sudo apt install -y python3 python3-pip
```
## Installing This Repo

### Clone the Repository
```
git clone git@github.com:Michael-Free/mongodb_fastapi.git
```

### Installing Python Requirements
```
python -m pip install -r requirements.txt
```

## Running the API
```
uvicorn mongoapi:app --reload
```

# To Dos:
- [ ] Unit tests
- [ ] Possibly some await calls for mongo functions
- [ ] Rewriting a couple of functions to be more efficient
- [ ] Creating an install/deployment script for mongodb
- [ ] Better documentation
- [ ] Virtual environment setup and documentation
- [ ] Linting to make sure it confirms with python codestyles
- [ ] using black to make sure there is unified code formatting
- [ ] using bandit to cover any common vulns in the code
- [ ] Production Deployment
  - [ ] Deployment to LXD Container
  - [ ] Deployment to Docker/Podman Container
  - [ ] Deployment to Kubernetes
