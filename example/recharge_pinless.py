# recharge_pinless.py
# @author:  Donald Chinhuru
# @created: 09 Dec 2019
# @updated: 09 Mar 2020

import hotrecharge

# change values only, keep the dict keys
# TODO Add Config module
credentials = {
    'code': '<your-code>',
    'pswd': '<your-password',
    'ref': '<agent-reference>'
}

api = hotrecharge.HotRecharge(headers=credentials)

try:
    response = api.rechargePinless(amount=1.50, number="077xxxxxxx")
    print(response)

except Exception as ex:
    print(f"[ERROR] There was a problem: {ex}")

