import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
class SendEmail:
    email = ''
    port = 0
    password = ''
    server_smtp = ''
    server = None
    message = None

    def __init__(self,email,password,server_smtp):
        self.email = email
        self.password = password
        self.server_email = server_smtp
        #self.port = port
        self.message = MIMEMultipart('alternative')

        try:
            self.server = smtplib.SMTP('smtp.gmail.com')

        except Exception as e:
            print(e)

    def send_email( self, to_email,message,subject):
        self.message['Subject'] = subject
        self.message['From'] = self.email
        self.message['To'] = to_email
        self.message.attach(MIMEText(message,'plain'))
        self.server.connect(host='smtp.gmail.com', port=587)
        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()
        self.server.login(self.email, self.password)
        self.server.sendmail(self.email,to_email,self.message.as_string())
        self.server.close()

def main():
    se = SendEmail('toms.extractor.log@gmail.com', 'Kaltire.2019', 'smtp.gmail.com:587')
    se.send_email('se.the.nowis@gmail.com', 'holaa', 'mensaje de prueba')


if __name__ == '__main__':
    schedule.every(3).minute.do(main)





