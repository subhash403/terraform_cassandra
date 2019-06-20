from fabric import Connection
#from fabric.contrib.files import exists
import csv
import time, sys
import argparse
import os
import time
from patchwork.files import exists
#Arguments Parsing
parser=argparse.ArgumentParser()
parser.add_argument('--keyname', required= True)
parser.add_argument('--file',required=True)
args = parser.parse_args()


#seedips = instance_config['file_name']
key_key = args.keyname
print(key_key)
print(args.file)


ip_list=open('ips.txt')
line=ip_list.readline()
cnt = 1
ips=[]
while line:
    ipsec=line.strip()
    ips.append(ipsec)
    line = ip_list.readline()
    cnt += 1
print(ips)

ip_list_private=open('ips2.txt')
#print (ip_list_private)
line_private=ip_list_private.readline()
cnt_private = 1
print ("my privtae ip",line_private)
ips_private=[]
while line_private:
    ipsec_private=line_private.strip()
    ips_private.append(ipsec_private)
    print ("my private ips",ips_private)
    line_private = ip_list_private.readline()
    cnt_private += 1
print ("my ipsss",ips_private)




def setup_cluster():
    print("setup cluster")
    print(ips_private)
    ips2=str(ips_private)
    cluster_ip_list = ips2
    print(ips2)
    seeds=ips2.replace("\'","").replace("[","").replace("]","").replace(" ","")
    print("seeds:- %s"%(seeds))
    for ip in ips:
        
        currentip=ip.replace("\r\n","")
        print(currentip)
        c=Connection(host="ubuntu@%s"%currentip,connect_kwargs={"key_filename":key_key})
        #c=Connection(host="ec2-user@13.235.19.179",connect_kwargs={"key_filename":key_key}) 
        #c=Connection(host="easyway@192.168.1.128",connect_kwargs={"key_filename":key_key})
        print("connected to",currentip)
        c.run('pwd') 
        DIR_1="/etc/cassandra"
        while not exists(c,DIR_1):
            time.sleep(120)
        
        c.sudo("service cassandra stop")

        c.sudo("sed -i \'s/127.0.0.1/%s/\' /etc/cassandra/cassandra.yaml"%(seeds))

        privateip=c.run("ip addr | grep \'state UP\' -A2 | tail -n1 | awk \'{print $2}\' | cut -f1 -d\'/\'")

        ipp=str(privateip.stdout).replace("\n","")

        c.sudo("sed -i \'s/rpc_address: localhost/rpc_address: %s/\' /etc/cassandra/cassandra.yaml"%(ipp))

        #c.sudo("sed -i \'s/# broadcast_address: 1.2.3.4/broadcast_address: %s/\' /etc/cassandra/cassandra.yaml"%(currentip))

        c.sudo("sed -i \'s/listen_address: localhost/listen_address: %s/\' /etc/cassandra/cassandra.yaml"%(ipp))

        c.sudo("rm -rf /var/run/cassandra/*")

        c.sudo("rm -rf /var/lock/subsys/cassandra")

        c.sudo("service cassandra stop")
        
        c.sudo("service cassandra start")

if __name__ == '__main__':
        setup_cluster()

