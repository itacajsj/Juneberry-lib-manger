#coding:utf-8
import smtplib,poplib,email
from email.mime.text import MIMEText


def send_email(subject, contents, touser):
    sender = 'xxxx@sina.com'
    receiver = touser
    username = 'xxxx@sina.com'
    password = 'your passwd'
    msg = MIMEText(contents,_subtype='html',_charset='utf-8')
    msg['Subject'] = subject
    msg['From']=sender
    msg['To']=touser
    smtp = smtplib.SMTP()
    smtp.connect('smtp.sina.com')
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
