from fabric import Connection
import csv
import time, sys
import argparse

#Arguments Parsing
parser=argparse.ArgumentParser()
parser.add_argument('--keyname', required= True)
parser.add_argument('--file',required=True)
args = parser.parse_args()


#seedips = instance_config['file_name']
key_key = args.keyname
print(key_key)
print(args.file)

ip_list=open('%s.txt'%(args.file))
for ips in ip_list:
    iplist=str(ips).split(",")

def setup_cluster():
    cluster_ip_list = iplist
    seeds=ips.replace("\r\n","")
    print("seeds",seeds)
    for ip in cluster_ip_list:
        currentip=ip.replace("\r\n","")
        c=Connection(host="ubuntu@%s"%currentip,connect_kwargs={"key_filename":key_key})
        print("connected to",currentip)
        c.run('pwd')
        # sudo("sed -i 's/127.0.0.1/%s/' /etc/dse/cassandra/cassandra.yaml"%(seeds))
        c.sudo("service ssh status",user="easyway",password="easyway@123")

        print("sed")
        c.sudo("sed -i \'s/127.0.0.1/%s/\' /etc/dse/cassandra/cassandra.yaml"%(seeds),user="ec2-user")

        #privateip=c.run("ip addr | grep \'state UP\' -A2 | tail -n1 | awk \'{print $2}\' | cut -f1 -d\'/\'")

        #prip=str(privateip.stdout)

        #print(prip)

        #c.sudo("sed -i \'s/listen_address: localhost/listen_address: %s/\' /etc/dse/cassandra/cassandra.yaml"%(prip),user="easyway")

        c.sudo("sed -i \'s/rpc_address: localhost/rpc_address: 0.0.0.0/\' /etc/dse/cassandra/cassandra.yaml",user="ec2-user")

        c.sudo("sed -i \'s/# broadcast_address: 1.2.3.4/broadcast_address: %s/\' /etc/dse/cassandra/cassandra.yaml"%(currentip),user="ec2-user")

        c.sudo("rm -rf /var/run/cassandra/*",user="ec2-user")

        c.sudo("rm -rf /var/lock/subsys/cassandra",user="ec2-user")

        c.sudo("service ssh status",user="ec2-user")


if __name__ == '__main__':
        setup_cluster()

