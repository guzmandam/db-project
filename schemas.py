from pydantic import BaseModel
from datetime import datetime, timedelta

class CopyBase(BaseModel):
    available: bool
    atention: bool
    book_id: int

class CopyUpdate(BaseModel):
    available: bool
    atention: bool

class CopyCreate(CopyBase):
    pass

class Copy(CopyBase):
    id: int
    
    class Config:
        orm_mode = True

class BookBase(BaseModel):
    title: str
    author: str
    editorial: str
    pub_year: int
    edition: int
    category_id: int

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    copies: list[Copy] = []

    class Config:
        orm_mode = True
        
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    books: list[Book] = []

    class Config:
        orm_mode = True

class LoanBase(BaseModel):
    loan_date: datetime = datetime.now()
    return_date: datetime = datetime.now() + timedelta(days=8)
    active: bool = True
    copy_id: int
    user_id: int

class LoanUpdate(BaseModel):
    loan_date: datetime
    return_date: datetime
    
class LoanCreate(LoanBase):
    pass

class Loan(LoanBase):
    id: int

    class Config:
        orm_mode = True
        json_encoders = {datetime: lambda dt: dt.isoformat() + 'Z'}

class UserBase(BaseModel):
    name: str
    last_name: str
    email: str
    phone: str
    active: bool
    register_date: datetime = datetime.now()
    expiration_date: datetime = datetime.now() + timedelta(days=120)

class UserUpdate(UserBase):
    pass

class UserCreate(UserBase):
    password: str
    pass

class User(UserBase):
    id: int
    loans: list[Loan] = []

    class Config:
        orm_mode = True
        json_encoders = {datetime: lambda dt: dt.isoformat() + 'Z'}