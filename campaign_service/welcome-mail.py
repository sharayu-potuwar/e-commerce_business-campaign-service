import json

import boto3

class SendEmail():

    def __init__(self):
        self.ses_client = boto3.client("ses", region_name="us-east-1")

    def verify_email(self, registrationObj):
    
        self.ses_client.verify_email_identity(EmailAddress=registrationObj['email_id'])
        print("Started verification of %s.", registrationObj['email_id'])

    def send_html_email(self, registrationObj):
       
        CHARSET = "UTF-8"
        HTML_EMAIL_CONTENT = f"""
            <html>
            <head></head>
            <h1 style='text-align:center'>Thanks, For signing with us</h1>
            <p>Hello, {registrationObj['first_name']}</p>
            <p>This is to inform you, that you have been successfully registered with us</P>
            <p> for any further queries you may connect with Apoorva wathodkar </p>
            </body>
            </html>
            """

        response = self.ses_client.send_email(
            Destination={
                "ToAddresses": [
                registrationObj['email_id']
                ],
            },
            Message={
                "Body": {
                    "Html": {
                        "Charset": CHARSET,
                        "Data": HTML_EMAIL_CONTENT,
                    }
                },
                "Subject": {
                    "Charset": CHARSET,
                    "Data": "Conratulations ! E-commerce welcome's you ..hehe",
                },
            },
            Source="sharayu.potuwar@gmail.com"
    )
        print(response)

def lambda_handler(event, context):
    sendemail = SendEmail()
    for record in event['Records']:
       try:
            message = record['Sns']['Message']
            registrationObj = json.loads(message) 
            print(registrationObj)
            # sendemail.verify_email(registrationObj)
            sendemail.send_html_email(registrationObj)

        
       except Exception as e:
            print("An error occurred")
            raise e
      
       
    



