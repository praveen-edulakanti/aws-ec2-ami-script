#cron setup
#30 01 * * * /bin/bash /location/scripts/ec2-create-image.sh i-054175bfffdcc2ca9 >> /location/logs/crontab.log 2>&1

DATE=$(date +%Y-%m-%d_%H-%M)
AMI_NAME="Backup - $DATE"
AMI_DESCRIPTION="Backup - $DATE"
INSTANCE_ID=$1

printf "Requesting AMI for instance $1...\n"
aws ec2 create-image --instance-id $1 --name "$AMI_NAME" --description "$AMI_DESCRIPTION" --no-reboot

if [ $? -eq 0 ]; then
	printf "AMI request complete!\n"
fi