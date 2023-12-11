from fastapi import FastAPI
from database import database
from models import savemindmapnode
import uvicorn

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/get_data", response_model=list)
async def get_all_data():
    query = savemindmapnode.select()
    results = await database.fetch_all(query)
    return results


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)