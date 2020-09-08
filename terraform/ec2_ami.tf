locals {
  timestamp = "${timestamp()}"
  timestamp_no_hyphens = "${replace("${local.timestamp}", "-", "")}"
  timestamp_no_spaces = "${replace("${local.timestamp_no_hyphens}", " ", "")}"
  timestamp_no_t = "${replace("${local.timestamp_no_spaces}", "T", "")}"
  timestamp_no_z = "${replace("${local.timestamp_no_t}", "Z", "")}"
  timestamp_no_colons = "${replace("${local.timestamp_no_z}", ":", "")}"
  timestamp_sanitized = "${local.timestamp_no_colons}"
}


resource "aws_ami_from_instance" "create_ami" {
  name               =  format("${var.ami_name}-%s", "${local.timestamp_sanitized}")
  source_instance_id =  var.instance_id

  tags = {
		 Environment = var.environment
         Project = var.project
	    Terraformed = "True"
	}
}

/*resource "aws_ami_copy" "example" {
  name              = "terraform-example"
  description       = "A copy of ami-xxxxxxxx"
  source_ami_id     =  aws_ami_from_instance.create_ami.id
  source_ami_region = "ap-south-1"

 tags = {
		 Environment = var.environment
         Project = var.project
	    Terraformed = "True"
	}
} */
