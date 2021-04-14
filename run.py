import pythoncom

from api.XASessions import XASession
from strategy import example1, example2
from constants import MOD

if __name__ == '__main__':
    # login
    login_session = XASession()
    login_session.login()
    print('mod is', MOD)

    # strategies
    example1.run()
    example2.run()

    # listening
    while True:
        pythoncom.PumpWaitingMessages()
