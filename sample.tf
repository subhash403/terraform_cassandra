provider "aws" {
    region = "us-east-1"
}

#For creating Security group

resource "aws_security_group" "cassandra_cluster1" {
    name = "cassandra_cluster"
    description = "Allow  ports 22,7000,9160,9042"
    vpc_id = "vpc-906a11f4"
    
ingress{
        from_port = "${var.allow_ssh}"
        to_port = "${var.allow_ssh}"
        protocol = "tcp"
        cidr_blocks =["0.0.0.0/0"]
    }
    ingress{
        from_port = "${var.allow_7000}"
        to_port = "${var.allow_7000}"
        protocol = "tcp"
        cidr_blocks =["0.0.0.0/0"]
    }
    ingress{
        from_port = "${var.allow_9042}"
        to_port = "${var.allow_9042}"
        protocol = "tcp"
        cidr_blocks =["0.0.0.0/0"]
    }
    ingress{
        from_port = "${var.allow_9160}"
        to_port = "${var.allow_9160}"
        protocol = "tcp"
        cidr_blocks =["0.0.0.0/0"]
    }

    egress{
        from_port = 0
        to_port = 0
        protocol ="-1"
        cidr_blocks=["0.0.0.0/0"]
    }
}


#get the security groupname 

output "sg_id" {
  value = "${aws_security_group.cassandra_cluster1.*.id}"
}

#resource "aws_key_pair" "terraform-demo" {
#  key_name   = "terraform-demo"
#  public_key = "${file("id_rsa.pub")}"
#}

resource "aws_instance" "cassandra_instance" {
    ami="${var.ami_id}"
    count=2
    instance_type ="${var.type_of_instance}"
    key_name = "oracledb"
    associate_public_ip_address = true
    subnet_id ="${var.subnet_id}"
    user_data  = "${file("script.sh")}"
    root_block_device {
        volume_size           = 8
        volume_type           = "gp2"
    }
    vpc_security_group_ids = ["${aws_security_group.cassandra_cluster1.id}"]
    tags = {
        Name = "${var.tag_of_instance} ${count.index}"
    }

#    connection {
#        user        = "ec2-user"
#        private_key = "${file(var.private_key_path)}"
#        host = "self.public_ip"
#    }
    
#provisioner "local-exec" {
#                command="python script.py"
#    }   
}

#resource "null_resource" "save_ip_to_local" {
#  depends_on = ["aws_instance.cassandra_instance"]
#    provisioner "local-exec" {
#        command = "echo '${join("\n", formatlist("private=%v", aws_instance.cassandra_instance.*.private_ip))}'>> \"ips.txt\""
#    }
#}
resource "local_file" "cassandra_localfile1" {
filename = "ips2.txt"
content  =<<EOT
%{ for ip in aws_instance.cassandra_instance.*.private_ip ~}
${ip}
%{ endfor ~}
EOT
}

resource "local_file" "cassandra_localfile" {
filename = "ips.txt"
content  =<<EOT
%{ for ip in aws_instance.cassandra_instance.*.public_ip ~}
${ip}
%{ endfor ~}
EOT
}

resource    "null_resource" "cassandra_instance"{
    triggers = {
         cluster_instance_ids = "${join(",", aws_instance.cassandra_instance.*.public_ip)}"
  }
    provisioner "local-exec" {
                command="python3.7 script.py --keyname /home/easyway/snap/skype/common/oracledb.pem --file ips"
    }  
}

