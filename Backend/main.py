from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String, Numeric, TIMESTAMP, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel
import datetime
import bcrypt
import jwt
from typing import List

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

class Customer(Base):
   __tablename__ = "Customers"

   customer_id = Column(Integer, primary_key=True, index=True)
   first_name = Column(String(50), nullable=False)
   last_name = Column(String(50), nullable=False)
   email = Column(String(100), unique=True, nullable=False)
   phone = Column(String(20), unique=True, nullable=False)

Base.metadata.create_all(bind=engine)

class Product(Base):
   __tablename__ = "Products"

   product_id = Column(Integer, primary_key=True, index=True)
   product_name = Column(String(100), unique=True, nullable=False)
   description = Column(String(255), nullable=False)
   cost_price = Column(Numeric(10, 2), nullable=False)
   selling_price = Column(Numeric(10, 2), nullable=False)
   stock_quantity = Column(Integer, default=0, nullable=False)
   reorder_level = Column(Integer, default=5, nullable=False)

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

class ProductCreate(BaseModel):
   product_name: str
   description: str
   cost_price: float
   selling_price: float
   stock_quantity: int
   reorder_level: int

class ProductResponse(BaseModel):
   product_id: int
   product_name: str
   description: str
   cost_price: float
   selling_price: float
   stock_quantity: int
   reorder_level: int

   class Config: 
      from_attributes = True

class CustomerCreate(BaseModel):
   first_name: str
   last_name: str
   email: str
   phone: str

class CustomerResponse(BaseModel):
   customer_id: int
   first_name: str
   last_name: str
   email: str
   phone: str

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
                            detail="Invalid email or password",
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

@app.post("/add_product/", response_model=ProductResponse)
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
   existing_product = db.query(Product).filter(Product.product_name == product.product_name).first()

   if existing_product:
      raise HTTPException(status_code=400, detail="Product with this name already exists")

   db_product = Product(
      product_name=product.product_name,
      description = product.description,
      cost_price = product.cost_price,
      selling_price = product.selling_price,
      stock_quantity = product.stock_quantity,
      reorder_level = product.reorder_level
   )

   db.add(db_product)
   db.commit()
   db.refresh(db_product)
   return db_product

@app.post("/add_customer/", response_model=CustomerResponse)
def add_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
   existing_customer = db.query(Customer).filter(Customer.email == customer.email).first()

   if existing_customer:
      raise HTTPException(status_code=400, detail="Email already registered")

   db_customer = Customer(
      first_name = customer.first_name,
      last_name = customer.last_name,
      email = customer.email,
      phone = customer.phone
   )

   db.add(db_customer)
   db.commit()
   db.refresh(db_customer)
   return db_customer

@app.get("/products/", response_model=List[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
   products = db.query(Product.all())
   return products