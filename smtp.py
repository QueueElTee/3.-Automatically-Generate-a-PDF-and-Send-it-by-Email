from smtplib import SMTP_SSL, SMTPAuthenticationError
from email_ import sender, message
import getpass

def connect_to_server():
    mail_server = SMTP_SSL('smtp.gmail.com', 465)
    mail_pass = getpass.getpass('Password? ')

    try:
        mail_server.login(sender, mail_pass)
        mail_server.send_message(message)
    except SMTPAuthenticationError:
        print("An error occurred while authenticating your details.")
        
    mail_server.quit()