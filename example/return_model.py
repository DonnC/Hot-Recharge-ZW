import hotrecharge

# create config class
config = hotrecharge.HRAuthConfig(
    access_code="acc-email",
    access_password="acc-pwd",
    reference="random-ref",  # (optional)
)

# pass config object to api constructor
# flag return_model -> True in order to return model, (Munch object)
api = hotrecharge.HotRecharge(config, return_model=True)

wb_model = api.walletBalance()

# if all goes well, this will return a model (see method DocStrings)
# and we can now access data via model attributes like working with classes
balance = wb_model.WalletBalance

print("Wallet Balance is: $", balance)
