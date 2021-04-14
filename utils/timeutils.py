import datetime


def get_current_timestamp():
    return datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')


def get_current_timestamp_as_win_file_ver():
    return datetime.datetime.today().strftime('%Y-%m-%d_%H-%M-%S')


def get_current_date():
    return datetime.datetime.today().strftime('%Y-%m-%d')


def get_next_option_expiration_date():
    today = datetime.date.today()
    next_thursday = today + datetime.timedelta(((3 - today.weekday()) % 7))
    while True:
        if 8 <= next_thursday.day <= 14:
            next_option_expiration_date = next_thursday
            break
        else:
            next_date = next_thursday + datetime.timedelta(days=1)
            next_thursday = next_date + datetime.timedelta(((3 - next_date.weekday()) % 7))
    return next_option_expiration_date
