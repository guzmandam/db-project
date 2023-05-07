from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, DateTime
from sqlalchemy.orm import relationship

from datetime import datetime, timedelta

from .database import Base

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    editorial = Column(String)
    pub_year = Column(Integer)
    edition = Column(Integer)
    category_id = Column(Integer, ForeignKey("categories.id"))
    
    categories = relationship("Category", back_populates="books")
    copies = relationship("Copy", back_populates="books")
    
class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    
    books = relationship("Book", back_populates="categories")
    
class Copy(Base):
    __tablename__ = "copies"
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    available = Column(Boolean)
    atention = Column(Boolean)
    
    books = relationship("Book", back_populates="copies")
    loans = relationship("Loan", back_populates="copies")
    
class Loan(Base):
    __tablename__ = "loans"
    
    id = Column(Integer, primary_key=True, index=True)
    copy_id = Column(Integer, ForeignKey("copies.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    loan_date = Column(DateTime, default=datetime.utcnow)
    active = Column(Boolean, default=True)
    return_date = Column(DateTime)
    
    copies = relationship("Copy", back_populates="loans")
    users = relationship("User", back_populates="loans")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)
    password = Column(String)
    active = Column(Boolean)
    register_date = Column(DateTime)
    expiration_date = Column(DateTime)
    
    loans = relationship("Loan", back_populates="users")