import logging

logger = logging.getLogger(__name__)

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
    logger.debug(f"validating crontab schedule {schedule}")
    parts = schedule.split()
    if len(parts) != 5:
        logger.debug(f"crontab has only {len(parts)}/5 parts")
        return False

    minute, hour, day, month, weekday = parts
    try:
        logger.debug(f"[crontab] validating minute: {minute}")
        validate_field(minute, 0, 59)
        logger.debug(f"[crontab] validating hour: {hour}")
        validate_field(hour, 0, 23)
        logger.debug(f"[crontab] validating day: {day}")
        validate_field(day, 1, 31)
        logger.debug(f"[crontab] validating month: {month}")
        validate_field(month, 1, 12)
        logger.debug(f"[crontab] validating weekday: {weekday}")
        validate_field(weekday, 0, 6)
    except ValueError:
        return False

    return True


def validate_field(value, min, max):
    if value == '*':
        logger.debug("[crontab] validation success: *")
        return
    elif "," in value:
        items = value.split(",")
        logger.debug(f"[crontab] recursive validation of {items}")
        return all(validate_field(val, min, max) for val in items)
    elif "*/" in value:
        logger.debug(f"[crontab] validating */ pattern")
        i = int(value.split("/")[1])
        logger.debug(f"[crontab] got {i} from {value}")
        return min <= i <= max
    elif "-" in value:
        logger.debug("[crontab] validating range")
        split = value.split("-")
        if len(split) < 2:
            logger.debug(f"[crontab] validation error: {value} has has a one sided range")
            return False
        minVal = int(split[0])
        maxVal = int(split[1])
        return (min <= minVal <= maxVal) and (minVal <= maxVal <= max)

    logger.debug(f"[crontab] validating simple number {value}")
    i = int(value)
    return min <= i <= max


def strip_quotes(value: str):
    """Strip enclosing single or double quotes if present"""
    if value[0] in QUOTE_CHARS:
        value = value[1:]
    if value[-1] in QUOTE_CHARS:
        value = value[:-1]

    return value
