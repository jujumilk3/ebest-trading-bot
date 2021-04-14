import win32com.client


class XAQueryEvents(object):
    def __init__(self):
        self.parent = None

    def set_parent(self, parent):
        self.parent = parent

    def OnReceiveMessage(self, system_error, message_code, message):
        if self.parent:
            self.parent.OnReceiveMessage(system_error, message_code, message)

    def OnReceiveData(self, tr_code):
        if self.parent:
            self.parent.OnReceiveData(tr_code)

    def OnReceiveChartRealData(self, tr_code):
        if self.parent:
            self.parent.OnReceiveChartRealData(tr_code)

    def OnReceiveSearchRealData(self, tr_code):
        if self.parent:
            self.parent.OnReceiveSearchRealData(tr_code)


class XAQuery(object):
    def __init__(self, parent=None):
        self.parent = parent

        self.ActiveX = win32com.client.DispatchWithEvents('XA_DataSet.XAQuery', XAQueryEvents)
        self.ActiveX.set_parent(parent=self)

        self.module_name = self.__class__.__name__
        self.inblock = '%sInBlock' % self.module_name
        self.inblock1 = '%sInBlock1' % self.module_name
        self.outblock = '%sOutBlock' % self.module_name
        self.outblock1 = '%sOutBlock1' % self.module_name
        self.outblock2 = '%sOutBlock2' % self.module_name
        self.outblock3 = '%sOutBlock3' % self.module_name
        self.res_file = 'C:\\eBEST\\xingAPI\\Res\\%s.res' % self.module_name

    def OnReceiveMessage(self, system_error, message_code, message):
        if self.parent:
            self.parent.OnReceiveMessage(system_error, message_code, message)

    def OnReceiveData(self, tr_code):
        pass

    def OnReceiveChartRealData(self, tr_code):
        pass

    def RequestLinkToHTS(self, szLinkName, szData, szFiller):
        return self.ActiveX.RequestLinkToHTS(szLinkName, szData, szFiller)


# 현물 정상주문 (매도1, 매수2)
class CSPAT00600(XAQuery):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.aps = 30

    def Query(self, account_number, password, shcode, order_quantity, order_price, deal_code, order_code='00'):

        if order_code == '03':
            order_price = ''

        self.ActiveX.LoadFromResFile(self.res_file)
        self.ActiveX.SetFieldData(self.inblock1, 'AcntNo', 0, account_number)
        self.ActiveX.SetFieldData(self.inblock1, 'InptPwd', 0, password)
        self.ActiveX.SetFieldData(self.inblock1, 'IsuNo', 0, shcode)
        self.ActiveX.SetFieldData(self.inblock1, 'OrdQty', 0, order_quantity)
        self.ActiveX.SetFieldData(self.inblock1, 'OrdPrc', 0, order_price)
        self.ActiveX.SetFieldData(self.inblock1, 'BnsTpCode', 0, deal_code)
        self.ActiveX.SetFieldData(self.inblock1, 'OrdprcPtnCode', 0, order_code)
        self.ActiveX.SetFieldData(self.inblock1, 'MgntrnCode', 0, '000')
        self.ActiveX.SetFieldData(self.inblock1, 'LoanDt', 0, '')
        self.ActiveX.SetFieldData(self.inblock1, 'OrdCndiTpCode', 0, '0')
        self.ActiveX.Request(0)

    def OnReceiveData(self, tr_code):
        result = {'shcode': self.ActiveX.GetFieldData(self.outblock1, 'IsuNo', 0).strip(),
                  'order_quantity': int(self.ActiveX.GetFieldData(self.outblock1, 'OrdQty', 0).strip()),
                  'order_price':  int(float(self.ActiveX.GetFieldData(self.outblock1, 'OrdPrc', 0).strip())),
                  'deal_code':  self.ActiveX.GetFieldData(self.outblock1, 'BnsTpCode', 0).strip(),

                  'timestamp': self.ActiveX.GetFieldData(self.outblock2, 'OrdTime', 0).strip(),
                  'shorten_code': self.ActiveX.GetFieldData(self.outblock2, 'ShtnIsuNo', 0).strip(),
                  'order_amount': int(self.ActiveX.GetFieldData(self.outblock2, 'OrdAmt', 0).strip()),
                  'order_number': int(self.ActiveX.GetFieldData(self.outblock2, 'OrdNo', 0).strip()),
                  'name': self.ActiveX.GetFieldData(self.outblock2, 'IsuNm', 0).strip()}

        if self.parent:
            self.parent.OnReceiveData(tr_code, result)


