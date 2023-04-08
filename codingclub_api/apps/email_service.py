import os
from postmark import PMMail
from django.conf import settings
from dotenv import load_dotenv

load_dotenv("config/.env")

POSTMARK_API_KEY = os.getenv("POSTMARK_API_KEY")


def send_email(to, subject, body):
    print(POSTMARK_API_KEY)

    mail = PMMail(api_key=POSTMARK_API_KEY,
                  subject=subject,
                  sender="munir4303324@cloud.neduet.edu.pk",
                  to=to,
                  text_body=body)
    mail.send()



# from __future__ import print_function
# import time
# import os
# import sib_api_v3_sdk
# from sib_api_v3_sdk.rest import ApiException
# from pprint import pprint
# from dotenv import load_dotenv
#
# load_dotenv("config/.env")
#
# API_KEY = os.getenv("SIB_API_KEY")
# configuration = sib_api_v3_sdk.Configuration()
# configuration.api_key['api-key'] = API_KEY
#
# api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
# # subject = "My Subject"
# # html_content = "<html><body>This is my first transactional email</body></html>"
# sender = {"name": "D-Sync", "email": "mustafamunir10@gmail.com"}
# # to = [{"email": "munir4303324@cloud.neduet.edu.pk", "name": "Jane Doe"}]
# cc = [{"email": "example2@example2.com", "name": "Janice Doe"}]
# bcc = [{"name": "John Doe", "email": "example@example.com"}]
# reply_to = {"email": "replyto@domain.com", "name": "John Doe"}
# headers = {"Some-Custom-Name": "unique-id-1234"}
# params = {"parameter": "My param value", "subject": "New Subject"}
# # send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers, html_content=html_content,
# #                                                sender=sender, subject=subject)
#
#
# class EmailService:
#     @staticmethod
#     def send_email(subject, to, to_name, message):
#         try:
#             to = [{"email": to, "name": to_name}]
#             html_content = f"<html><body>{message}</body></html>"
#             send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers, html_content=html_content,
#                                                            sender=sender, subject=subject)
#             print(API_KEY)
#             api_response = api_instance.send_transac_email(send_smtp_email)
#             pprint(api_response)
#         except ApiException as e:
#             print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
