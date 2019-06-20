variable "allow_ssh" {
  description = "The region to provision AWS resources in."
  default=22
}

variable "allow_7000" {
  description = "The region to provision AWS resources in."
  default=7000
}

variable "allow_9160" {
  description = "The region to provision AWS resources in."
  default=9160
}

variable "allow_9042" {
  description = "The region to provision AWS resources in."
  default=9042
}

variable "type_of_instance"{
    description ="instance type"
    default="t2.micro"
}

variable "ami_id" {
    description ="providing ami id "
    default="ami-024a64a6685d05041"
  
}


variable "subnet_id" {
    description ="providing subnetid"
    default="subnet-0496d2c62bdb0157b"
  
}

variable "tag_of_instance" {
    description = "providing tag to the instance"
    default="cassandra_instance"
}



