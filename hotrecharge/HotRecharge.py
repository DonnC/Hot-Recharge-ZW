'''
    @author:    DonnC <https://github.com/DonnC>
    @created:   December 2019
    @updated:   March 2021

    HotRecharge api main class
'''

from uuid import uuid4
from json import dumps, loads
from http.client import HTTPSConnection

class HotRecharge:
    """
        Hot Recharge Python Api Library
        __author__  Donald Chinhuru
        __version__ 1.4.0
        __name__    Hot Recharge Api
    """

    __ROOT_ENDPOINT     = "ssl.hot.co.zw"
    __API_VERSION       = "/api/v1/"
    __MIME_TYPES        = "application/json"

    # endpoints definition
    __RECHARGE_PINLESS  = "agents/recharge-pinless"
    __RECHARGE_DATA     = "agents/recharge-data"
    __WALLET_BALANCE    = "agents/wallet-balance"
    __GET_DATA_BUNDLE   = "agents/get-data-bundles"
    __ENDUSER_BALANCE   = "agents/enduser-balance?targetmobile="
    __QUERY_TRANSACTION = "agents/query-transaction?agentReference="
    __RECHARGE_ZESA     = "agents/recharge-zesa"
    __ZESA_CUSTOMER     = "agents/check-customer-zesa"

    __conn              = HTTPSConnection(__ROOT_ENDPOINT)

    # TODO: make a better way of passing auth keys
    # TODO: consider using a Config class
    def __init__(self, headers: dict, use_random_ref=True):
        self.headers        = headers
        self.use_random_ref = use_random_ref
        self.__headers()

    def __headers(self):
        # for proper auth, headers are required, ref must be 50 char max
        if self.headers.get('ref') and len(self.headers.get('ref')) > 50:
            raise Exception("AGENT Reference must not exceed 50 characters")

        self.headers = {
            'x-access-code': self.headers.get('code'),
            'x-access-password': self.headers.get('pswd'),
            'x-agent-reference': self.headers.get('ref'),
            'content-type': self.__MIME_TYPES,
            'cache-control': "no-cache"
        }

    def __uuidChunkRef(self):
        # simple tokenizer to get a random str as ref from uuid
        # uuid4() example := c1ce5f4a-0596-49a9-aa28-a118f2888122
        uuid_ref =  str(uuid4())
        chunk = uuid_ref.split('-')
        return chunk[0]

    def __autoUpdateRef(self):
        if self.use_random_ref:
            self.headers.update({'x-agent-reference': self.__uuidChunkRef()})

    def updateReference(self, reference: str):
        """
        update agent-reference field in headers.
        Reference should not be the same for any request made to the web service
        :param reference:
        :return: None
        """
        self.headers.update({'x-agent-reference': reference})

    def walletBalance(self):
        """
         Get agent wallet balance
        :return: wallet balance resp
        """
        self.__autoUpdateRef()

        url = f"{self.__API_VERSION}{self.__WALLET_BALANCE}"

        self.__conn.request("GET", url=url, headers=self.headers)

        res  = self.__conn.getresponse()
        data = res.read()

        return loads(data.decode("utf-8"))

    def queryTransactionReference(self, agent_reference):
        """
         Query a transaction for reconciliation: reccommended is to query within the last 30 days of the transaction
        :param: agent_reference := previous record's transaction agentReference used
        :return: api payload -> dict
        """
        self.__autoUpdateRef()

        url = f"{self.__API_VERSION}{self.__QUERY_TRANSACTION}{agent_reference}"

        self.__conn.request("GET", url=url, headers=self.headers)

        res  = self.__conn.getresponse()
        data = res.read()

        return loads(data.decode("utf-8"))

    # TODO: deprecated, will be removed later
    def __endUserBalance(self, mobile_number: str):
        """
        :param mobile_number: str
        :return: End User Balance api response: dict
        """
        self.__autoUpdateRef()

        url = f"{self.__API_VERSION}{self.__ENDUSER_BALANCE}{mobile_number}"

        self.__conn.request("GET", url=url, headers=self.headers)

        res  = self.__conn.getresponse()
        data = res.read()

        return loads(data.decode("utf-8"))

    def rechargePinless(self, amount, number, brandID=None, mesg=None):
        """
        :param amount: a number
        :param number: target phone number
        :param brandID - Optional:
        :param mesg - Optional, Customer sms to send, 135 chars max
        `mesg` place holders to use:
        %AMOUNT% - $xxx.xx
        %INITIALBALANCE% - $xxx.xx
        %FINALBALANCE% - $xxx.xx
        %TXT% - xxx texts
        %DATA% - xxx MB
        %COMPANYNAME% - as defined by Customer on the website www.hot.co.zw
        %ACCESSNAME% - defined by Customer on website – Teller or Trusted User or branch name
        :return: response payload -> dict
        """
        self.__autoUpdateRef()

        payload = dict()
        payload["amount"] = amount
    
        if brandID:
            payload["BrandID"] = brandID 

        else:
            pass

        if mesg:
            if len(mesg) > 135:
                raise Exception("CustomerSMS: `mesg` passed exceeds chars limit of 135 chars")

            payload["CustomerSMS"] = mesg

        else:
            pass 

        if number.startswith('07') or number.startswith('08'):
            payload["targetMobile"] = number

        else:
            raise Exception("targetMobile: `number` passed has incorrect format. Allowed formats are `07xxx..` or `086xxx...`")

        url = f"{self.__API_VERSION}{self.__RECHARGE_PINLESS}"

        self.__conn.request("POST", url, dumps(payload), self.headers)

        res  = self.__conn.getresponse()

        data = res.read()

        return loads(data.decode("utf-8"))

    def dataBundleRecharge(self, product_code, number, amount=None, mesg=None):
        """
        recharge data bundles to `number` target mobile
        :param product_code: bundle product code e.g DWB15 for `weekly data bundle - Econent`
        :param number: target mobile in 07xxxxxxxx | 086XXxxxxxx
        :param amount: Optional, value of bundle
        :param mesg: Optional,  customer sms to send
        `mesg` place holders to use:
        %AMOUNT% - $xxx.xx
        %BUNDLE% - name of data bundle
        %ACCESSNAME% - defined by Customer on website – Teller or Trusted User or branch name
        %COMPANYNAME% - as defined by customer on website
        :return: response dict payload
        """

        self.__autoUpdateRef()

        payload = dict()
        payload["productcode"] = product_code

        if amount:
            payload["amount"] = amount 

        else:
            pass

        if mesg:
            if len(mesg) > 135:
                raise Exception("CustomerSMS: `mesg` passed exceeds chars limit of 135 chars")

            payload["CustomerSMS"] = mesg

        else:
            pass 

        if number.startswith('07') or number.startswith('08'):
            payload["targetMobile"] = number

        else:
            raise Exception("targetMobile: `number` passed has incorrect format. Allowed formats are `07xxx..` or `086xxx...`")

        url = f"{self.__API_VERSION}{self.__RECHARGE_DATA}"

        self.__conn.request("POST", url, dumps(payload), self.headers)

        res  = self.__conn.getresponse()
        data = res.read()

        return loads(data.decode("utf-8"))

    def getDataBundles(self):
        """
        get available data bundles
        :return: dict object containing bundles info and product-codes
        """
        self.__autoUpdateRef()

        url = f"{self.__API_VERSION}{self.__GET_DATA_BUNDLE}"

        self.__conn.request("GET", url=url, headers=self.headers)

        res  = self.__conn.getresponse()
        data = res.read()

        return loads(data.decode("utf-8"))

    def rechargeZesa(self, amount, notify_contact, meter_number, mesg=None):
        '''
            recharge zesa
            amount: should be $50+ per api requirements
            notify_contact: contact to sent zesa token to
            meter_number: the 11 digit meter number to recharge
            mesg: (Optional) custom message to send to user
        '''

        self.__autoUpdateRef()

        payload = dict()

        payload["Amount"] = amount

        payload["meterNumber"] = meter_number

        if mesg:
            if len(mesg) > 135:
                raise Exception("CustomerSMS: `mesg` passed exceeds chars limit of 135 chars")

            payload["CustomerSMS"] = mesg

        else:
            pass 

        if notify_contact.startswith('07'):
            payload["TargetNumber"] = number

        else:
            raise Exception("TargetNumber: `notify_contact` passed has incorrect format. Allowed formats are `07xxx..`")

        url = f"{self.__API_VERSION}{self.__RECHARGE_ZESA}"

        self.__conn.request("POST", url, dumps(payload), self.headers)

        res  = self.__conn.getresponse()

        data = res.read()

        return loads(data.decode("utf-8"))

    def checkZesaCustomer(self, meter_number):
        '''
            check zesa customer. please note! You are advised to first check zesa customer before performing
            zesa recharge, i.e prompt the user to confirm their details first before proceeding
            meter_number: the 11 digit meter number of suer
            :return: on successsful, it returns user information and address, print response for more
        '''

        self.__autoUpdateRef()

        payload = {
            "MeterNumber": meter_number,
        }

        url = f"{self.__API_VERSION}{self.__ZESA_CUSTOMER}"

        self.__conn.request("POST", url, dumps(payload), self.headers)

        res  = self.__conn.getresponse()

        data = res.read()

        return loads(data.decode("utf-8"))