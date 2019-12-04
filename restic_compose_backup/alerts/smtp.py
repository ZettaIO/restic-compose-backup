from restic_compose_backup.alerts.base import BaseAlert


class SMTPAlert(BaseAlert):
    name = 'smtp'

    def __init__(self):
        pass

    def create_from_config(self, config):
        pass

    def send(self, self, subject=None, attachment=None, alert_type=ALERT_ERROR):
        pass
