import requests
from random import randint

class HotRecharge:
    """
        Hot Recharge web service library
        __author__  Donald Chinhuru
        __version__ 1.1.0
        __name__    Hot Recharge api
    """

    __ROOT_ENDPOINT = "https://ssl.hot.co.zw/api/v1/"
    __MIME_TYPES    = "application/json"

    def __init__(self, headers, use_random_ref=False):
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
            'x-agent-reference': self.headers.get('ref')
        }

    def __autoUpdateRef(self):
        if self.use_random_ref:
            self.headers.update({'x-agent-reference': str(randint(10000, 99999))})


    def updateReference(self, reference):
        """
        update agent-reference field in headers.
        Reference should not be the same for any request made to Hot Recharge web service
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

        wbURI = "agents/wallet-balance"
        uri = self.__ROOT_ENDPOINT + wbURI
        req = requests.get(url=uri, headers=self.headers)

        req.raise_for_status()

        resp = req.json()

        return resp

    def endUserBalance(self, mobile_number=None):
        """
        :param mobile_number:
        :return: End User Balance
        """
        self.__autoUpdateRef()

        eubURI = f"agents/enduser-balance?targetMobile={mobile_number}"
        uri    = self.__ROOT_ENDPOINT + eubURI
        req = requests.get(url=uri, headers=self.headers)

        req.raise_for_status()

        resp = req.json()

        return resp

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
        :return:
        """
        self.__autoUpdateRef()

        body = {
            'Amount': float(amount),
            'TargetMobile': number,
            'BrandID': brandID,
            'CustomerSMS': mesg
        }

        rpURI = "agents/recharge-pinless"
        uri   = self.__ROOT_ENDPOINT + rpURI
        req   = requests.post(url=uri, data=body, headers=self.headers)

        req.raise_for_status()

        resp = req.json()

        return resp

    def dataBundleRecharge(self, product_code, number, amount=None, mesg=None):
        """
        recharge data bundles to `number` target mobile
        :param product_code: bundle product code
        :param number: target mobile in 07xxxxxxxx | 086XXxxxxxx
        :param amount: Optional, value of bundle
        :param mesg: Optional,  customer sms to send
        `mesg` place holders to use:
        %AMOUNT% - $xxx.xx
        %BUNDLE% - name of data bundle
        %ACCESSNAME% - defined by Customer on website – Teller or Trusted User or branch name
        %COMPANYNAME% - as defined by customer on website
        :return:
        """

        self.__autoUpdateRef()

        body = {
            "ProductCode": product_code,
            "Amount": amount,
            "TargetMobile": number,
            "CustomerSMS": mesg
        }

        dbrURI = "agents/recharge-data"
        uri    = self.__ROOT_ENDPOINT + dbrURI
        req    = requests.post(url=uri, data=body, headers=self.headers)

        req.raise_for_status()

        resp = req.json()

        return resp

    def getDataBundles(self):
        """
        get available data bundles
        :return:
        """
        self.__autoUpdateRef()

        gdbURI = "agents/get-data-bundles"
        uri    = self.__ROOT_ENDPOINT + gdbURI
        req    = requests.get(url=uri, headers=self.headers)

        req.raise_for_status()

        resp = req.json()

        return resp
