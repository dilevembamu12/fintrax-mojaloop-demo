from fastapi import FastAPI

app = FastAPI()

transactions = []

@app.post("/ingest")
def ingest(tx: dict):
    tx["certified"] = True
    tx["royalty"] = tx["amount"] * 0.005
    transactions.append(tx)
    return tx

@app.get("/transactions")
def get_all():
    return transactions