import win32com.client
import inspect


class XARealEvents(object):
    def __init__(self):
        self.parent = None

    def set_parent(self, parent):
        self.parent = parent

    def OnReceiveMessage(self, systemError, messageCode, message):
        if self.parent:
            self.parent.OnReceiveMessage(systemError, messageCode, message)

    def OnReceiveData(self, szTrCode):
        if self.parent:
            self.parent.OnReceiveData(szTrCode)

    def OnReceiveRealData(self, szTrCode):
        if self.parent:
            self.parent.OnReceiveRealData(szTrCode)

    def OnReceiveChartRealData(self, szTrCode):
        if self.parent:
            self.parent.OnReceiveChartRealData(szTrCode)

    def OnRecieveLinkData(self, szLinkName, szData, szFiller):
        if self.parent:
            self.parent.OnRecieveLinkData(szLinkName, szData, szFiller)


class XAReal(object):
    def __init__(self, parent=None):
        self.parent = parent
        self.ActiveX = win32com.client.DispatchWithEvents('XA_DataSet.XAReal', XARealEvents)
        self.ActiveX.set_parent(parent=self)

        self.module_name = self.__class__.__name__
        self.inblock = 'InBlock'
        self.outblock = 'OutBlock'
        self.res_file = 'C:\\eBEST\\xingAPI\\Res\\%s.res' % self.module_name

    def OnReceiveMessage(self, systemError, messageCode, message):
        class_name = self.__class__.__name__
        function_name = inspect.currentframe().f_code.co_name
        print('%s-%s ' % (class_name, function_name), systemError, messageCode, message)

    def AdviseLinkFromHTS(self):
        self.ActiveX.AdviseLinkFromHTS()

    def UnAdviseLinkFromHTS(self):
        self.ActiveX.UnAdviseLinkFromHTS()

    def OnRecieveLinkData(self, szLinkName, szData, szFiller):
        print(szLinkName, szData, szFiller)


# KOSPI체결
class S3_(XAReal):
    def __init__(self, parent=None):
        super(__class__, self).__init__(parent=parent)
        self.ActiveX.LoadFromResFile(self.res_file)
        self.onadvise = {}

    def AdviseRealData(self, code):
        if code not in list(self.onadvise.keys()):
            self.onadvise[code] = ''
            self.ActiveX.SetFieldData(self.inblock, 'shcode', code)
            self.ActiveX.AdviseRealData()

    def UnadviseRealDataWithKey(self, code):
        self.onadvise.pop(code, None)
        self.ActiveX.UnadviseRealDataWithKey(code)

    def UnadviseRealData(self):
        self.onadvise = {}
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):
        result = {'price': int(self.ActiveX.GetFieldData(self.outblock, 'price')),
                  'offer': int(self.ActiveX.GetFieldData(self.outblock, 'offerho')),
                  'bid': int(self.ActiveX.GetFieldData(self.outblock, 'bidho')),
                  'shcode': self.ActiveX.GetFieldData(self.outblock, 'shcode')}

        if self.parent:
            self.parent.OnReceiveRealData(szTrCode, result)


# KOSDAQ체결
class K3_(XAReal):
    def __init__(self, parent=None):
        super(__class__, self).__init__(parent=parent)
        self.ActiveX.LoadFromResFile(self.res_file)
        self.onadvise = {}

    def AdviseRealData(self, code):
        if code not in list(self.onadvise.keys()):
            self.onadvise[code] = ''
            self.ActiveX.SetFieldData(self.inblock, 'shcode', code)
            self.ActiveX.AdviseRealData()

    def UnadviseRealDataWithKey(self, code):
        self.onadvise.pop(code, None)
        self.ActiveX.UnadviseRealDataWithKey(code)

    def UnadviseRealData(self):
        self.onadvise = {}
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):
        result = {'price': int(self.ActiveX.GetFieldData(self.outblock, 'price')),
                  'offer': int(self.ActiveX.GetFieldData(self.outblock, 'offerho')),
                  'bid': int(self.ActiveX.GetFieldData(self.outblock, 'bidho')),
                  'shcode': self.ActiveX.GetFieldData(self.outblock, 'shcode')}

        if self.parent:
            self.parent.OnReceiveRealData(szTrCode, result)


