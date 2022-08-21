import os
import smtplib
from email.message import EmailMessage
import datetime
import time

class email:

  EMAIL_USER = os.environ.get('pythonEmailUser')
  EMAIL_PSWD = os.environ.get('pythonEmailPSWD')

  def __init__(self, reciever) -> None:
    self.mail = EmailMessage()
    self.subject = "Daily News Letter - "
    self.reciever = reciever
    self.content = ''


  # reads a given txt file and returns a string containing the contents
  def getMessage(self, fileName:str):
    with open(fileName, 'r', encoding="utf-8") as file:
      content = file.read()
    return content

  # returns the date format: (Aug 16, 2022)
  def getDate(self):
    today = datetime.date.today()
    day = today.strftime("%b %d, %Y")
    return day


  # returns the current date format: (04:45:23) - hour, minute, second
  def getTime(self):
    time = datetime.datetime.now()
    curr_time = time.strftime("%H:%M:%S")
    return curr_time


  # configures the email subject, sender, receiver, and content
  def setEmail(self, content:str):
    self.mail['Subject'] =  self.subject + " " + self.getDate()
    self.mail['From'] = self.EMAIL_USER
    self.mail['To'] = self.reciever
    self.mail.set_content(content)


  # sends the configured email
  # tries a total of 5 times to send email if the emails fail to send
  def sendEmail(self):
    for x in range(0, 5):
      try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(self.EMAIL_USER, self.EMAIL_PSWD) #login into mail server

            smtp.send_message(self.mail)
            print("Email successfully sent " + self.getDate() + " " + self.getTime())
      except smtplib.SMTPException:
        print("Email failed to send" + self.getDate() + " " + self.getTime())
        time.sleep(5)
      else:
        break

