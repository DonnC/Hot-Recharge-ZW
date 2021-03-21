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

