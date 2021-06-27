## [3.2.0] - Jun 2021
* added few more api custom exceptions
* minor fixes

## [3.1.0] - Jun 2021
* fixed dependency not found issue

## [3.0.0] - Jun 2021
* Added get zesa wallet balance
* Added query zesa transaction
* Improved documentation
* **NEW** - can now opt to return a Munch object for easy access of attributes
* **NEW** - api now raises custom api exceptions

## [2.1.0] - Apr 2021
* fixed name error issue on `.rechargeZesa(..)` method

## [2.0.0] - Apr 2021
* **BREAKING CHANGE** - constructor now takes a config class arguement for credentials instead of dict of predefined keys 
```python
import hotrecharge

# create config class
config = hotrecharge.HRAuthConfig(
    access_code='acc-email', 
    access_password='acc-pwd',
    reference='random-ref'
)

# pass config object to api constructor
api = hotrecharge.HotRecharge(config)
```
* Added recharge EVD `electronic vouchers`
* Added query evds to get all available EVDs
* Can now perform data bundle recharge

## [1.4.0] - Mar 2021
* Can now perform zesa recharge operations `api.zesaRecharge(..)`
* Can check zesa customer details from meter number `api.checkZesaCustomer(..)`
* removed `endUserBalance` method
* removed `requests` library on requirements
  
## [1.3.0] - 12 Feb 2021.
* you can now, finally, be able to include `brandID` and CustomerSMS (`mesg`) when making `.rechargePinless(...)` requests
 
* you can now, finally, be able to include `amount` and CustomerSMS (`mesg`) when making `.dataBundleRecharge(...)` requests

* `NEW` You can now query a previous transaction by its `agentReference` for reconciliation using `.queryTransactionReference(agentRefrence)`
* updated project description
* improved api documentation

## [1.2.0] - 9 Mar 2020.
* code refactor
* updated examples and readme

## [1.1.0] - 3 Mar 2020.
* Update readme
* set `random_ref` to `True` by default to automatically update request reference

## [1.0.0] - 9 Dec 2019.
* Initial release.

