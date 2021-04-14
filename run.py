import pythoncom

from api.XASessions import XASession
from strategy import example1, example2

if __name__ == '__main__':
    # login
    login_session = XASession()
    login_session.login()

    # strategies
    example1.run()
    example2.run()

    # listening
    while True:
        pythoncom.PumpWaitingMessages()
