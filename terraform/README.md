Change region, instance_id, volsize, vol_id values etc in ami.tfvars file

terraform init
terraform plan -var-file="ami.tfvars"
terraform apply -var-file="ami.tfvars"
terraform destroy -var-file="ami.tfvars"