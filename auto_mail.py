import email.utils
import os
import smtplib
import ssl
from email.message import EmailMessage
import dotenv

dotenv.load_dotenv()

sender = "user@mail.com"
password = os.environ.get("GAPP_PASSWORD")
receivers = ["user@mail.com"]

subject = "Daily Report"
body = ""

message = EmailMessage()
message["From"] = email.utils.formataddr(("Dr. Dark Flames", sender))
message["To"] = receivers
message["Subject"] = subject
message.set_content(body)
message.add_alternative("""
<!DOCTYPE html>
<html>
    <body>
        <h1>
            This is a Test~
        </h1>
    </body>
</html>
""", subtype="html")

with open("../res/Giga-chad.png", "rb") as file:
    file_data = file.read()
    file_type = file.name[file.name.rindex('.'):]
    file_name = file.name.split('/')[-1]
    file.close()

message.add_attachment(file_data, maintype="image", subtype=file_type, filename=file_name)

context = ssl.create_default_context()
port = 465


def send_mail():
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as smtp:
        try:
            smtp.login(sender, password)
            smtp.sendmail(sender, receivers, message.as_string())
            smtp.close()
            print("Email Sent Successfully!")
        except smtplib.SMTPException as e:
            print("Couldn't Send the Email!", e)


if __name__ == '__main__':
    send_mail()
