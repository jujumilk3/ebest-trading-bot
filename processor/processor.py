import threading

from time import sleep
from models.singleton import SingletonInstance


class MainProcessor(SingletonInstance):
    def __init__(self):
        self.registered_tr_name_list = []
        self.registered_tr_object_list = []
        self.registered_tr_object_dict = {}

    def add_action(self, tr_object: object, *args):
        tr_name = tr_object.__class__.__name__
        if tr_name not in self.registered_tr_name_list:
            tr_processor = TRProcessor(tr_name, tr_object.aps)
            self.registered_tr_name_list.append(tr_name)
            self.registered_tr_object_dict[tr_name] = tr_processor
            tr_processor.register_action(tr_object, *args)
            tr_processor.start()
        else:
            tr_processor = self.registered_tr_object_dict[tr_name]
            tr_processor.register_action(tr_object, *args)


class TRProcessor(threading.Thread):
    def __init__(self, tr_name: str, action_per_second: float):
        super().__init__()
        self.tr_name = tr_name
        self.action_per_second = action_per_second * 0.9  # 초당 tr횟수를 꽉채우면 가끔씩 제한에 걸려서 안날아가길래 안정빵
        self.action_term = 1 / self.action_per_second
        self.transaction_queue = []

    def run(self):
        while True:
            if len(self.transaction_queue) > 0:
                print(self.tr_name + " is Working. And Its Enlisted Works: (" + str(len(self.transaction_queue)) + ")")
                transaction = self.transaction_queue.pop()
                transaction.activate()
                sleep(self.action_term)

    def register_action(self, tr_object, *args):
        transaction = Transaction(tr_object, *args)
        self.transaction_queue.append(transaction)


class Transaction:
    def __init__(self, tr_object, *args):
        self.tr_object = tr_object
        self.params = args

    def activate(self):
        self.tr_object.Query(*self.params)
