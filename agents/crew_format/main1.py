from fastapi import FastAPI
from main import run

app = FastAPI()
print("Running Working")
@app.post("/run/")
async def run(inputs: dict):
    result = run(inputs)
    print(result)
    return {"result": result}