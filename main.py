from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Department, Job, Employee, Base  
from io import StringIO
app = FastAPI()

DATABASE_URL = "sqlite:///./test.db"  
engine = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

def load_departments(df: pd.DataFrame, db: Session):
    df.fillna({'department': 'Unknown'}, inplace=True)
    for _, row in df.iterrows():
        department = Department(id=row[0], department=row[1])  # Usar índices
        db.add(department)
    db.commit()

def load_jobs(df: pd.DataFrame, db: Session):
    df.fillna({'job': 'Unknown'}, inplace=True)
    for _, row in df.iterrows():
        job = Job(id=row[0], job=row[1])  # Usar índices
        db.add(job)
    db.commit()

def load_employees(df: pd.DataFrame, db: Session):
    df.fillna({
        2: pd.NaT,  # Rellenar con 'NaT' para datetime
        3: None,    # Rellenar NaN en 'department_id' con None
        4: None     # Rellenar NaN en 'job_id' con None
    }, inplace=True)
    for _, row in df.iterrows():
        employee = Employee(
            id=row[0],
            name=row[1],
            hire_datetime=pd.to_datetime(row[2]),
            department_id=row[3],
            job_id=row[4]
        )
        db.add(employee)
    db.commit()

@app.post("/upload-data/")
async def upload_data(department_file: UploadFile = File(...), 
                      job_file: UploadFile = File(...), 
                      employee_file: UploadFile = File(...)):
    contents_department = await department_file.read()
    contents_job = await job_file.read()
    contents_employee = await employee_file.read()

    df_departments = pd.read_csv(StringIO(contents_department.decode('utf-8')), header=None)
    df_jobs = pd.read_csv(StringIO(contents_job.decode('utf-8')), header=None)
    df_employees = pd.read_csv(StringIO(contents_employee.decode('utf-8')), header=None)

    db = Session()

    db.query(Department).delete()
    db.query(Job).delete()
    db.query(Employee).delete()  # Limpia la tabla de departamentos
    db.commit()

    try:
        load_departments(df_departments, db)
        load_jobs(df_jobs, db)
        load_employees(df_employees, db)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

    return {"message": "Data uploaded successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)