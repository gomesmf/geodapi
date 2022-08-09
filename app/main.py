from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies import dba, pv, credentials_exception
from app.routers import accounts, distances

from accounts.auth import authenticate_account, create_account_id_access_token

app = FastAPI(description="Compute Geodesic Distance Between Address API")

app.include_router(accounts.router)
app.include_router(distances.router)

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    account = authenticate_account(dba, pv, form_data.username, form_data.password)
    if not account:
        raise credentials_exception
    account_id_token = create_account_id_access_token(account.id)
    return {"access_token": account_id_token, "token_type": "bearer"}
