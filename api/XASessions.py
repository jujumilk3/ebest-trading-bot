import win32com.client
import pythoncom
import constants


class XASessionEvents(object):
    def __init__(self):
        self.parent = None

    def set_parent(self, parent):
        self.parent = parent

    def OnLogin(self, code, msg):
        if self.parent:
            self.parent.OnLogin(code, msg)

    def OnLogout(self):
        if self.parent:
            self.parent.OnLogout()

    def OnDisconnect(self):
        if self.parent:
            self.parent.OnDisconnect()


class XASession:
    def __init__(self, parent=None):
        self.login_state = 0
        self.ActiveX = win32com.client.DispatchWithEvents('XA_Session.XASession', XASessionEvents)

        if parent is None:
            self.ActiveX.set_parent(parent=self)
        else:
            self.ActiveX.set_parent(parent=parent)

    def login(self, svrtype=0):
        server_url = 'hts.ebestsec.co.kr' if constants.MOD == 'REAL' else 'demo.ebestsec.co.kr'
        user_id = constants.LOGIN_ID
        user_password = constants.PASSWORD
        result = self.ActiveX.ConnectServer(server_url, 200001)
        if not result:
            nErrCode = self.ActiveX.GetLastError()
            strErrMsg = self.ActiveX.GetErrorMessage(nErrCode)
            return False, nErrCode, strErrMsg
        connected = self.ActiveX.Login(user_id, user_password, '', svrtype, 0)
        if not connected:
            print("login failed")
            return False
        while self.login_state == 0:
            pythoncom.PumpWaitingMessages()
        else:
            return True, 0, 'OK'

    def OnLogin(self, code, msg):
        if code == '0000':
            print("login success")
            self.login_state = 1
        else:
            print("login failed. code: {0}, message: {1}".format(code, msg))
            self.login_state = 2

    def logout(self):
        self.ActiveX.Logout()

    def disconnect(self):
        self.ActiveX.DisconnectServer()

    def IsConnected(self):
        return self.ActiveX.IsConnected()

    def get_account_info(self):
        for i in range(self.ActiveX.GetAccountListCount()):
            print(self.ActiveX.GetAccountList(i))
