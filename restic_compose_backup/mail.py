"""
"""
import smtplib
from email.mime.text import MIMEText

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 465
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_SEND_TO = ['']


def main():
    send_mail("Hello world!")


def send_mail(text):
    msg = MIMEText(text)
    msg['Subject'] = "Message from restic-compose-backup"
    msg['From'] = EMAIL_HOST_USER
    msg['To'] = ', '.join(EMAIL_SEND_TO)

    try:
        print("Connecting to {} port {}".format(EMAIL_HOST, EMAIL_PORT))
        server = smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT)
        server.ehlo()
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        server.sendmail(EMAIL_HOST_USER, EMAIL_SEND_TO, msg.as_string())
        print('Email Sent')
    except Exception as e:
        print(e)
    finally:
        server.close()


if __name__ == '__main__':
    main()
