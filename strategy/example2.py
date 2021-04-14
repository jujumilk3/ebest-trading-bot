import os

from models.singleton import SingletonInstance


class Example2Strategy(SingletonInstance):
    def OnReceiveMessage(self, system_error, message_code, message):
        print(system_error, message_code, message)

    def OnReceiveData(self, tr_code, result):
        print(tr_code, result)

    def OnReceiveRealData(self, tr_code, result):
        print(tr_code, result)


def run():
    print(os.path.basename(__file__) + ' is running...')
    example_strategy_object = Example2Strategy()
