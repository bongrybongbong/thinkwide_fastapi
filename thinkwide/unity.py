
from fastapi import FastAPI
from pydantic import BaseModel
import databases, sqlalchemy
import uvicorn
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

# 데이터베이스 설정
DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4' # 여기에 실제 데이터베이스 연결 문자열을 입력해주세요.
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# 테이블 설정
minmapnode_table = sqlalchemy.Table(
    "saveminmapnode",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("Node_Text", sqlalchemy.String),
    sqlalchemy.Column("Node_type", sqlalchemy.Integer),
    sqlalchemy.Column("aiData", sqlalchemy.String),
    sqlalchemy.Column("isSelected", sqlalchemy.Boolean),
    sqlalchemy.Column("Children", sqlalchemy.String),
)

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/get_data", response_model=list)
async def get_all_data():
    query = minmapnode_table.select()
    results = await database.fetch_all(query)
    return results




if __name__ == "__main__":
    # from models import Base
    # Base.metadata.create_all(bind=engine)

    uvicorn.run(app, host="0.0.0.0", port=8000)

# uvicorn app:app --reload --host=0.0.0.0 --port 5000