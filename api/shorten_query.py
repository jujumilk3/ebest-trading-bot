from constants import *
from api.XAQuaries import CSPAT00600, CSPAT00800, CFOAT00100, CFOAT00300, t0424
from models.singleton import SingletonInstance


class ShortenQuery(SingletonInstance):
    def OnReceiveMessage(self, system_error, message_code, message):
        print(system_error, message_code, message)

    def OnReceiveData(self, tr_code, result):
        print(tr_code, result)


def deal(stock_type, code, quantity, price, deal_code, parent=None, current_price=False):
    parent_object = ShortenQuery().instance() if not parent else parent
    account = LOGIN_ID
    password = PASSWORD
    order_code = '00'
    if current_price:
        price = 0
        order_code = '03'
    if stock_type == 'spot':
        order_object = CSPAT00600(parent=parent_object)
        order_object.Query(account, password, code, quantity, price, deal_code, order_code)
    elif stock_type == 'future':
        order_object = CFOAT00100(parent=parent_object)
        order_object.Query(account, password, code, quantity, price, deal_code)


def deal_cancel(stock_type, order_number, code, quantity, parent=None):
    parent_object = ShortenQuery.instance() if not parent else parent
    account = LOGIN_ID
    password = PASSWORD
    if stock_type == 'spot':
        order_object = CSPAT00800(parent_object)
        order_object.Query(order_number, account, password, code, quantity)
    elif stock_type == 'future':
        order_object = CFOAT00300(parent_object)
        order_object.Query(order_number, account, password, code, quantity)


def get_account_info(stock_type, account_number, password):
    shorten_query_object = ShortenQuery().instance()
    if stock_type == 'spot':
        t0424object = t0424(parent=shorten_query_object)
        return t0424object.Query(account_number, password)

