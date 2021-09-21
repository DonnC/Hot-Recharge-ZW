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
                    int(self.response.ReplyCode), HotRechargeException(_msg, self.response)
                )

        if self.is_429_401:
            raise self.__switcher(_msg).get(self.is_429_401, HotRechargeException(_msg, self.response))

        else:
            # raise default error
            raise HotRechargeException(_msg, self.response)

    def __switcher(self, message: str) -> dict:
        api_exception_mapper = {
            4: PendingZesaTransaction(message, self.response),
            206: PrepaidPlatformFail(message, self.response),
            208: InsufficientBalance(message, self.response),
            209: OutOfPinStock(message, self.response),
            210: PrepaidPlatformFail(message, self.response),
            216: DuplicateRequestException(message, self.response),
            217: InvalidContact(message, self.response),
            218: AuthorizationError(message, self.response),
            219: WebServiceException(message, self.response),
            220: AuthorizationError(message, self.response),
            221: BalanceRequestError(message, self.response),
            222: RechargeAmountLimit(message, self.response),
            # -------- http status code -----------
            401: AuthorizationError(message, self.response),
            429: DuplicateReference(message, self.response),
            # -------------------------------------
            800: TransactionNotFound(message, self.response),
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
