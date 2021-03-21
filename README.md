# [Hot Recharge](https://ssl.hot.co.zw/)
perform hot-recharge services with hot-recharge python library programmatically

- ℹ Not an official hot-recharge python library

## Library installation
```sh
$ pip install hot-recharge
```
or update with
```sh
$ pip install -U hot-recharge
```

## [CHANGELOG](CHANGELOG.md)
please see full [changelog here](CHANGELOG.md)

## Sign Up
- needs a hot recharge co-operate account or `contact hot-recharge for proper account`
- ![sign up](https://raw.githubusercontent.com/DonnC/Hot-Recharge-ZW/master/Docs/images/signup_cooperate.png)

## Authentication keys
- `code` := the email address used on registration
- `pswd` := the password of the account used on registration
- `ref`  := any random string or chars < 50
- these are passed as a dict, `use dict keys as is`
```python
# api credentials headers
credentials = {
    'code': '<your-email>',
    'pswd': '<your-password',
    'ref': '<any-random-text>'
}
```

## Performing requests
- this shows how to do basic get requests for different services
```python
import hotrecharge
import pprint

api = hotrecharge.HotRecharge(headers=credentials)

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
```
-
# Recharge
## Recharge data bundles
- use bundle product code
- an optional customer sms can be send together upon request
- Place holders used include
```
%AMOUNT% 	    $XXX.XX
%COMPANYNAME%	As Defined by Customer on the website www.hot.co.zw
%ACCESSNAME%	Defined by Customer on website – Teller or Trusted User or branch name
%BUNDLE%	    Name of the Data Bundle
```
```python
import hotrecharge
from pprint import pprint

# you can opt to update the reference code manually 
# by setting `use_random_ref` to False
api = hotrecharge.HotRecharge(headers=credentials, use_random_ref=False)

try:

    # option message to send to user
    customer_sms =  " Amount of %AMOUNT% for data %BUNDLE% recharged! " \
                    " %ACCESSNAME%. The best %COMPANYNAME%!"

    # need to update reference manually, if `use_random_ref` is set to False
    api.updateReference('<new-random-string>')

    response = api.dataBundleRecharge(product_code="<bundle-product-code>", number="071xxxxxxx", mesg=customer_sms)

    pprint(response)

except Exception as ex:
    print(f"There was a problem: {ex}")
```

### Recharge pinless
```python
import hotrecharge

api = hotrecharge.HotRecharge(headers=credentials)

try:
    customer_sms = "Recharge of %AMOUNT% successful" \
                   "Initial balance $%INITIALBALANCE%" \
                   "Final Balance $%FINALBALANCE%" \
                   "%COMPANYNAME%"

    response = api.rechargePinless(amount=3.5, number="077xxxxxxx", mesg=customer_sms)

    print(response)

except Exception as ex:
    print(f"There was a problem: {ex}")
```

## Zesa Recharge: new in  `v1.4.x` ✨
custom Message place holders to use and their representation on end user for zesa transactions:
- `%AMOUNT% - $xxx.xx`
- `%KWH% - Unit in Kilowatt Hours(Kwh)`
- `%ACOUNTNAME% - Account holdername of meter number`
- `%METERNUMBER% - meter number`
- `%COMPANYNAME% - as defined by Customer on the website www.hot.co.zw`

## Note on Zesa Recharges
### Requirements 
- A method  for Purchasing ZESA Tokens 
- It is a ZESA requirement that any purchase must be **verified**. As such please ensure that you use the `checkZesaCustomer()` method 
```python

    try:
        customer = api.checkZesaCustomer(meterNumber)

        print(customer)

        # prompt user to confirm their details first before performing a recharge

    except Exception as err:
        print('[ERROR] Error getting zesa customer: ', err)
  ```

- and prompt the customer to confirm the details **before** calling this method (`api.rechargeZesa(...)`). 
- There is a new transaction state specifically for ZESA that is Pending verification indicated by **reply code 4**. Transactions in this state can result in successful transactions after a period of time once ZESA complete transaction.
- You must call Query ZESA method `TBD` periodically until a permanent resolution of the transaction occurs. This polling of a pending transaction should not exceed more that **4 request a minute**. Resending of transactions that have not yet failed can result in the duplication of transaction and lose of funds. 
- Please note ZESA does not allow *refunds* so the cost of any errors cannot be recovered. 


# New in `v1.3.0`✨
- fully implemented method parameters e.g `brandID` and `mesg` for customerSMS on api method calls
### Query transaction
- You can now query a previous transaction by its `agentReference` for reconciliation. 
- It is reccommended to query within the last 30 days of the transaction
```python
import hotrecharge

api = hotrecharge.HotRecharge(headers=credentials)

try:
    response = api.rechargePinless(amount=3.5, number="077xxxxxxx")

    # save agentReference to query for reconciliation
    prevTransactionAgentReference = response.get("agentReference")

    result = api.queryTransactionReference(prevTransactionAgentReference)

    print(response, result)

except Exception as ex:
    print(f"There was a problem: {ex}")
```

## Support 🤿
- A little support can go a long way
- You can help by making `PR` on any changes you would like to contribute to
- `Fork` or `star` this repo, it will help a lot 
