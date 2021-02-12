from uuid import uuid4
from json import dumps, loads
from http.client import HTTPSConnection

class HotRecharge:
    """
        Hot Recharge Python Api Library
        __author__  Donald Chinhuru
        __version__ 1.3.0
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

    __conn              = HTTPSConnection(__ROOT_ENDPOINT)

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

    def endUserBalance(self, mobile_number: str):
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