# 현물 취소주문
class CSPAT00800(XAQuery):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.aps = 30

    def Query(self, order_number, account_number, password, shcode, order_quantity):

        self.ActiveX.LoadFromResFile(self.res_file)
        self.ActiveX.SetFieldData(self.inblock1, 'OrgOrdNo', 0, order_number)
        self.ActiveX.SetFieldData(self.inblock1, 'AcntNo', 0, account_number)
        self.ActiveX.SetFieldData(self.inblock1, 'InptPwd', 0, password)
        self.ActiveX.SetFieldData(self.inblock1, 'IsuNo', 0, shcode)
        self.ActiveX.SetFieldData(self.inblock1, 'OrdQty', 0, order_quantity)

        self.ActiveX.Request(0)

    def OnReceiveData(self, tr_code):
        result = {'timestamp': self.ActiveX.GetFieldData(self.outblock2, 'OrdTime', 0).strip(),
                  'shorten_code': self.ActiveX.GetFieldData(self.outblock2, 'ShtnIsuNo', 0).strip(),
                  'order_number': int(self.ActiveX.GetFieldData(self.outblock2, 'OrdNo', 0).strip()),
                  'parent_order_number': self.ActiveX.GetFieldData(self.outblock2, 'PrntOrdNo', 0).strip(),
                  'name': self.ActiveX.GetFieldData(self.outblock2, 'IsuNm', 0).strip()}

        if self.parent:
            self.parent.OnReceiveData(tr_code, result)


# 선물옵션 정상주문
class CFOAT00100(XAQuery):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.aps = 30

    def Query(self, account_number, password, futcode, order_quantity, order_price, deal_code):
        self.ActiveX.LoadFromResFile(self.res_file)
        self.ActiveX.SetFieldData(self.inblock1, 'AcntNo', 0, account_number)
        self.ActiveX.SetFieldData(self.inblock1, 'Pwd', 0, password)
        self.ActiveX.SetFieldData(self.inblock1, 'FnoIsuNo', 0, futcode)
        self.ActiveX.SetFieldData(self.inblock1, 'OrdQty', 0, order_quantity)
        self.ActiveX.SetFieldData(self.inblock1, 'OrdPrc', 0, order_price)
        self.ActiveX.SetFieldData(self.inblock1, 'BnsTpCode', 0, deal_code)
        self.ActiveX.SetFieldData(self.inblock1, 'FnoOrdprcPtnCode', 0, '00')

        self.ActiveX.Request(0)

    def OnReceiveData(self, tr_code):
        result = {'futcode': self.ActiveX.GetFieldData(self.outblock1, 'FnoIsuNo', 0).strip(),
                  'deal_code':  self.ActiveX.GetFieldData(self.outblock1, 'BnsTpCode', 0).strip(),
                  'order_price': float(self.ActiveX.GetFieldData(self.outblock1, 'OrdPrc', 0).strip()),
                  'order_quantity': int(self.ActiveX.GetFieldData(self.outblock1, 'OrdQty', 0).strip()),
                  'order_number': int(self.ActiveX.GetFieldData(self.outblock2, 'OrdNo', 0).strip()),
                  }

        if self.parent:
            self.parent.OnReceiveData(tr_code, result)


# 선물옵션 취소주문
class CFOAT00300(XAQuery):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.aps = 30

    def Query(self, order_number, account_number, password, futcode, order_quantity):

        self.ActiveX.LoadFromResFile(self.res_file)
        self.ActiveX.SetFieldData(self.inblock1, 'OrgOrdNo', 0, order_number)
        self.ActiveX.SetFieldData(self.inblock1, 'AcntNo', 0, account_number)
        self.ActiveX.SetFieldData(self.inblock1, 'Pwd', 0, password)
        self.ActiveX.SetFieldData(self.inblock1, 'FnoIsuNo', 0, futcode)
        self.ActiveX.SetFieldData(self.inblock1, 'CancQty', 0, order_quantity)

        self.ActiveX.Request(0)

    def OnReceiveData(self, tr_code):
        result = {'futcode': self.ActiveX.GetFieldData(self.outblock1, 'FnoIsuNo', 0).strip(),
                  'order_quantity': int(self.ActiveX.GetFieldData(self.outblock1, 'CancQty', 0).strip()),
                  'order_number': int(self.ActiveX.GetFieldData(self.outblock1, 'OrgOrdNo', 0).strip())}

        if self.parent:
            self.parent.OnReceiveData(tr_code, result)


# 주식 현재가 호가 조회
class t1101(XAQuery):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.aps = 5

    def Query(self, code):
        self.ActiveX.LoadFromResFile(self.res_file)
        self.ActiveX.SetFieldData(self.inblock, 'shcode', 0, code)
        self.ActiveX.Request(0)

    def OnReceiveData(self, tr_code):
        result = {'name': str(self.ActiveX.GetFieldData(self.outblock, 'hname', 0)),
                  'shcode': str(self.ActiveX.GetFieldData(self.outblock, 'shcode', 0)),
                  'price': int(self.ActiveX.GetFieldData(self.outblock, 'price', 0)),
                  'offer': int(self.ActiveX.GetFieldData(self.outblock, 'offerho1', 0)),
                  'offer_quantity': int(self.ActiveX.GetFieldData(self.outblock, 'offerrem1', 0)),
                  'bid': int(self.ActiveX.GetFieldData(self.outblock, 'bidho1', 0)),
                  'bid_quantity': int(self.ActiveX.GetFieldData(self.outblock, 'bidrem1', 0))}

        if self.parent:
            self.parent.OnReceiveData(tr_code, result)


