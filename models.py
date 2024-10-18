from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Department(Base):
    __tablename__ = 'departments'
    
    id = Column(Integer, primary_key=True, index=True)
    department = Column(String, nullable=False)
    
    employees = relationship("Employee", back_populates="department")

class Job(Base):
    __tablename__ = 'jobs'
    
    id = Column(Integer, primary_key=True, index=True)
    job = Column(String, nullable=False)
    
    employees = relationship("Employee", back_populates="job")

class Employee(Base):
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    hire_datetime = Column(DateTime, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    
    department = relationship("Department", back_populates="employees")
    job = relationship("Job", back_populates="employees")