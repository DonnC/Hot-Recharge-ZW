"""
@author: DonnC Lab <https://github.com/DonnC>
@created: June 2021
@updated: June 2021

    - api custom response exceptions
    - force to throw exceptions when api response has error
"""

from munch import Munch


class HotRechargeException(Exception):
    """HotRechargeException base exception for api exceptions

    Args:
        Exception (HotRechargeException): base exception for all other api exceptions
                                          you can use this base class if you are not sure which specific exception to target although its not good practise
    """

    def __init__(self, message, response:Munch = None):
        super().__init__(message)
        self.message = message
        self.response = response


class DuplicateReference(HotRechargeException):
    """DuplicateReference Exception

    Args:
        HotRechargeException (DuplicateReference): unique reference should be provided per each request
    """

    pass


class AuthorizationError(HotRechargeException):
    """AuthorizationError Exception

    Args:
        HotRechargeException (AuthorizationError): password or access-code is wrong or failed to login
    """

    pass


class InvalidContact(HotRechargeException):
    """InvalidContact Exception

    Args:
        HotRechargeException (InvalidContact): wrong number to recharge or invalid network
    """

    pass


class PendingZesaTransaction(HotRechargeException):
    """PendingZesaTransaction Exception

    Args:
        HotRechargeException (PendingZesaTransaction): indicates Pending Zesa Verification

        Transactions in this state can result in successful transactions after a period of time once Zesa completes transaction / verification.

        If it happens, you can call the below method periodically to poll transaction status

        Request should not exceed more than 4 requests / minute
        >>> zesa_trans = api.queryZesaTransaction('<recharge-id>')


    """

    pass


class PrepaidPlatformFail(HotRechargeException):
    """PrepaidPlatformFail Exception

    Failed Recharge Network Prepaid Platform
    """

    pass


class RechargeAmountLimit(HotRechargeException):
    """RechargeAmountLimit Exception

    Failed recharge amount limit, too little / too much
    """

    pass


class ReferenceExceedLimit(HotRechargeException):
    """ReferenceExceedLimit Exception

    passed reference exceeds required limit
    """

    pass


class InsufficientBalance(HotRechargeException):
    """InsufficientBalance Exception

    not enough wallet balance
    """

    pass


class ServiceError(HotRechargeException):
    """ServiceError Exception

    recharge platform is down
    """

    pass


class OutOfPinStock(HotRechargeException):
    """OutOfPinStock Exception

    request received but provider does not have correct stock to process
    """

    pass


class WebServiceException(HotRechargeException):
    """WebServiceException Exception"""

    pass


class BalanceRequestError(HotRechargeException):
    """BalanceRequestError Exception

    possible cause: contract line or invalid number or invalid formart
    """

    pass


class DuplicateRequestException(HotRechargeException):
    """DuplicateRequest Exception

    api already received the request and is being processed
    """

    pass


class TransactionNotFound(HotRechargeException):
    """TransactionNotFound Exception

    the transaction could not be found, possibly failed to locate original transaction data
    or query request performed way after threshold days (30 days)
    """

    pass
