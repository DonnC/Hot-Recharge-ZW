"""
    @author:    DonnC <https://github.com/DonnC>
    @created:   December 2019
    @updated:   June 2021

    HotRecharge api main class
"""

from uuid import uuid4
from json import dumps, loads
from munch import Munch, munchify
from http.client import HTTPSConnection

from .HRConfig import HRAuthConfig
from .HotRechargeExcHandler import ApiExceptionHandler


class HotRecharge:
    """
    Hot Recharge Python Api Library
    __author__  Donald Chinhuru
    __version__ 3.3.1
    __name__    Hot Recharge Api
    """

    __ROOT_ENDPOINT = "ssl.hot.co.zw"
    __API_VERSION = "/api/v1/"
    __MIME_TYPES = "application/json"

    # endpoints definition
    __RECHARGE_PINLESS = "agents/recharge-pinless"
    __RECHARGE_DATA = "agents/recharge-data"
    __WALLET_BALANCE = "agents/wallet-balance"
    __GET_DATA_BUNDLE = "agents/get-data-bundles"
    __ENDUSER_BALANCE = "agents/enduser-balance?targetmobile="
    __QUERY_TRANSACTION = "agents/query-transaction?agentReference="
    __QUERY_ZESA = "agents/query-zesa-transaction"
    __RECHARGE_ZESA = "agents/recharge-zesa"
    __ZESA_CUSTOMER = "agents/check-customer-zesa"
    __ZESA_BALANCE = "agents/wallet-balance-zesa"
    __QUERY_EVD = "agents/query-evd"
    __RECHARGE_EVD = "agents/recharge-evd"

    __conn = HTTPSConnection(__ROOT_ENDPOINT)
    __headers = {}

    def __init__(
        self,
        config: HRAuthConfig,
        use_random_ref: bool = True,
        return_model: bool = False,
    ):
        """[HotRecharge]

        Args:
            `config` (HRAuthConfig): config class object to hold auth credentials
            `use_random_ref` (bool, optional): True -> let library take care of each request unique reference.
                False -> you must provide a unique reference for each request manually by calling 
                
                >>> api.updateReference('unique-ref')

                Defaults to True.

            `return_model` (bool, optional): True -> return a python model class equivalent of the respond object
                It uses a simple mechanism from [Munch], returns a Munch Object Model

                if api response is:
                >>> response = {
                        'AgentReference': agentReference,
                        'ReplyCode': replyCode,
                        'ReplyMsg': replyMsg,
                        'WalletBalance': walletBalance,
                    }

                it will return a Munch model

                >>> model = Munch(response)

                and attributes will be accessible using the dot (.) operator like class attributes

                >>> print(model.AgentReference)

                >>> print(model.WalletBalance)


                False -> returns a dict python object instead.

                Defaults to False.
        """
        self.use_random_ref = use_random_ref
        self.config = config
        self.return_model = return_model
        self.__setupHeaders()

    def __setupHeaders(self):
        if self.config:
            # print(self.config)

            if self.use_random_ref:
                self.__headers = {
                    "x-access-code": self.config.access_code,
                    "x-access-password": self.config.access_password,
                    "x-agent-reference": self.__uuidChunkRef(),
                    "content-type": self.__MIME_TYPES,
                    "cache-control": "no-cache",
                }

            else:
                self.__headers = {
                    "x-access-code": self.config.access_code,
                    "x-access-password": self.config.access_password,
                    "x-agent-reference": self.config.reference,
                    "content-type": self.__MIME_TYPES,
                    "cache-control": "no-cache",
                }

    def __uuidChunkRef(self):
        # simple tokenizer to get a random str as ref from uuid
        # uuid4() example := c1ce5f4a-0596-49a9-aa28-a118f2888122
        uuid_ref = str(uuid4())
        chunk = uuid_ref.split("-")
        return chunk[0]

    def __autoUpdateRef(self):
        if self.use_random_ref:
            self.__headers.update({"x-agent-reference": self.__uuidChunkRef()})

    def updateReference(self, reference: str) -> None:
        """
        update agent-reference field in headers.
        Reference should not be the same for any request made to the web service
        :param reference:
        :return: None
        """
        self.__headers.update({"x-agent-reference": reference})

    def walletBalance(self) -> Munch or dict:
        """
         Get agent wallet balance
        :return: wallet balance resp or Munch equivalent

        >>> {
            'AgentReference': agentReference,
            'ReplyCode': replyCode,
            'ReplyMsg': replyMsg,
            'WalletBalance': walletBalance,
        }
        """
        self.__autoUpdateRef()

        url = f"{self.__API_VERSION}{self.__WALLET_BALANCE}"

        resp = self.__conn.request("GET", url=url, headers=self.__headers)

        res = self.__conn.getresponse()

        data = res.read()

        status_code = res.status

        _json_data = loads(data.decode("utf-8"))

        _munch_obj = munchify(_json_data)

        if hasattr(_munch_obj, "ReplyCode"):
            if _munch_obj.ReplyCode == 2:

                if self.return_model:
                    return _munch_obj

                return _json_data

            else:
                pass

        if status_code == 401 or 429:
            ApiExceptionHandler(response=_munch_obj, is_429_401=status_code)

        ApiExceptionHandler(response=_munch_obj)

    def queryTransactionReference(self, agent_reference) -> dict or Munch:
        """
         Query a transaction for reconciliation: reccommended is to query within the last 30 days of the transaction
        :param: agent_reference := previous record's transaction agentReference used
        :return: api payload -> dict
        :OriginalAgentReference -> object of original transaction response

        >>> {
                'ReplyCode': replyCode,
                'ReplyMsg': replyMsg,
                'OriginalAgentReference': originalAgentReference,
                'RawReply': rawReply,
                'AgentReference': agentReference,
             }
        """
        self.__autoUpdateRef()

        url = f"{self.__API_VERSION}{self.__QUERY_TRANSACTION}{agent_reference}"

        self.__conn.request("GET", url=url, headers=self.__headers)

        res = self.__conn.getresponse()
        data = res.read()

        status_code = res.status

        _json_data = loads(data.decode("utf-8"))

        _munch_obj = munchify(_json_data)

        if hasattr(_munch_obj, "ReplyCode"):
            if _munch_obj.ReplyCode == 2:
                if self.return_model:
                    return _munch_obj

                return _json_data

            else:
                pass

        if status_code == 401 or 429:
            ApiExceptionHandler(response=_munch_obj, is_429_401=status_code)

        ApiExceptionHandler(response=_munch_obj)

    def rechargePinless(self, amount, number, brandID=None, mesg=None) -> dict or Munch:
        """
        :param amount: a number
        :param number: target phone number in formart 07xx.. or 086xx..
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

        >>> {
            'AgentReference': agentReference,
            'Amount': amount,
            'Data': data,
            'Discount': discount,
            'FinalBalance': finalBalance,
            'InitialBalance': initialBalance,
            'RechargeID': rechargeID,
            'ReplyCode': replyCode,
            'ReplyMsg': replyMsg,
            'SMS': sms,
            'WalletBalance': walletBalance,
            'Window': window,
        }
        """
        self.__autoUpdateRef()

        payload = dict()
        payload["amount"] = amount

        if brandID:
            payload["BrandID"] = brandID

        else:
            pass

        if mesg:
            # if len(mesg) > 135:
            #    raise Exception("CustomerSMS: `mesg` passed exceeds chars limit of 135 chars")

            payload["CustomerSMS"] = mesg

        else:
            pass

        payload["targetMobile"] = number

        url = f"{self.__API_VERSION}{self.__RECHARGE_PINLESS}"

        self.__conn.request("POST", url, dumps(payload), self.__headers)

        res = self.__conn.getresponse()

        data = res.read()

        status_code = res.status

        _json_data = loads(data.decode("utf-8"))

        _munch_obj = munchify(_json_data)

        if hasattr(_munch_obj, "ReplyCode"):
            if _munch_obj.ReplyCode == 2:
                if self.return_model:
                    return _munch_obj

                return _json_data

            else:
                pass

        if status_code == 401 or 429:
            ApiExceptionHandler(response=_munch_obj, is_429_401=status_code)

        ApiExceptionHandler(response=_munch_obj)

    def dataBundleRecharge(
        self, product_code, number, amount=None, mesg=None
    ) -> dict or Munch:
        """
        recharge data bundles to `number` target mobile
        :param product_code: bundle product code e.g DWB15 for `weekly data bundle - Econet`
        :param number: target mobile in 07xxxxxxxx | 086XXxxxxxx
        :param amount: Optional, value of bundle
        :param mesg: Optional,  customer sms to send
        `mesg` place holders to use:
        %AMOUNT% - $xxx.xx
        %BUNDLE% - name of data bundle
        %ACCESSNAME% - defined by Customer on website – Teller or Trusted User or branch name
        %COMPANYNAME% - as defined by customer on website
        :return: response dict payload

        >>> {
            'AgentReference': agentReference,
            'Amount': amount,
            'Data': data,
            'Discount': discount,
            'FinalBalance': finalBalance,
            'InitialBalance': initialBalance,
            'RechargeID': rechargeID,
            'ReplyCode': replyCode,
            'ReplyMsg': replyMsg,
            'SMS': sms,
            'WalletBalance': walletBalance,
            'Window': window,
        }
        """

        self.__autoUpdateRef()

        payload = dict()
        payload["ProductCode"] = product_code

        if amount:
            payload["Amount"] = amount

        else:
            pass

        if mesg:
            # if len(mesg) > 135:
            #    raise Exception("CustomerSMS: `mesg` passed exceeds chars limit of 135 chars")

            payload["CustomerSMS"] = mesg

        else:
            pass

        payload["TargetMobile"] = number

        url = f"{self.__API_VERSION}{self.__RECHARGE_DATA}"

        self.__conn.request("POST", url, dumps(payload), self.__headers)

        res = self.__conn.getresponse()
        data = res.read()

        status_code = res.status

        _json_data = loads(data.decode("utf-8"))

        _munch_obj = munchify(_json_data)

        if hasattr(_munch_obj, "ReplyCode"):
            if _munch_obj.ReplyCode == 2:
                if self.return_model:
                    return _munch_obj

                return _json_data

            else:
                pass

        if status_code == 401 or 429:
            ApiExceptionHandler(response=_munch_obj, is_429_401=status_code)

        ApiExceptionHandler(response=_munch_obj)

    def rechargeEVD(self, brand_id, pin_value, number, quantity=1) -> dict or Munch:
        """
        recharge evd to `number` target mobile, voucher pin will be send to `number`
        :param brand_id: brand id of evd as got from `api.getEVD()` e.g 24
        :param pin_value: evd value as float, (used to be Denomination)
        :param number: contact number to sent voucher pin, usually netone
        :param quantity: number of voucher pins to purchase

        :return: response dict payload
        on successful, *Pins will be a list of string : PIN, SerialNumber, BrandID, Denomination (PinValue), Expiry
        e.g ['0812273518776434,008101288101|17,.50,3/27/2021']

        >>> {
            'AgentReference': agentReference,
            'Amount': amount,
            'Discount': discount,
            'RechargeID': rechargeID,
            'ReplyCode': replyCode,
            'ReplyMsg': replyMsg,
            'Pins': [pin],
            'WalletBalance': walletBalance,
        }
        """

        self.__autoUpdateRef()

        payload = dict()
        payload["BrandID"] = str(brand_id)
        payload["Denomination"] = str(pin_value)
        payload["Quantity"] = str(quantity)
        payload["TargetNumber"] = number

        url = f"{self.__API_VERSION}{self.__RECHARGE_EVD}"

        self.__conn.request("POST", url, dumps(payload), self.__headers)

        res = self.__conn.getresponse()
        data = res.read()

        status_code = res.status

        _json_data = loads(data.decode("utf-8"))

        _munch_obj = munchify(_json_data)

        if hasattr(_munch_obj, "ReplyCode"):
            if _munch_obj.ReplyCode == 2:
                if self.return_model:
                    return _munch_obj

                return _json_data

            else:
                pass

        if status_code == 401 or 429:
            ApiExceptionHandler(response=_munch_obj, is_429_401=status_code)

        ApiExceptionHandler(response=_munch_obj)

    def getDataBundles(self) -> dict or Munch:
        """
        get available data bundles
        :return: dict object containing bundles info and product-codes

        >>> {
            'ReplyCode': replyCode,
            'Bundles': [bundle],
            'AgentReference': agentReference,
        }

        :bundle: list of `bundle` object
        >>> {
            'BundleId': bundleId,
            'BrandId': brandId,
            'Network': network,
            'ProductCode': productCode,
            'Amount': amount,
            'Name': name,
            'Description': description,
            'Validity': validity,
        }
        """
        self.__autoUpdateRef()

        url = f"{self.__API_VERSION}{self.__GET_DATA_BUNDLE}"

        self.__conn.request("GET", url=url, headers=self.__headers)

        res = self.__conn.getresponse()
        data = res.read()

        status_code = res.status

        _json_data = loads(data.decode("utf-8"))

        _munch_obj = munchify(_json_data)

        if hasattr(_munch_obj, "ReplyCode"):
            if _munch_obj.ReplyCode == 2:
                if self.return_model:
                    return _munch_obj

                return _json_data

            else:
                pass

        if status_code == 401 or 429:
            ApiExceptionHandler(response=_munch_obj, is_429_401=status_code)

        ApiExceptionHandler(response=_munch_obj)

    def getEVDs(self) -> dict or Munch:
        """
        query evds (electronic vouchers)
        *PinValue ==  Denomination in some context
        :return: dict object containing evds

        >>> {
            'ReplyCode': replyCode,
            'ReplyMsg': replyMsg,
            'InStock': [in_stock],
            'AgentReference': agentReference,
        }

        :in_stock: list of stock object
        >>> {
            'BrandId': brandId,
            'BrandName': brandName,
            'PinValue': pinValue,
            'Stock': stock,
        }
        """
        self.__autoUpdateRef()

        url = f"{self.__API_VERSION}{self.__QUERY_EVD}"

        self.__conn.request("GET", url=url, headers=self.__headers)

        res = self.__conn.getresponse()
        data = res.read()

        status_code = res.status

        _json_data = loads(data.decode("utf-8"))

        _munch_obj = munchify(_json_data)

        if hasattr(_munch_obj, "ReplyCode"):
            if _munch_obj.ReplyCode == 2:
                if self.return_model:
                    return _munch_obj

                return _json_data

            else:
                pass

        if status_code == 401 or 429:
            ApiExceptionHandler(response=_munch_obj, is_429_401=status_code)

        ApiExceptionHandler(response=_munch_obj)

    def rechargeZesa(
        self, amount, notify_contact, meter_number, mesg=None
    ) -> dict or Munch:
        """
        recharge zesa
        amount: should be $50+ per api requirements
        notify_contact: contact to sent zesa token to
        meter_number: the 11 digit meter number to recharge
        mesg: (Optional) custom message to send to user

        :return:
        >>> {
            'ReplyCode': replyCode,
            'ReplyMsg': replyMsg,
            'WalletBalance': walletBalance,
            'Amount': amount,
            'Discount': discount,
            'Meter': meter,
            'AccountName': accountName,
            'Address': address,
            'Tokens': [token],
            'AgentReference': agentReference,
            'RechargeID': rechargeID,
        }

        :token: list of token object
        >>> {
            'Token': token,
            'Units': units,
            'NetAmount': netAmount,
            'Levy': levy,
            'Arrears': arrears,
            'TaxAmount': taxAmount,
            'ZesaReference': zesaReference,
        }

        If it throws `ZesaPendingTransaction` excpetion, see ZesaPendingTransaction docstrings for more
        """

        self.__autoUpdateRef()

        payload = dict()

        payload["Amount"] = amount

        payload["meterNumber"] = meter_number

        if mesg:
            # if len(mesg) > 135:
            #    raise Exception("CustomerSMS: `mesg` passed exceeds chars limit of 135 chars")

            payload["CustomerSMS"] = mesg

        else:
            pass

        payload["TargetNumber"] = notify_contact

        url = f"{self.__API_VERSION}{self.__RECHARGE_ZESA}"

        self.__conn.request("POST", url, dumps(payload), self.__headers)

        res = self.__conn.getresponse()

        data = res.read()

        status_code = res.status

        _json_data = loads(data.decode("utf-8"))

        _munch_obj = munchify(_json_data)

        if hasattr(_munch_obj, "ReplyCode"):
            if _munch_obj.ReplyCode == 2:
                if self.return_model:
                    return _munch_obj

                return _json_data

            else:
                pass

        if status_code == 401 or 429:
            ApiExceptionHandler(response=_munch_obj, is_429_401=status_code)

        ApiExceptionHandler(response=_munch_obj)

    def checkZesaCustomer(self, meter_number) -> dict or Munch:
        """
        check zesa customer. please note! You are advised to first check zesa customer before performing
        zesa recharge, i.e prompt the user to confirm their details first before proceeding
        meter_number: the 11 digit meter number of suer
        :return: on successsful, it returns user information and address, print response for more

        >>> {
            'ReplyCode': replyCode,
            'ReplyMsg': replyMsg,
            'Meter': meter,
            'AgentReference': agentReference,
            'CustomerInfo': <customer>,
        }

        :customer:
        >>> {
            'CustomerName': customerName,
            'Address': address,
            'MeterNumber': meterNumber,
            'Reference': reference,
        }

        """

        self.__autoUpdateRef()

        payload = {
            "MeterNumber": meter_number,
        }

        url = f"{self.__API_VERSION}{self.__ZESA_CUSTOMER}"

        self.__conn.request("POST", url, dumps(payload), self.__headers)

        res = self.__conn.getresponse()

        data = res.read()

        status_code = res.status

        _json_data = loads(data.decode("utf-8"))

        _munch_obj = munchify(_json_data)

        if hasattr(_munch_obj, "ReplyCode"):
            if _munch_obj.ReplyCode == 2:
                if self.return_model:
                    return _munch_obj

                return _json_data

            else:
                pass

        if status_code == 401 or 429:
            ApiExceptionHandler(response=_munch_obj, is_429_401=status_code)

        ApiExceptionHandler(response=_munch_obj)

    def zesaWalletBalance(self) -> dict or Munch:
        """
         Get agent zesa wallet balance
        :return: zesa wallet balance resp

        >>> {
            'AgentReference': agentReference,
            'ReplyCode': replyCode,
            'ReplyMsg': replyMsg,
            'WalletBalance': walletBalance,
        }
        """

        self.__autoUpdateRef()

        url = f"{self.__API_VERSION}{self.__ZESA_BALANCE}"

        resp = self.__conn.request("GET", url=url, headers=self.__headers)

        res = self.__conn.getresponse()

        data = res.read()

        status_code = res.status

        _json_data = loads(data.decode("utf-8"))

        _munch_obj = munchify(_json_data)

        if hasattr(_munch_obj, "ReplyCode"):
            if _munch_obj.ReplyCode == 2:
                if self.return_model:
                    return _munch_obj

                return _json_data

            else:
                pass

        if status_code == 401 or 429:
            ApiExceptionHandler(response=_munch_obj, is_429_401=status_code)

        ApiExceptionHandler(response=_munch_obj)

    def queryZesaTransaction(self, recharge_id) -> dict or Munch:
        """
         Query a zesa transaction for reconciliation: reccommended is to query within the last 30 days of the transaction
        :param: recharge_id := previous zesa record's transaction RechargeId returned
        :return: api payload -> dict | Munch obj

        >>> {
            'ReplyCode': replyCode,
            'ReplyMsg': replyMsg,
            'WalletBalance': walletBalance,
            'Amount': amount,
            'Discount': discount,
            'Meter': meter,
            'AccountName': accountName,
            'Address': address,
            'Tokens': [tokens],
            'AgentReference': agentReference,
            'RechargeID': rechargeID,
            'CustomerInfo': <customer>,
        }

        :tokens: list of token object
        >>> {
            'Token': token,
            'Units': units,
            'NetAmount': netAmount,
            'Levy': levy,
            'Arrears': arrears,
            'TaxAmount': taxAmount,
            'ZesaReference': zesaReference,
        }

        :customer:
        >>> {
            'CustomerName': customerName,
            'Address': address,
            'MeterNumber': meterNumber,
            'Reference': reference,
        }
        """
        self.__autoUpdateRef()

        payload = {"RechargeId": str(recharge_id)}

        url = f"{self.__API_VERSION}{self.__QUERY_ZESA}"

        self.__conn.request("POST", url, dumps(payload), self.__headers)

        res = self.__conn.getresponse()

        data = res.read()

        status_code = res.status

        _json_data = loads(data.decode("utf-8"))

        _munch_obj = munchify(_json_data)

        if hasattr(_munch_obj, "ReplyCode"):
            if _munch_obj.ReplyCode == 2:
                if self.return_model:
                    return _munch_obj

                return _json_data

            else:
                pass

        if status_code == 401 or 429:
            ApiExceptionHandler(response=_munch_obj, is_429_401=status_code)

        ApiExceptionHandler(response=_munch_obj)