# 주식선물 현재가조회
class t8402(XAQuery):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.aps = 5

    def Query(self, code):
        self.ActiveX.LoadFromResFile(self.res_file)
        self.ActiveX.SetFieldData(self.inblock, 'focode', 0, code)
        self.ActiveX.Request(0)

    def OnReceiveData(self, tr_code):
        result = {'name': str(self.ActiveX.GetFieldData(self.outblock, 'hname', 0)),
                  'shcode': str(self.ActiveX.GetFieldData(self.outblock, 'shcode', 0)),
                  'price': int(self.ActiveX.GetFieldData(self.outblock, 'price', 0)),
                  'base_price': int(self.ActiveX.GetFieldData(self.outblock, 'baseprice', 0)),
                  'multiplier': float(self.ActiveX.GetFieldData(self.outblock, 'mulcnt', 0))}

        if self.parent:
            self.parent.OnReceiveData(tr_code, result)


# 주식선물 호가조회
class t8403(XAQuery):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.aps = 5

    def Query(self, code):
        self.ActiveX.LoadFromResFile(self.res_file)
        self.ActiveX.SetFieldData(self.inblock, 'shcode', 0, code)
        self.ActiveX.Request(0)

    def OnReceiveData(self, tr_code):
        result = {'name': str(self.ActiveX.GetFieldData(self.outblock, 'hname', 0)),
                  'futcode': str(self.ActiveX.GetFieldData(self.outblock, 'shcode', 0)),
                  'price': int(self.ActiveX.GetFieldData(self.outblock, 'price', 0)),
                  'offer': int(self.ActiveX.GetFieldData(self.outblock, 'offerho1', 0)),
                  'offer_quantity': int(self.ActiveX.GetFieldData(self.outblock, 'offerrem1', 0)),
                  'bid': int(self.ActiveX.GetFieldData(self.outblock, 'bidho1', 0)),
                  'bid_quantity': int(self.ActiveX.GetFieldData(self.outblock, 'bidrem1', 0))}

        if self.parent:
            self.parent.OnReceiveData(tr_code, result)


# 주식잔고2
class t0424(XAQuery):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.aps = 1

    def Query(self, 계좌번호='', 비밀번호='', 단가구분='1', 체결구분='0', 단일가구분='0', 제비용포함여부='1', CTS_종목번호=''):
        self.ActiveX.LoadFromResFile(self.res_file)
        self.ActiveX.SetFieldData(self.inblock, 'accno', 0, 계좌번호)
        self.ActiveX.SetFieldData(self.inblock, 'passwd', 0, 비밀번호)
        self.ActiveX.SetFieldData(self.inblock, 'prcgb', 0, 단가구분)
        self.ActiveX.SetFieldData(self.inblock, 'chegb', 0, 체결구분)
        self.ActiveX.SetFieldData(self.inblock, 'dangb', 0, 단일가구분)
        self.ActiveX.SetFieldData(self.inblock, 'charge', 0, 제비용포함여부)
        self.ActiveX.SetFieldData(self.inblock, 'cts_expcode', 0, CTS_종목번호)
        self.ActiveX.Request(0)

    def OnReceiveData(self, szTrCode):
        result = []
        nCount = self.ActiveX.GetBlockCount(self.outblock1)
        for i in range(nCount):
            stock_dict = {'shcode': self.ActiveX.GetFieldData(self.outblock1, 'expcode', i).strip(),
                          'name': self.ActiveX.GetFieldData(self.outblock1, 'hname', i).strip(),
                          'current_price': int(self.ActiveX.GetFieldData(self.outblock1, 'price', i).strip()),
                          'remain_quantity': int(self.ActiveX.GetFieldData(self.outblock1, 'janqty', i).strip()),
                          'capable_quantity': int(self.ActiveX.GetFieldData(self.outblock1, 'mdposqt', i).strip()),
                          'deal_price_avg': int(self.ActiveX.GetFieldData(self.outblock1, 'pamt', i).strip()),
                          'deal_price_total': int(self.ActiveX.GetFieldData(self.outblock1, 'mamt', i).strip()),
                          'total_evaluation_price': int(self.ActiveX.GetFieldData(self.outblock1, 'appamt', i).strip()),
                          'profit_and_loss': int(self.ActiveX.GetFieldData(self.outblock1, 'dtsunik', i).strip()),
                          'yield': float(self.ActiveX.GetFieldData(self.outblock1, 'sunikrt', i).strip()),
                          'fee': int(self.ActiveX.GetFieldData(self.outblock1, 'fee', i).strip())}
            result.append(stock_dict)

        if self.parent:
            self.parent.OnReceiveData(szTrCode, result)


