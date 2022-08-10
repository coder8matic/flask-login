# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
import json

from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()


def sendEmail(to, subject, emailContent):
    message = Mail(
        from_email=os.environ.get('SENDGRID_DEFAULT_SENDER'),
        to_emails=to,
        subject=subject,
        html_content=emailContent
        )

    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)

        return response.status_code

    except Exception as e:
        for error in json.loads((e.body).decode('ascii'))['errors']:
            error_message = error['message']
        
        return error_message