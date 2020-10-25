import boto3
import csv
import sys
import datetime
from dateutil.tz import tzutc

#aws configure
iam = boto3.client('iam')
#Directly assigning access key
#iam = boto3.client('iam',aws_access_key_id="XXXX",aws_secret_access_key="YYY")
resource = boto3.resource('iam')
user_list = []
cnt=0
#print(dir(iam))
#sys.exit(0)
def LastActivity(user_name):
    today = datetime.datetime.now()
    final_report = ''
    number = 1

    # Get Access Keys for the User
    keys_response = iam.list_access_keys(UserName=user_name)
    last_access = None

    # For every Access Key associate with the user
    for key in keys_response['AccessKeyMetadata']:
        last_used_response = iam.get_access_key_last_used(AccessKeyId=key['AccessKeyId'])
        if 'LastUsedDate' in last_used_response['AccessKeyLastUsed']:
            accesskey_last_used = last_used_response['AccessKeyLastUsed']['LastUsedDate']
            #print(accesskey_last_used)
            if last_access is None or accesskey_last_used < last_access:
                last_access = accesskey_last_used

        # More than x days since last access?
        if last_access is not None:
            delta = (today - last_access.replace(tzinfo=None)).days
            if delta >= 0:
                final_report = str(delta) + " days"
                number += 1
    #print(final_report)
    return final_report

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
    LoginDaysBack=LastActivity(key['UserName'])
    if not len(LoginDaysBack):
        LoginDaysBack = 'Never LoggedIn'

    result['LastActivityDays']=LoginDaysBack

    user_list.append(result)
    cnt = ((cnt+1))

#print(format(user_list))
for key in user_list:
    print(format(key))

csv_file = "IAM_ListExport.csv"
csv_columns = ['SNo','UserName','UserId', 'Policies','Groups','isMFADeviceConfigured','Arn','CreateDate','LastActivityDays']
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
