import boto3
import csv
#aws configure
iam = boto3.client('iam')
#Directly assigning access key
#iam = boto3.client('iam',aws_access_key_id="XXXX",aws_secret_access_key="YYY")
user_list = []
cnt=0
for key in iam.list_users()['Users']:
    result = {}
    Policies = []
    Groups=[]
    SNo=((cnt+1))
    result['SNo']=SNo
    result['UserName']=key['UserName']
    result['UserId']=key['UserId']
    List_of_Policies =  iam.list_user_policies(UserName=key['UserName'])

    result['Policies'] = List_of_Policies['PolicyNames']

    List_of_Groups =  iam.list_groups_for_user(UserName=key['UserName'])

    for Group in List_of_Groups['Groups']:
        Groups.append(Group['GroupName'])
    result['Groups'] = Groups

    List_of_MFA_Devices = iam.list_mfa_devices(UserName=key['UserName'])

    if not len(List_of_MFA_Devices['MFADevices']):
        result['isMFADeviceConfigured']=False   
    else:
        result['isMFADeviceConfigured']=True

    result['Arn']=key['Arn']
    result['CreateDate']=key['CreateDate']

    user_list.append(result)
    cnt = ((cnt+1))

#print(format(user_list))
for key in user_list:
    print(format(key))

csv_file = "IAM_UsersList.csv"
csv_columns = ['SNo','UserName','UserId', 'Policies','Groups','isMFADeviceConfigured','Arn','CreateDate']
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns, lineterminator='\n')
        writer.writeheader()
        for data in user_list:
            #Groups,Policies list changing to string and removing quotes
            if type(data['Groups']) is list:
                data['Groups'] = str(data['Groups'])[1:-1].replace("\'", ' ')
            if type(data['Policies']) is list:
                data['Policies'] = str(data['Policies'])[1:-1].replace("\'", ' ')
            writer.writerow(data)
except IOError:
    print("I/O error")
