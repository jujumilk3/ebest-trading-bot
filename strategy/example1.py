import os

from models.singleton import SingletonInstance
from api.XAQuaries import *
from api.XAReals import *


class Example1Strategy(SingletonInstance):
    def OnReceiveMessage(self, system_error, message_code, message):
        print(system_error, message_code, message)

    def OnReceiveData(self, tr_code, result):
        if tr_code == 't1101':  # 주식 현물
            print(tr_code, result)

    def OnReceiveRealData(self, tr_code, result):
        if tr_code == 'S3_':  # KOSPI 현물 체결 (실시간 시세)
            print(tr_code, result)


def run():
    short_code = '005930'  # 삼성전자 현물 코드
    print(os.path.basename(__file__) + ' is running...')
    example_strategy_object = Example1Strategy()
    t1101object = t1101(parent=example_strategy_object)
    t1101object.Query(short_code)
    s3_object = S3_(parent=short_code)
    s3_object.AdviseRealData(short_code)
