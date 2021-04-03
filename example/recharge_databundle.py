# recharge_databundle.py
# @author:  Donald Chinhuru
# @created: 09 Dec 2019
# @updated: 09 Mar 2020

import hotrecharge
from pprint import pprint

# use config helper class
config = hotrecharge.HRAuthConfig(
    access_code='', 
    access_password='',
    reference=''
)

api = hotrecharge.HotRecharge(config=config)

try:
    # to see other product-codes and more info, use api.getDataBundles()
    response = api.dataBundleRecharge(product_code="DWB15", number="077xxxxxxx")

    pprint(response)

except Exception as ex:
    print(f"There was a problem: {ex}")

