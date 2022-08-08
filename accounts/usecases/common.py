from accounts.entities import MIN_LEN_PASSWORD, MIN_LEN_USERNAME

ERRMSG_INVALID_ACCTYPE = "Invalid account type"
ERRMSG_INVALID_PASSWORD = f"Invalid password: must have at least {MIN_LEN_PASSWORD} characters"
ERRMSG_INVALID_NAME = "Invalid name: cannot be empty"
ERRMSG_INVALID_USERNAME = f"Invalid username: must have at least {MIN_LEN_USERNAME} characters"
ERRMSG_INVALID_EMAIL = "Invalid email"
ERRMSG_EMAIL_EXISTS = "Email already used by another account"
ERRMSG_USERNAME_EXISTS = "Username already used by another account"
ERRMSG_CANNOT_CREATE_ACCOUNT = "Account cannot be created in the database"
ERRMSG_CANNOT_UPDATE_ACCOUNT = "Account cannot be updated in the database"
ERRMSG_TWO_PASSWD_MUST_MATCH = "Passwords must be equal"
ERRMSG_ACCOUNT_NOT_FOUND = "Account does not exists"
