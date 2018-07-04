#!/bin/bash

### Docker Installation ###
# install docker-ce with edge engine
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update && sudo apt-get install -y docker-ce

# install docker-compose
sudo curl -L https://github.com/docker/compose/releases/download/1.21.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# prepare the users
sudo usermod -aG docker ubuntu

# restart to take effect
sudo service docker restart

# relog the SSH
exit

# verify docker
docker ps
### End Docker Installation ###
