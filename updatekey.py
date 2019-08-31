import boto3
from emailKeyDisabled import sendAccessKeyDisabledEmail

def sendKeyDisabled(email,userName,accessKeyId,status='Inactive'):
    #/* Update Access Key status to Inactive */
    client_u = boto3.client('iam') 
    response = client_u.update_access_key(UserName=userName,AccessKeyId=accessKeyId,Status=status)
    print('updated access Key ',response)
    sendAccessKeyDisabledEmail(email,userName)
    print('Email Sent :',email,userName)


# Test Data

#userName1=''
#akey=''

# Test Function
#sendKeyDisabled('email',userName1,akey)
