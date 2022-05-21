from .base_notifier import BaseNotifier
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
import textwrap


class EmailNotifier(BaseNotifier):
    def __init__(self):
        self.FROM = os.getenv('EMAIL_FROM', None)
        self.TO = os.getenv('EMAIL_TO', None)
        self.SMTP = os.getenv('EMAIL_SMPT', None)
        self.PORT = int(os.getenv('EMAIL_PORT', 587))
        self.USER = os.getenv('EMAIL_USER', None)
        self.PASSWORD = os.getenv('EMAIL_PASSWORD', None)
        self.server = None

        if None not in (self.FROM, self.TO, self.SMTP,
                        self.USER, self.PASSWORD):

            # SMTP Session
            self.session = smtplib.SMTP(host=self.SMTP, port=self.PORT)

            self.session.sendmail(from_addr=self.FROM,
                                  to_addrs=self.TO, msg=message.as_string())
            self.session.quit()

            self.server = smtplib.SMTP(host=self.SMTP, port=self.PORT)
            self.server.starttls()
            self.server.ehlo()
            self.server.login(user=self.USER, password=self.PASSWORD)

    def check_setup(self) -> bool:
        return bool(self.server is not None)

    def connect(self):
        self.session.connect(host=self.SMTP, port=self.PORT)
        self.session.starttls()
        self.session.ehlo()
        self.session.login(user=self.USER, password=self.PASSWORD)

    def close_connection(self):
        self.session.quit()

    def notify(self, notifications: list):
        if self.check_setup() and notifications:
            
            # Compose body message
            body_message = "Hello! New price drops found: \n\n"
            for notification in notifications:
                product_message = textwrap.dedent(
                    f"""Product [{notification["product_name"]}]
                    - Price: {notification["price"]},
                    - Mean of period: {notification["mean_of_period"]}
                    - Minimum recorded: {notification["historic_min"]}
                    - Retailers with this price: {notification["historic_min"]}
                    \n
                    """)
                body_message += product_message

            # Setup the MIME
            message = MIMEMultipart()
            message['From'] = self.FROM
            message['To'] = self.TO
            first_products = [x["product_name"] for x in notifications[0:2]]
            first_products = ", ".join(first_products)[:30]
            message['Subject'] = f"Price drops for {first_products}..."
            message.attach(MIMEText(body_message, 'plain'))

            self.session.sendmail(
                from_addr=self.FROM, to_addrs=self.TO,
                msg=message.as_string())

            self.close_connection()
