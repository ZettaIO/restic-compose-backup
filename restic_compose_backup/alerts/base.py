from restic_compose_backup.alerts import ALERT_INFO, ALERT_ERROR, ALERT_TYPES


class BaseAlert:
    name = None

    def __init__(self):
        pass

    def create_from_config(self, config):
        pass

    def send(self, self, subject=None, attachment=None, alert_type=ALERT_ERROR):
        pass
