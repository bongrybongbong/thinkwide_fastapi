from sqlalchemy import create_engine, Column, Integer, String, Boolean, Sequence
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
import databases, sqlalchemy
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean, create_engine

Base = declarative_base()


DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4'
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=create_engine)

class saveminmapnode(Base):
    __tablename__ = "saveminmapnode"

    id = Column(Integer, primary_key=True, autoincrement=True)
    Node_Text  = Column(String(100))
    gpt_result = Column(String(5000)) #결과로 추정한 길이 


