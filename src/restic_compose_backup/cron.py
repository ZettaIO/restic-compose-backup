"""
# ┌───────────── minute (0 - 59)
# │ ┌───────────── hour (0 - 23)
# │ │ ┌───────────── day of the month (1 - 31)
# │ │ │ ┌───────────── month (1 - 12)
# │ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday;
# │ │ │ │ │                                   7 is also Sunday on some systems)
# │ │ │ │ │
# │ │ │ │ │
# * * * * * command to execute
"""
QUOTE_CHARS = ['"', "'"]


def generate_crontab(config):
    """Generate a crontab entry for running backup job"""
    command = config.cron_command.strip()
    schedule = config.cron_schedule

    if schedule:
        schedule = schedule.strip()
        schedule = strip_quotes(schedule)
        if not validate_schedule(schedule):
            schedule = config.default_crontab_schedule
    else:
        schedule = config.default_crontab_schedule

    return f'{schedule} {command}\n'


def validate_schedule(schedule: str):
    """Validate crontab format"""
    parts = schedule.split()
    if len(parts) != 5:
        return False

    for p in parts:
        if p != '*' and not p.isdigit():
            return False

    minute, hour, day, month, weekday = parts
    try:
        validate_field(minute, 0, 59)
        validate_field(hour, 0, 23)
        validate_field(day, 1, 31)
        validate_field(month, 1, 12)
        validate_field(weekday, 0, 6)
    except ValueError:
        return False

    return True


def validate_field(value, min, max):
    if value == '*':
        return

    i = int(value)
    return min <= i <= max


def strip_quotes(value: str):
    """Strip enclosing single or double quotes if present"""
    if value[0] in QUOTE_CHARS:
        value = value[1:]
    if value[-1] in QUOTE_CHARS:
        value = value[:-1]

    return value
