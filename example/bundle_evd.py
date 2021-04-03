# @author:  DonnC Lab <https://github.com/DonnC>
# @created: April 2021
# @updated: April 2021

import hotrecharge
from time import sleep
import pprint

# use config helper class
config = hotrecharge.HRAuthConfig(
    access_code='', 
    access_password='',
    reference=''
)

# to use random code generated references, flag it to True, True by default, <<reccommended>>
api = hotrecharge.HotRecharge(config=config)

try:
    # get data bundles
    print('=== get data bundles ===')
    data_bundles_resp = api.getDataBundles()
    print("Data bundles: ")
    pprint.pprint(data_bundles_resp)

    sleep(5)

    print('=== get EVDs ===')
    evds = api.getEVDs()
    print("EVDs: ")
    pprint.pprint(evds)

    sleep(5)

    print('=== recharge EVD ===')
    recharge_evd = api.rechargeEVD(brand_id=24, pin_value=0.5, number='0712359809')
    print('Recharge EVD: ')
    pprint.pprint(recharge_evd)

    sleep(5)

    print('=== recharge bundle ===')
    recharge_bndl = api.dataBundleRecharge(product_code='SMSD5', number='0778060126')
    print('Recharge bundle: ')
    pprint.pprint(recharge_bndl)

except Exception as ex:
    print(f"There was a problem: {ex}")

