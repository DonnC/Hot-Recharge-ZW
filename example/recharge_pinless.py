# recharge_pinless.py
# @author:  Donald Chinhuru
# @created: 09 Dec 2019
# @updated: 09 Dec 2019

import hotrecharge
import sys

credentials = {
    'code': '<your-code>',
    'pswd': '<your-password',
    'ref': '<agent-reference>'
}

# to use random code generated references, flag it to True
api = hotrecharge.HotRecharge(headers=credentials, use_random_ref=False)

try:
    # recharge pinless with a (OPTIONAL) custom Customer SMS, max char should not exceed 135
    # uses places holders as used on hot recharge registration
    customer_sms = "Recharge of %AMOUNT% successful" \
                   "Initial balance $%INITIALBALANCE%" \
                   "Final Balance $%FINALBALANCE%" \
                   "Thank you for using %COMPANYNAME%"

    # can check length first if not sure
    if len(customer_sms) > 135:
        print("Too many chars for custom customer sms.")
        sys.exit()

    # can update reference manually, if `use_random_ref` is set to False
    api.updateReference('37ehd93')

    response = api.rechargePinless(amount=0.5, number="077xxxxxxx", mesg=customer_sms)

    print(response)

    pass

except Exception as ex:
    print(f"There was a problem: {ex}")

