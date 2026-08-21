from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel
import datetime
import bcrypt
import jwt

DATABASE_URL = "postgresql://postgres:Valentine@localhost:5433/Inventory_Management_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

SECRET_KEY = "Inventory12!2@adfkEY78"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Employee(Base):
    __tablename__ = "Employees"

    employee_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    role = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)

Base.metadata.create_all(bind=engine)

# Helper function
def hash_password(password: str) -> str:
   salt = bcrypt.gensalt()
   return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
   return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: datetime.timedelta = None) -> str:
   to_encode = data.copy()
   expire = datetime.datetime.utcnow() + (expires_delta or datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
   to_encode.update({"exp": expire})
   encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
   return encoded_jwt

class EmployeeCreate(BaseModel):
   first_name: str
   last_name: str
   email: str
   phone: str
   role: str
   password: str

class EmployeeLogin(BaseModel):
   email: str
   password: str

class TokenResponse(BaseModel):
   access_token: str
   token_type: str
   employee_id: int
   email: str
   role: str

class UserResponse(BaseModel):
   employee_id: int
   first_name: str
   last_name: str
   email: str
   phone: str
   role: str

   class Config:
      from_attributes = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
       db.close()

app = FastAPI(title="Inventory Management API")

@app.post("/add_employee/", response_model=UserResponse)
def add_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    existing_employee = db.query(Employee).filter(Employee.email == employee.email).first()

    if existing_employee:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pwd = hash_password(employee.password)
    db_employee = Employee(
       first_name=employee.first_name,
       last_name = employee.last_name,
       email = employee.email,
       phone = employee.phone,
       role = employee.role,
       password = hashed_pwd
    )

    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@app.post("/login/", response_model=TokenResponse)
def employee_login(employee_credentials: EmployeeLogin, db: Session = Depends(get_db)):
    db_employee = db.query(Employee).filter(Employee.email == employee_credentials.email).first()

    if not db_employee or not verify_password(employee_credentials.password, db_employee.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalida email or password",
                            headers={"WWW-Authenticate": "Bearer"},)

    token_data = {
       "sub": str(db_employee.employee_id),
       "email": db_employee.email
    }

    access_token = create_access_token(data=token_data)

    return {
       "access_token": access_token,
       "token_type": "bearer",
       "employee_id": db_employee.employee_id,
       "email": db_employee.email,
       "role": db_employee.role
    }

   
