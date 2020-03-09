# get_tests.py
# @author:  Donald Chinhuru
# @created: 09 Dec 2019
# @updated: 09 Dec 2019

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

    # get end user balance
    end_user_bal_resp = api.endUserBalance('077xxxxxxx')

    # get data bundles
    data_bundles_resp = api.getDataBundles()

    print("Wallet Balance: ")
    pprint.pprint(wallet_bal_response)

    print("End User Balance: ")
    pprint.pprint(end_user_bal_resp)

    print("Data Bundles Balance: ")
    pprint.pprint(data_bundles_resp)

except Exception as ex:
    print(f"There was a problem: {ex}")

