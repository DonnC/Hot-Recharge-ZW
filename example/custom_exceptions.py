# demo to show api throwing custom api exceptions
import hotrecharge

# create config class
config = hotrecharge.HRAuthConfig(
    access_code="acc-email",
    access_password="acc-pwd",
)

api = hotrecharge.HotRecharge(config)

try:
    response = api.queryZesaTransaction(recharge_id="un-existing-rechargeid")

    print(response)

# api now throws custom HotRechargeExceptions
# HotRechargeException is a base class Exception for all api exceptions
# you can narrow it down with specific exception
except hotrecharge.HotRechargeException as err:
    print("[HR Error] Api error: ", err)

# example to show, checking specific api exception
try:
    response = api.rechargePinless(10, "invalid-network-number")  # can try one like -> 0752782828

    print(response)

# can narrow it down to except InvalidContact exception
except hotrecharge.InvalidContact as err:
    print("[InvalidContactException] Error: ", err)