# 선물/옵션 잔고평가(이동평균)
class t0441(XAQuery):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.aps = 1

    def Query(self, 계좌번호='', 비밀번호='', CTS_종목번호='', CTS_매매구분=''):
        self.ActiveX.LoadFromResFile(self.res_file)
        self.ActiveX.SetFieldData(self.inblock, 'accno', 0, 계좌번호)
        self.ActiveX.SetFieldData(self.inblock, 'passwd', 0, 비밀번호)
        self.ActiveX.SetFieldData(self.inblock, 'cts_expcode', 0, CTS_종목번호)
        self.ActiveX.SetFieldData(self.inblock, 'cts_medocd', 0, CTS_매매구분)
        self.ActiveX.Request(0)

    def OnReceiveData(self, szTrCode):
        result = []
        nCount = self.ActiveX.GetBlockCount(self.outblock1)
        for i in range(nCount):
            stock_dict = {'shcode': self.ActiveX.GetFieldData(self.outblock1, 'expcode', i).strip(),
                          'current_price': int(float(self.ActiveX.GetFieldData(self.outblock1, 'price', i).strip())),
                          'deal_type': self.ActiveX.GetFieldData(self.outblock1, 'medosu', i).strip(),
                          'deal_code': int(self.ActiveX.GetFieldData(self.outblock1, 'medocd', i).strip()),
                          'remain_quantity': int(self.ActiveX.GetFieldData(self.outblock1, 'jqty', i).strip()),
                          'capable_quantity': int(self.ActiveX.GetFieldData(self.outblock1, 'cqty', i).strip()),
                          'deal_price_avg': float(self.ActiveX.GetFieldData(self.outblock1, 'pamt', i).strip()),
                          'deal_price_total': int(self.ActiveX.GetFieldData(self.outblock1, 'mamt', i).strip()),
                          'total_evaluation_price': int(self.ActiveX.GetFieldData(self.outblock1, 'appamt', i).strip()),
                          'dtsunik': int(self.ActiveX.GetFieldData(self.outblock1, 'dtsunik', i).strip()),
                          'profit_and_loss': int(self.ActiveX.GetFieldData(self.outblock1, 'dtsunik1', i).strip()),
                          'yield': float(self.ActiveX.GetFieldData(self.outblock1, 'sunikrt', i).strip()),
                          'sysprocseq': self.ActiveX.GetFieldData(self.outblock1, 'sysprocseq', i).strip()}
            result.append(stock_dict)

        if self.parent:
            self.parent.OnReceiveData(szTrCode, result)


# 현물계좌 예수금/주문가능금액/총평가 조회(API)
class CSPAQ12200(XAQuery):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.aps = 0.2

    def Query(self, account_number: str, password: str):
        self.ActiveX.LoadFromResFile(self.res_file)
        self.ActiveX.SetFieldData(self.inblock1, 'RecCnt', 0, 1)
        self.ActiveX.SetFieldData(self.inblock1, 'MgmtBrnNo', 0, ' ')
        self.ActiveX.SetFieldData(self.inblock1, 'AcntNo', 0, account_number)
        self.ActiveX.SetFieldData(self.inblock1, 'Pwd', 0, password)
        self.ActiveX.SetFieldData(self.inblock1, 'BalCreTp', 0, '0')
        self.ActiveX.Request(0)

    def OnReceiveData(self, szTrCode):
        result = {'capable_amount': int(self.ActiveX.GetFieldData(self.outblock2, 'MnyOrdAbleAmt', 0).strip())}

        if self.parent:
            self.parent.OnReceiveData(szTrCode, result)


# 선물옵션 계좌예탁금증거금조회
class CFOBQ10500(XAQuery):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.aps = 1

    def Query(self, account_number: str, password: str):
        self.ActiveX.LoadFromResFile(self.res_file)
        self.ActiveX.SetFieldData(self.inblock1, 'RecCnt', 0, 1)
        self.ActiveX.SetFieldData(self.inblock1, 'AcntNo', 0, account_number)
        self.ActiveX.SetFieldData(self.inblock1, 'Pwd', 0, password)
        self.ActiveX.Request(0)

    def OnReceiveData(self, szTrCode):
        result = {'capable_amount': int(self.ActiveX.GetFieldData(self.outblock2, 'MnyOrdAbleAmt', 0).strip())}

        if self.parent:
            self.parent.OnReceiveData(szTrCode, result)
