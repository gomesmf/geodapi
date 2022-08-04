from fastapi import FastAPI

from fake import get_dba

dba = get_dba()

app = FastAPI(description="Delivery Guy API")

@app.get("/accounts")
def get_accounts():
    return dba.data

@app.post("/accounts")
def create_account():
    return {"account_id": 1}
