import boto3
from botocore.exceptions import ClientError

def sendAccessKeyDisabledEmail(email,username):
    #/** Send Email TO the Valid Email id (AS String) passed **/

    SENDER = "Sender Name <>"
    RECIPIENT = email
    AWS_REGION = ""

    # The subject line for the email.
    SUBJECT = "Warning-AWS password is expired and the access key has been disabled"

    BODY_TEXT = ("user guide for the IAM credentials rotation\r\n"
             "Below are the steps to be followed to rotate the user IAM access key "
             "AWS SDK for Python (Boto)."
             )
    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
    <p>Hi {0},</p>
    <p> Your access Key Has been Disabled</p>
    </body>
    </html>
                """.format(username)

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])


#Test Data
# #sendAccessKeyDisabledEmail('xxx.xxx@xxx.com',"Bade")