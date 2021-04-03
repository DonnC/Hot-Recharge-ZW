'''
    @author:    DonnC <https://github.com/DonnC>
    @created:   December 2019
    @updated:   April 2021

    HotRecharge api main class
'''

from uuid import uuid4
from json import dumps, loads
from http.client import HTTPSConnection

from .HRConfig import HRAuthConfig

class HotRecharge:
    """
        Hot Recharge Python Api Library
        __author__  Donald Chinhuru
        __version__ 2.0.0
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
    __QUERY_EVD         = "agents/query-evd"
    __RECHARGE_EVD      = "agents/recharge-evd"

    __conn              = HTTPSConnection(__ROOT_ENDPOINT)
    __headers           = {}

    def __init__(self, config: HRAuthConfig, use_random_ref=True):
        self.use_random_ref = use_random_ref
        self.config         = config
        self.__setupHeaders()

    def __setupHeaders(self):
        if self.config:
            #print(self.config)

            if self.use_random_ref:
                self.__headers = {
                    'x-access-code': self.config.access_code,
                    'x-access-password': self.config.access_password,
                    'x-agent-reference': self.__uuidChunkRef(),
                    'content-type': self.__MIME_TYPES,
                    'cache-control': "no-cache"
                }

            else:
                self.__headers = {
                    'x-access-code': self.config.access_code,
                    'x-access-password': self.config.access_password,
                    'x-agent-reference': self.config.reference,
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
            self.__headers.update({'x-agent-reference': self.__uuidChunkRef()})

    def updateReference(self, reference: str):
        """
        update agent-reference field in headers.
        Reference should not be the same for any request made to the web service
        :param reference:
        :return: None
        """
        self.__headers.update({'x-agent-reference': reference})

    def walletBalance(self):
        """
         Get agent wallet balance
        :return: wallet balance resp
        """
        self.__autoUpdateRef()

        url = f"{self.__API_VERSION}{self.__WALLET_BALANCE}"

        self.__conn.request("GET", url=url, headers=self.__headers)

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

        self.__conn.request("GET", url=url, headers=self.__headers)

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
            #if len(mesg) > 135:
            #    raise Exception("CustomerSMS: `mesg` passed exceeds chars limit of 135 chars")

            payload["CustomerSMS"] = mesg

        else:
            pass 

        if number.startswith('07') or number.startswith('08'):
            payload["targetMobile"] = number

        else:
            raise Exception("targetMobile: `number` passed has incorrect format. Allowed formats are `07xxx..` or `086xxx...`")

        url = f"{self.__API_VERSION}{self.__RECHARGE_PINLESS}"

        self.__conn.request("POST", url, dumps(payload), self.__headers)

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
        payload["ProductCode"] = product_code

        if amount:
            payload["Amount"] = amount 

        else:
            pass

        if mesg:
            #if len(mesg) > 135:
            #    raise Exception("CustomerSMS: `mesg` passed exceeds chars limit of 135 chars")

            payload["CustomerSMS"] = mesg

        else:
            pass 

        if number.startswith('07') or number.startswith('08'):
            payload["TargetMobile"] = number

        else:
            raise Exception("targetMobile: `number` passed has incorrect format. Allowed formats are `07xxx..` or `086xxx...`")

        url = f"{self.__API_VERSION}{self.__RECHARGE_DATA}"

        self.__conn.request("POST", url, dumps(payload), self.__headers)

        res  = self.__conn.getresponse()
        data = res.read()

        return loads(data.decode("utf-8"))

    def rechargeEVD(self, brand_id, pin_value, number, quantity=1):
        """
        recharge evd to `number` target mobile, voucher pin will be send to `number`
        :param brand_id: brand id of evd as got from `api.getEVD()` e.g 24
        :param pin_value: evd value as float, (used to be Denomination)
        :param number: contact number to sent voucher pin, usually netone
        :param quantity: number of voucher pins to purchase
 
        :return: response dict payload
        on successful, pins will be a list of string : PIN, SerialNumber, BrandID, Denomination, Expiry
        e.g ['0812273518776434,008101288101|17,.50,3/27/2021']
        """

        self.__autoUpdateRef()

        payload = dict()
        payload["BrandID"] = str(brand_id)
        payload["Denomination"] = str(pin_value)
        payload["Quantity"] = str(quantity)

        if number.startswith('07') or number.startswith('08'):
            payload["TargetNumber"] = number

        else:
            raise Exception("targetNumber: `number` passed has incorrect format. Allowed formats are `07xxx..` or `086xxx...`")

        url = f"{self.__API_VERSION}{self.__RECHARGE_EVD}"

        self.__conn.request("POST", url, dumps(payload), self.__headers)

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

        self.__conn.request("GET", url=url, headers=self.__headers)

        res  = self.__conn.getresponse()
        data = res.read()

        return loads(data.decode("utf-8"))

    def getEVDs(self):
        """
        query evds (electronic vouchers)
        :return: dict object containing evds
        """
        self.__autoUpdateRef()

        url = f"{self.__API_VERSION}{self.__QUERY_EVD}"

        self.__conn.request("GET", url=url, headers=self.__headers)

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
            #if len(mesg) > 135:
            #    raise Exception("CustomerSMS: `mesg` passed exceeds chars limit of 135 chars")

            payload["CustomerSMS"] = mesg

        else:
            pass 

        if notify_contact.startswith('07'):
            payload["TargetNumber"] = number

        else:
            raise Exception("TargetNumber: `notify_contact` passed has incorrect format. Allowed formats are `07xxx..`")

        url = f"{self.__API_VERSION}{self.__RECHARGE_ZESA}"

        self.__conn.request("POST", url, dumps(payload), self.__headers)

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

        self.__conn.request("POST", url, dumps(payload), self.__headers)

        res  = self.__conn.getresponse()

        data = res.read()

        return loads(data.decode("utf-8"))