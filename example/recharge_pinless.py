# recharge_pinless.py
# @author:  Donald Chinhuru
# @created: 09 Dec 2019
# @updated: 09 Mar 2020

import hotrecharge

# use config helper class
config = hotrecharge.HRAuthConfig(
    access_code='', 
    access_password='',
    reference=''
)

api = hotrecharge.HotRecharge(config=config)

try:
    response = api.rechargePinless(amount=1.50, number="077xxxxxxx")
    print(response)

except Exception as ex:
    print(f"[ERROR] There was a problem: {ex}")

