import boto3
import datetime
#import updatekey # Uncomment to make the access key Inactive
#import sendReminderEmail #For Sending Reminder mail

def notifyUsersForAccessKeyStatus():
    #InActivates the access Key if older then 90 days and send the mail to notify the same
    #Sends a Waring mail for the users that access key is going to be expired from 15 days prior to expire 
    #Returns total Number of users expired and mail sent

    iam = boto3.client('iam')
    email_list = list()
    timeLimit=datetime.datetime.now() - datetime.timedelta( days = 75 ) 
    timeLimit =timeLimit.replace(tzinfo=None)
    count =0 

    for user in iam.list_users(MaxItems=1000)['Users']:
        res = iam.list_access_keys(UserName=user['UserName'])
        if res is not None: 
            accesskeydate = res['AccessKeyMetadata']
            #print("accesskeydate ",accesskeydate)
            if len(accesskeydate) != 0: #To get the accesskey creation date if only access key is created for the user
                user_date = accesskeydate[0]['CreateDate']
                #print(user_date)
                user_date = user_date.replace(tzinfo=None)
                if user_date <= timeLimit:
                    #print("User added in reminder list = ",user)
                    response = iam.get_user(UserName=user['UserName'])
                    user = response['User']
                    if'Tags' in user:
                        for tag in user['Tags']:
                            if tag['Key'] == 'EMAIL':
                                email_list.append(tag['Value'])
                                delta = user_date - timeLimit
                                #print(type(delta))
                                inde=str(delta).find('days')
                                days = int (str(delta)[0:inde])*-1
                                count+=1 # Count the users for expired and about to expire

                                if days > 90: #Users Expired
                                    print("Key Disabled Sent ",tag['Value'],"Number of Days :",days)
                                    #sendKeyDisabled(tag['Value'],user['UserName'],accesskeydate[0]['AccessKeyId'])]
                                    print('Email :',tag['Value'],"UserName : ",user['UserName'],accesskeydate[0]['AccessKeyId'])
                                else: #users about to exprire
                                    print("Email Reminder Sent ",tag['Value'],"Number of Days :",days)
                                    print('Email :',tag['Value'],"UserName : ",user['UserName'],accesskeydate[0]['AccessKeyId'])
                                    #sendReminderMail(tag['Value'],days)
                                                        
    return count  

print(notifyUsersForAccessKeyStatus())