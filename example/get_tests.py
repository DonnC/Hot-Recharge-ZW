# get_tests.py
# @author:  Donald Chinhuru
# @created: 09 Dec 2019
# @updated: Mar 2021

import hotrecharge
import pprint

# use config helper class
config = hotrecharge.HRAuthConfig(
    access_code='', 
    access_password='',
    reference=''
)

api = hotrecharge.HotRecharge(config=config)

try:
    # get wallet balance
    wallet_bal_response = api.walletBalance()

    # get data bundles
    data_bundles_resp = api.getDataBundles()

    print("Wallet Balance: ")
    pprint.pprint(wallet_bal_response)

    print("Data Bundles Balance: ")
    pprint.pprint(data_bundles_resp)

except Exception as ex:
    print(f"There was a problem: {ex}")

