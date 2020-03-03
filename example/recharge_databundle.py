# recharge_databundle.py
# @author:  Donald Chinhuru
# @created: 09 Dec 2019
# @updated: 09 Dec 2019

import hotrecharge
import sys
from pprint import pprint

credentials = {
    'code': '<your-code>',
    'pswd': '<your-password',
    'ref': '<agent-reference>'
}

# to use random code generated references, flag it to True
api = hotrecharge.HotRecharge(headers=credentials, use_random_ref=False)

try:
    # recharge data bundle with a (OPTIONAL) custom Customer SMS, max char should not exceed 135
    # uses places holders as used on hot recharge registration
    customer_sms =  " Amount of %AMOUNT% for data %BUNDLE% recharged! " \
                    " %ACCESSNAME%. The best %COMPANYNAME%!"

    # can check length first if not sure
    if len(customer_sms) > 135:
        print("Too many chars for custom customer sms.")
        sys.exit()

    # need to update reference manually, if `use_random_ref` is set to False
    api.updateReference('383yd3')

    response = api.dataBundleRecharge(product_code="<bundle-product-code>", number="077xxxxxxx", mesg=customer_sms)

    pprint(response)

except Exception as ex:
    print(f"There was a problem: {ex}")

