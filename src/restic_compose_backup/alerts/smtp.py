import os
import smtplib
import logging
from email.mime.text import MIMEText

from restic_compose_backup.alerts.base import BaseAlert

logger = logging.getLogger(__name__)


class SMTPAlert(BaseAlert):
    name = 'smtp'

    def __init__(self, host, port, user, password, to):
        self.host = host
        self.port = port
        self.user = user
        self.password = password or ""
        self.to = to

    @classmethod
    def create_from_env(cls):
        instance = cls(
            os.environ.get('EMAIL_HOST'),
            os.environ.get('EMAIL_PORT'),
            os.environ.get('EMAIL_HOST_USER'),
            os.environ.get('EMAIL_HOST_PASSWORD'),
            (os.environ.get('EMAIL_SEND_TO') or "").split(','),
        )
        if instance.properly_configured:
            return instance

        return None

    @property
    def properly_configured(self) -> bool:
        return self.host and self.port and self.user and len(self.to) > 0

    def send(self, subject: str = None, body: str = None, alert_type: str = 'INFO'):
        # send_mail("Hello world!")
        msg = MIMEText(body)
        msg['Subject'] = f"[{alert_type}] {subject}"
        msg['From'] = self.user
        msg['To'] = ', '.join(self.to)

        try:
            logger.info("Connecting to %s port %s", self.host, self.port)
            server = smtplib.SMTP_SSL(self.host, self.port)
            server.ehlo()
            server.login(self.user, self.password)
            server.sendmail(self.user, self.to, msg.as_string())
            logger.info('Email sent')
        except Exception as ex:
            logger.exception(ex)
        finally:
            server.close()
