from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies import dba, pv, credentials_exception
from app.routers import accounts, distances

from accounts.auth import authenticate_account, create_account_id_access_token

description = [
    "Geodesic Distance API",
    "1. Create account (POST /accounts) and login (button 'Authorize')",
    "2. Compute geodesic distance between two addresses (POST /distances)",
    "3. Get historical queries (GET /distances)"
]

app = FastAPI(description="\n".join(description))

app.include_router(accounts.router)
app.include_router(distances.router)

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    account = authenticate_account(dba, pv, form_data.username, form_data.password)
    if not account:
        raise credentials_exception
    account_id_token = create_account_id_access_token(account.id)
    return {"access_token": account_id_token, "token_type": "bearer"}
