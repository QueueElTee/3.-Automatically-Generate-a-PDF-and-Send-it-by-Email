from email.message import EmailMessage
import os.path, mimetypes
from pdf_generation import title, generate_summary

message = EmailMessage()

sender = 'sender@gmail.com'
recipient = 'recipient@gmail.com'


def send_email():
    message['From'] = sender
    message['To'] = recipient
    message['Subject'] = title

    summary = generate_summary('\n')
    body = summary

    message.set_content(body)

    attachment_path = 'tmp/cars.pdf'
    attachment_filename = os.path.basename(attachment_path)

    mime_type, _ = mimetypes.guess_type(attachment_path)
    mime_type, mime_subtype = mime_type.split('/', 1)

    with open(attachment_path, 'rb') as ap:
        message.add_attachment(ap.read(), 
                            maintype = mime_type, 
                            subtype = mime_subtype,
                            filename = attachment_filename)