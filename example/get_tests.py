# get_tests.py
# @author:  Donald Chinhuru
# @created: 09 Dec 2019
# @updated: Mar 2021

import hotrecharge
import pprint

# TODO:: Add Config module
# change dict values only
credentials = {
    'code': '<your-code>',
    'pswd': '<your-password',
    'ref': '<agent-reference>'
}

# to use random code generated references, flag it to True, True by default, <<reccommended>>
api = hotrecharge.HotRecharge(headers=credentials, use_random_ref=True)

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

