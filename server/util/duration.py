class Duration(object):
    # Cache times
    MINUTE = 60
    HOUR = 60 * MINUTE
    DAY = 24 * HOUR
    WEEK = 7 * DAY
    MONTH = 30 * DAY
    YEAR = 365 * DAY

    SHORT = 15 * MINUTE
    LONG = HOUR
    FOREVER = DAY
