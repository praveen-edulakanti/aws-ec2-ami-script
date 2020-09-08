variable "aws_profile" {
  type = string
  default = "default" 
}

variable "region" {
  default     = "ap-south-1"
  description = "AWS Region where module should operate (e.g. `us-east-1`)"
}

variable "instance_id" {
  description = "AWS Instance ID which is used for creating the AMI image (e.g. `id-123456789012`)"
}

variable "ami_name" {
  type = string
}

variable "volsize" {
  type = string
}

variable "vol_id" {
  type = string
}

variable "environment" {
  type = string
}

variable "project" {
  type = string
}