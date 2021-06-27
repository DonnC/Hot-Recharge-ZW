# a hot-recharge auth config class

from .HotRechargeException import ReferenceExceedLimit


class HRAuthConfig:
    """
    a hot-recharge auth credentials config

    `access_code`: account email as used on registration
    `access_password`: account password as used on reg
    `reference` (optional): any random chars to use as initial reference
    """

    access_code = str
    access_password = str
    reference = str

    def __init__(self, access_code: str, access_password: str, reference=None):
        self.access_code = access_code
        self.access_password = access_password
        self.reference = reference

        self.__checkReferenceLimit()

    def __checkReferenceLimit(self):
        """
        private method to check reference max limit allowed
        """
        # for proper auth, headers are required, ref must be 50 char max
        if self.reference:
            if len(self.reference) > 50:
                raise ReferenceExceedLimit("reference must not exceed 50 characters")

    def set_access_code(self, access_code: str):
        """
        set config access code
        account email used on registration
        """
        self.access_code = access_code

    def set_access_password(self, access_password: str):
        """
        set config access password
        account passowrd used on registration
        """
        self.access_password = access_password

    def set_reference(self, reference: str):
        """
        set config initial reference
        a unique reference string, max of 50 chars
        """
        self.reference = reference

        self.__checkReferenceLimit()

    def __repr__(self):
        return f"<HotRechargeAuthConfig: {self.access_code}, {self.access_password}, {self.reference}>"
