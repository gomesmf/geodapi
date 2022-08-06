from accounts.entities import AccountType, MIN_LEN_PASSWORD

VLD_ACCTYPE = AccountType.DELIVERYGUY.value
VLD_NAME = "matheus"
VLD_EMAIL = "matheus@email.com"
VLD_PASSWORD = "p"*MIN_LEN_PASSWORD
INVLD_ACCTYPE = "wrongtype"
INVLD_NAME = ""
INVLD_EMAIL = "matheus"
INVLD_PASSWORD = "1"*(MIN_LEN_PASSWORD-1)