# 주식선물체결
class JC0(XAReal):
    def __init__(self, parent=None):
        super(__class__, self).__init__(parent=parent)
        self.ActiveX.LoadFromResFile(self.res_file)
        self.onadvise = {}

    def AdviseRealData(self, code):
        if code not in list(self.onadvise.keys()):
            self.onadvise[code] = ''
            self.ActiveX.SetFieldData(self.inblock, 'futcode', code)
            self.ActiveX.AdviseRealData()

    def UnadviseRealDataWithKey(self, code):
        self.onadvise.pop(code, None)
        self.ActiveX.UnadviseRealDataWithKey(code)

    def UnadviseRealData(self):
        self.onadvise = {}
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):
        result = {'price': int(self.ActiveX.GetFieldData(self.outblock, 'price')),
                  'offer': int(self.ActiveX.GetFieldData(self.outblock, 'offerho1')),
                  'bid': int(self.ActiveX.GetFieldData(self.outblock, 'bidho1')),
                  'futcode': self.ActiveX.GetFieldData(self.outblock, 'futcode')}

        if self.parent:
            self.parent.OnReceiveRealData(szTrCode, result)


# 주식주문체결 (내거)
class SC1(XAReal):
    def __init__(self, parent=None):
        super(__class__, self).__init__(parent=parent)
        self.ActiveX.LoadFromResFile(self.res_file)
        self.onadvise = {}

    def AdviseRealData(self):
        self.ActiveX.AdviseRealData()

    def UnadviseRealData(self):
        self.onadvise = {}
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):
        result = {'shcode': self.ActiveX.GetFieldData(self.outblock, 'Isuno'),
                  'name': self.ActiveX.GetFieldData(self.outblock, 'Isunm'),
                  'timestamp': self.ActiveX.GetFieldData(self.outblock, 'exectime'),
                  'deal_price': int(self.ActiveX.GetFieldData(self.outblock, 'execprc')),
                  'deal_quantity': int(self.ActiveX.GetFieldData(self.outblock, 'execqty')),
                  'deal_code': int(self.ActiveX.GetFieldData(self.outblock, 'bnstp')),
                  'lineseq': self.ActiveX.GetFieldData(self.outblock, 'lineseq'),
                  'trcode': self.ActiveX.GetFieldData(self.outblock, 'trcode'),
                  'order_number': int(self.ActiveX.GetFieldData(self.outblock, 'ordno'))}

        if self.parent:
            self.parent.OnReceiveRealData(szTrCode, result)


# 선물주문체결 (내거)
class C01(XAReal):
    def __init__(self, parent=None):
        super(__class__, self).__init__(parent=parent)
        self.ActiveX.LoadFromResFile(self.res_file)
        self.onadvise = {}

    def AdviseRealData(self):
        self.ActiveX.AdviseRealData()

    def UnadviseRealData(self):
        self.onadvise = {}
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):
        result = {'shcode': self.ActiveX.GetFieldData(self.outblock, 'expcode'),
                  'timestamp': self.ActiveX.GetFieldData(self.outblock, 'chetime'),
                  'deal_price': int(float(self.ActiveX.GetFieldData(self.outblock, 'cheprice')) * 100),
                  'deal_quantity': int(self.ActiveX.GetFieldData(self.outblock, 'chevol')),
                  'deal_code': int(self.ActiveX.GetFieldData(self.outblock, 'dosugb')),
                  'order_number': int(self.ActiveX.GetFieldData(self.outblock, 'ordno'))}

        if self.parent:
            self.parent.OnReceiveRealData(szTrCode, result)


