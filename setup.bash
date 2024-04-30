#!/bin/bash

# Update apt package lists
sudo apt update

# Install git
sudo apt install -y git

# Add Docker repository key
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -

# Add Docker repository
sudo apt install -y software-properties-common
sudo add-apt-repository -y "deb [arch=amd64] https://download.docker.com/linux/debian bookworm stable"

# Update apt lists again
sudo apt update

# Install Docker and docker-compose
sudo apt install -y docker docker-compose
docker -v

# Clone the project from GitHub
git clone https://github.com/jovillarrealm/tejidos

cd tejidos

docker-compose up -d

echo "Django project setup (using tejidos repository) with HTTPS completed.
**Make sure you have DNS records pointing your domain name (jorgeavm.top) to your GCP instance.**

Access your project at https://jorgeavm.top"
