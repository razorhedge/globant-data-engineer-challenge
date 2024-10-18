from fastapi import FastAPI, UploadFile, File
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Department, Job, Employee, Base  
app = FastAPI()

DATABASE_URL = "sqlite:///./test.db"  
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

@app.post("/upload-employees/")
async def upload_employees(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(pd.compat.StringIO(contents.decode('utf-8')))
    return {"filename": file.filename, "content_type": file.content_type}

