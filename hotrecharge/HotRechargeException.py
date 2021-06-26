"""
@author: DonnC Lab <https://github.com/DonnC>
@created: June 2021
@updated: June 2021

    - api custom response exceptions
    - force to throw exceptions when api response has error
"""


class HotRechargeException(Exception):
    """HotRechargeException base exception for api exceptions

    Args:
        Exception ([type]): [description]
    """

    pass


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
