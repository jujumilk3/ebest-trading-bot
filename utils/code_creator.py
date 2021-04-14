from constants import *
from utils.timeutils import get_next_option_expiration_date


def get_next_month_stock_future_tail_code():
    next_option_expiration_date = get_next_option_expiration_date()
    expiration_year = next_option_expiration_date.year
    expiration_month = next_option_expiration_date.month
    return str(OPTION_EXPIRATION_YEAR_CODE[expiration_year]) + format(expiration_month, 'X') + '000'
