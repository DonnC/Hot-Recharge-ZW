# @author:  DonnC Lab
# @created: Jun 2021

from munch import Munch

from .HotRechargeException import *


class ApiExceptionHandler:
    """ApiExceptionHandler

    Handles api request [ReplyCode] and throw appropriate exception
    """

    def __init__(self, response: Munch, is_429_401: int = None):
        self.response = response
        self.is_429_401 = is_429_401

        # handle errors
        self.__process_response()

    def __process_response(self):
        # process api response for exceptions
        # raise exception if any is found
        _msg = self.__message_getter()

        if hasattr(self.response, "ReplyCode"):
            if int(self.response.ReplyCode) != 2:
                raise self.__switcher(_msg).get(
                    int(self.response.ReplyCode), HotRechargeException(_msg)
                )

        if self.is_429_401:
            raise self.__switcher(_msg).get(self.is_429_401, HotRechargeException(_msg))

        else:
            # raise default error
            raise HotRechargeException(_msg)

    def __switcher(self, message: str) -> dict:
        api_exception_mapper = {
            4: PendingZesaTransaction(message),
            206: PrepaidPlatformFail(message),
            208: InsufficientBalance(message),
            209: OutOfPinStock(message),
            210: PrepaidPlatformFail(message),
            216: DuplicateRequestException(message),
            217: InvalidContact(message),
            218: AuthorizationError(message),
            219: WebServiceException(message),
            220: AuthorizationError(message),
            221: BalanceRequestError(message),
            222: RechargeAmountLimit(message),
            # -------- http status code -----------
            401: AuthorizationError(message),
            429: DuplicateReference(message),
            # -------------------------------------
            800: TransactionNotFound(message),
        }

        return api_exception_mapper

    def __message_getter(self) -> str:
        # get appropriate message from api response

        if hasattr(self.response, "Message"):
            return self.response.Message

        if hasattr(self.response, "ReplyMessage"):
            return self.response.ReplyMessage

        if hasattr(self.response, "ReplyMsg"):
            return self.response.ReplyMsg

        else:
            return self.response.toDict().__str__
