#!/bin/bash
sudo apt-get update
sudo apt install openjdk-8-jre -y
echo "JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:bin/java::")" | sudo tee -a /etc/profile
source /etc/profile
echo $JAVA_HOME
echo "deb http://www.apache.org/dist/cassandra/debian 311x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
curl https://www.apache.org/dist/cassandra/KEYS | sudo apt-key add -
sudo apt-get update -y
sudo apt-key adv --keyserver pool.sks-keyservers.net --recv-key A278B781FE4B2BDA -y
sudo apt-get update -y 
sudo apt-get install cassandra -y 
sudo DEBIAN_FRONTEND=noninteractive apt-get install python-pip -y
pip install cassandra-driver
service cassandra restart
