from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from . import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    register_date = datetime.now()
    expiration_date = register_date + timedelta(days=30)
    db_user = models.User(name=user.name, last_name=user.last_name, email=user.email, phone=user.phone, active=user.active, register_date=register_date, expiration_date=expiration_date)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_user.name = user.name
    db_user.last_name = user.last_name
    db_user.email = user.email
    db_user.phone = user.phone
    db_user.active = user.active
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(title=book.title, author=book.author, editorial=book.editorial, pub_year=book.pub_year, edition=book.edition, category_id=book.category_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    db.query(models.Book).filter(models.Book.id == book_id).delete()
    db.commit()

def get_books_by_category(db: Session, category_id: int):
    return db.query(models.Book).filter(models.Book.category_id == category_id).all()

def get_book_by_id(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()

def get_books_by_author(db: Session, author: str):
    return db.query(models.Book).filter(models.Book.author == author).all()

def get_books_by_editorial(db: Session, editorial: str):
    return db.query(models.Book).filter(models.Book.editorial == editorial).all()

def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    db.query(models.Category).filter(models.Category.id == category_id).delete()
    db.commit()
    
def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()

def get_category_by_name(db: Session, name: str):
    return db.query(models.Category).filter(models.Category.name == name).first()

def create_copy(db: Session, copy: schemas.CopyCreate):
    db_copy = models.Copy(available=copy.available, atention=copy.atention, book_id=copy.book_id)
    db.add(db_copy)
    db.commit()
    db.refresh(db_copy)
    return db_copy

def delete_copy(db: Session, copy_id: int):
    db.query(models.Copy).filter(models.Copy.id == copy_id).delete()
    db.commit()

def update_copy_not_available(db: Session, copy_id: int):
    db_copy = db.query(models.Copy).filter(models.Copy.id == copy_id).first()
    db_copy.available = False
    db.commit()
    db.refresh(db_copy)
    return db_copy

def get_copy(db: Session, copy_id: int):
    return db.query(models.Copy).filter(models.Copy.id == copy_id).first()

def get_copies_by_book(db: Session, book_id: int):
    return db.query(models.Copy).filter(models.Copy.book_id == book_id).all()

def get_copies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Copy).offset(skip).limit(limit).all()

def get_copies_available_by_book(db: Session, book_id: int):
    return db.query(models.Copy).filter(models.Copy.book_id == book_id, models.Copy.available == True, models.Copy.atention == False).all()

def create_loan(db: Session, loan: schemas.LoanCreate):
    db_loan = models.Loan(loan_date=loan.loan_date, return_date=loan.return_date, user_id=loan.user_id, copy_id=loan.copy_id)
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan

def update_loan(db: Session, loan_id: int, loan: schemas.LoanUpdate):
    db_loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    db_loan.loan_date = loan.loan_date
    db_loan.return_date = loan.return_date
    db.commit()
    db.refresh(db_loan)
    return db_loan

def update_loan_status(db: Session, loan_id: int):
    db_loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    if db_loan.active == False:
        db_loan.active = True
    else:
        db_loan.active = False
    db.commit()
    db.refresh(db_loan)
    return db_loan

def delete_loan(db: Session, loan_id: int):
    db.query(models.Loan).filter(models.Loan.id == loan_id).delete()
    db.commit()
    
def get_loan(db: Session, loan_id: int):
    return db.query(models.Loan).filter(models.Loan.id == loan_id).first()

def get_loans(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Loan).offset(skip).limit(limit).all()

def get_loans_by_user(db: Session, user_id: int):
    return db.query(models.Loan).filter(models.Loan.user_id == user_id).all()

def get_active_loans_by_user(db: Session, user_id: int):
    return db.query(models.Loan).filter(models.Loan.user_id == user_id, models.Loan.active == True).all()


def get_loans_by_copy(db: Session, copy_id: int):
    return db.query(models.Loan).filter(models.Loan.copy_id == copy_id).all()