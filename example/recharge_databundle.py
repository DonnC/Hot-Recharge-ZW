# recharge_databundle.py
# @author:  Donald Chinhuru
# @created: 09 Dec 2019
# @updated: 09 Mar 2020

import hotrecharge
from pprint import pprint

credentials = {
    'code': '<your-code>',
    'pswd': '<your-password',
    'ref': '<agent-reference>'
}

api = hotrecharge.HotRecharge(headers=credentials)

try:
    # to see other product-codes and more info, use api.getDataBundles()
    response = api.dataBundleRecharge(product_code="DWB15", number="077xxxxxxx")

    pprint(response)

except Exception as ex:
    print(f"There was a problem: {ex}")

