resource "aws_ebs_snapshot" "create_ebs_snapshot" {
  volume_id = var.vol_id
  tags = {
    Name = format("${var.environment}-${var.project}-%s", "Snapshot-${timestamp()}")
    Environment = var.environment
            Project = var.project
	    Terraformed = "True"
  }
}