# KOSPI호가잔량
class H1_(XAReal):
    def __init__(self, parent=None):
        super(__class__, self).__init__(parent=parent)
        self.ActiveX.LoadFromResFile(self.res_file)
        self.onadvise = {}

    def AdviseRealData(self, code):
        if code not in list(self.onadvise.keys()):
            self.onadvise[code] = ''
            self.ActiveX.SetFieldData(self.inblock, 'shcode', code)
            self.ActiveX.AdviseRealData()

    def UnadviseRealDataWithKey(self, code):
        self.onadvise.pop(code, None)
        self.ActiveX.UnadviseRealDataWithKey(code)

    def UnadviseRealData(self):
        self.onadvise = {}
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):
        result = {'shcode': self.ActiveX.GetFieldData(self.outblock, 'shcode'),
                  'offer': int(self.ActiveX.GetFieldData(self.outblock, 'offerho1')),
                  'offer_quantity': int(self.ActiveX.GetFieldData(self.outblock, 'offerrem1')),
                  'bid': int(self.ActiveX.GetFieldData(self.outblock, 'bidho1')),
                  'bid_quantity': int(self.ActiveX.GetFieldData(self.outblock, 'bidrem1'))}

        if self.parent:
            self.parent.OnReceiveRealData(szTrCode, result)


# KOSDAQ호가잔량
class HA_(XAReal):
    def __init__(self, parent=None):
        super(__class__, self).__init__(parent=parent)
        self.ActiveX.LoadFromResFile(self.res_file)
        self.onadvise = {}

    def AdviseRealData(self, code):
        if code not in list(self.onadvise.keys()):
            self.onadvise[code] = ''
            self.ActiveX.SetFieldData(self.inblock, 'shcode', code)
            self.ActiveX.AdviseRealData()

    def UnadviseRealDataWithKey(self, code):
        self.onadvise.pop(code, None)
        self.ActiveX.UnadviseRealDataWithKey(code)

    def UnadviseRealData(self):
        self.onadvise = {}
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):
        result = {'shcode': self.ActiveX.GetFieldData(self.outblock, 'shcode'),
                  'offer': int(self.ActiveX.GetFieldData(self.outblock, 'offerho1')),
                  'offer_quantity': int(self.ActiveX.GetFieldData(self.outblock, 'offerrem1')),
                  'bid': int(self.ActiveX.GetFieldData(self.outblock, 'bidho1')),
                  'bid_quantity': int(self.ActiveX.GetFieldData(self.outblock, 'bidrem1'))}

        if self.parent:
            self.parent.OnReceiveRealData(szTrCode, result)


# 주식선물호가
class JH0(XAReal):
    def __init__(self, parent=None):
        super(__class__, self).__init__(parent=parent)
        self.ActiveX.LoadFromResFile(self.res_file)
        self.onadvise = {}

    def AdviseRealData(self, code):
        if code not in list(self.onadvise.keys()):
            self.onadvise[code] = ''
            self.ActiveX.SetFieldData(self.inblock, 'futcode', code)
            self.ActiveX.AdviseRealData()

    def UnadviseRealDataWithKey(self, code):
        self.onadvise.pop(code, None)
        self.ActiveX.UnadviseRealDataWithKey(code)

    def UnadviseRealData(self):
        self.onadvise = {}
        self.ActiveX.UnadviseRealData()

    def OnReceiveRealData(self, szTrCode):
        result = {'futcode': self.ActiveX.GetFieldData(self.outblock, 'futcode'),
                  'hotime': self.ActiveX.GetFieldData(self.outblock, 'hotime'),
                  'offer': int(self.ActiveX.GetFieldData(self.outblock, 'offerho1')),
                  'offer_quantity': int(self.ActiveX.GetFieldData(self.outblock, 'offerrem1')),
                  'bid': int(self.ActiveX.GetFieldData(self.outblock, 'bidho1')),
                  'bid_quantity': int(self.ActiveX.GetFieldData(self.outblock, 'bidrem1'))}

        if self.parent:
            self.parent.OnReceiveRealData(szTrCode, result)
