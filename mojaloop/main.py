from fastapi import FastAPI
import httpx
import uuid

app = FastAPI()

accounts = {
    "alice": {"balance": 500000},
    "bob": {"balance": 100000},
}

@app.get("/accounts")
def get_accounts():
    return accounts

@app.post("/transfers")
async def transfer(data: dict):
    payer = accounts[data["payer_id"]]
    payee = accounts[data["payee_id"]]

    if payer["balance"] < data["amount"]:
        return {"status": "REJECTED"}

    payer["balance"] -= data["amount"]
    payee["balance"] += data["amount"]

    tx = {
        "transactionId": str(uuid.uuid4()),
        "amount": data["amount"],
        "status": "SUCCESS"
    }

    async with httpx.AsyncClient() as client:
        await client.post("http://fintrax:8001/ingest", json=tx)

    return tx