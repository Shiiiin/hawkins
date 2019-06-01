import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from config import my_gmail_password

def send_log_files_to_admin():
    gmail_user = 'dp.horimz@gmail.com'
    gmail_password = my_gmail_password

    sent_from = gmail_user
    send_to = 'dp.horimz@gmail.com'

    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = send_to
    msg['Subject'] = 'ina219 sensor value log data'

    body = 'Log files are compressed in the attachement\n\n'
    msg.attach(MIMEText(body, 'plain'))

    file_to_send = 'data/log.zip'
    attachment = open(file_to_send, 'rb')

    part = MIMEBase('application', 'zip')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Dispostion', 'attachment; filename= ' + file_to_send)

    msg.attach(part)

    email_text = msg.as_string()

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, send_to, email_text)
        server.close()

        print('Email sent!')
    except:
        print('Something went wrong when trying to send an email...')
