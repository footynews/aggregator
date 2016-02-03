import os
import smtplib

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader, Template


class Email:

    def __init__(self, from_addr, to_addr, subject, body_template_text,
                 body_template_html, render_context,attachments=None,
                 from_name=None):
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.subject = subject
        if attachments is None:
            attachments = []
        elif isinstance(attachments, str):
            attachments = [attachments]
        self.attachments = attachments
        self.from_name = from_name
        self.body_template_text = body_template_text
        self.body_template_html = body_template_html
        self.env = Environment(loader=FileSystemLoader('templates'))
        self.render_context = render_context
        self.message = None

    def init_email(self):
        message = MIMEMultipart()
        message['From'] = self.from_name if self.from_name else self.from_addr
        message['To'] = self.to_addr
        message['Subject'] = self.subject
        return message

    def email_body(self):
        # Record the MIME types of both parts - text/plain and text/html.
        body = MIMEMultipart('alternative')
        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        body.attach(self.body_text())
        body.attach(self.body_html())
        return body

    def body_text(self):
        template = self.env.get_template(self.body_template_text)
        rendered_text = template.render(self.render_context)
        return MIMEText(rendered_text, 'plain')

    def body_html(self):
        template = self.env.get_template(self.body_template_html)
        rendered_html = template.render(self.render_context)
        return MIMEText(rendered_html, 'html')

    @staticmethod
    def file_name(file_path):
        _, tail = os.path.split(file_path)
        return tail

    def upload_attachment(self, attachment):
        name = Email.file_name(attachment)
        with open(attachment, 'rb') as fp:
            file_attachment = MIMEApplication(fp.read())
            file_attachment.add_header('Content-Disposition', 'attachment',
                                        filename=name)
        return file_attachment

    def compose_email(self):
        self.message = self.init_email()
        self.message.attach(self.email_body())
        for attachment in self.attachments:
            self.message.attach(self.upload_attachment(attachment))
        return self.message


def send_email(from_addr, password, to_addr, subject, body_template_text,
               body_template_html, render_context,attachments=None,
               from_name=None):
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(from_addr, password)
        email = Email(from_addr, to_addr, subject, body_template_text,
                      body_template_html, render_context, attachments)
        composed_email = email.compose_email()
        server.sendmail(from_addr, to_addr, composed_email.as_string())
