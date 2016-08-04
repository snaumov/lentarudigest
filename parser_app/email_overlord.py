import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

from news_parser.settings import config

import news_parser.settings as settings

class EmailOverlord():
    """Class for e-mail related activities

    Grabs data for it's fields from config file

    usage: emailoverl = EmailOverlord()

    send_mail(send_to, file): function for sending email message with attachment to e-mail address:
        send_to: valid e-mail address, str type
        file: filepath, str type

        If no file is attached, the different e-mail will be sent.



    """

    class EmailOverlordException(Exception):
        pass

    def __init__(self):
        try:
            self.smtp_server_url = config['smtp_server_url']
            self.smtp_server_port = config['smtp_server_port']
            self.smtp_sent_from = config['smtp_sent_from']

        except KeyError:
            raise self.EmailOverlordException('No smtp server url & port & sent_from info found in config file')

        try:
            self.smtp_server_username = settings.SMTP_SERVER_USERNAME
            self.smtp_server_password = settings.SMTP_SERVER_PASSWORD
        except KeyError:
            self.smtp_server_username = None
            self.smtp_server_password = None

    def send_mail(self, send_to, file=None):

        send_from = self.smtp_sent_from
        print("[EMAIL]: file to send {0}".format(file))
        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = send_to
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = 'News Digest'

        if file:

            text = "Thank you for using our service! Please find your digest attached"

            try:
                with open(file, "rb") as fil:
                    part = MIMEApplication(
                        fil.read(),
                        Name=basename(file)
                    )
                    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(file)
                    msg.attach(part)
            except Exception as e:
                raise self.EmailOverlordException('[EMAIL]: Can not open the attachment', e.args) from e

        else:
            text = "Thank you for using our service! Unfortunately, no news found for requested period"

        msg.attach(MIMEText(text))

        try:
            smtp = smtplib.SMTP_SSL(self.smtp_server_url, self.smtp_server_port)
            smtp.login(self.smtp_server_username, self.smtp_server_password)
            smtp.sendmail(send_from, send_to, msg.as_string())
            print("[EMAIL]: e-mail to {0} sent".format(send_to))
            smtp.close()
        except Exception as e:
            raise self.EmailOverlordException('[EMAIL]: Can not send email', e.args) from e
