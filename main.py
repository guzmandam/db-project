from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Proyecto Bases de Datos - Biblioteca",
        version="0.0.1",
        description="Actuaria - FES Acatlán",
        routes=app.routes,
    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
@app.post("/users/", response_model=schemas.User, status_code=201, tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email) 
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User], status_code=200, tags=["Users"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.patch("/users/{user_id}", response_model=schemas.User, status_code=200, tags=["Users"])
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user(db=db, user_id=user_id, user=user)

@app.delete("/users/{user_id}", status_code=200, tags=["Users"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db, user_id=user_id)
    db.commit()
    return {"message": f"User {user_id} deleted"}

@app.get("/users/{user_id}", response_model=schemas.User, status_code=200, tags=["Users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/users/email/{email}", response_model=schemas.User, status_code=200, tags=["Users"])
def read_user_email(email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/books/", status_code=201, tags=["Books"])
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = crud.create_book(db=db, book=book)
    return db_book

@app.delete("/books/{book_id}", response_model=schemas.Book, status_code=200, tags=["Books"])
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_id(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    crud.delete_book(db, book_id=book_id)
    return {"message": f"Book {book_id} deleted"}

@app.get("/books/", response_model=list[schemas.Book], status_code=200, tags=["Books"])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books

@app.get("/books/{book_id}", response_model=schemas.Book, status_code=200, tags=["Books"])
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_id(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.get("/books/category/{category_id}", response_model=list[schemas.Book], status_code=200, tags=["Books"])
def read_books_category(category_id: int, db: Session = Depends(get_db)):
    db_books = crud.get_books_by_category(db, category_id=category_id)
    if db_books is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_books

@app.get("/books/author/{author}", response_model=list[schemas.Book], status_code=200, tags=["Books"])
def read_books_title(author: str, db: Session = Depends(get_db)):
    db_books = crud.get_books_by_author(db, author=author)
    if db_books is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_books

@app.get("/books/editorial/{editorial}", response_model=list[schemas.Book], status_code=200, tags=["Books"])
def read_books_editorial(editorial: str, db: Session = Depends(get_db)):
    db_books = crud.get_books_by_editorial(db, editorial=editorial)
    if db_books is None:
        raise HTTPException(status_code=404, detail="Editorial not found")
    return db_books

@app.post("/categories/", response_model=schemas.Category, status_code=201, tags=["Categories"])
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = crud.create_category(db=db, category=category)
    return db_category

@app.delete("/categories/{category_id}", status_code=200, tags=["Categories"])
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    crud.delete_category(db, category_id=category_id)
    return {"message": "Category deleted"}

@app.get("/categories/", response_model=list[schemas.Category], status_code=200, tags=["Categories"])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud.get_categories(db, skip=skip, limit=limit)
    return categories

@app.get("/categories/{category_id}", response_model=schemas.Category, status_code=200, tags=["Categories"])
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@app.get("/categories/name/{name}", response_model=schemas.Category, status_code=200, tags=["Categories"])
def read_category_name(name: str, db: Session = Depends(get_db)):
    db_category = crud.get_category_by_name(db, name=name)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@app.post("/copies/", response_model=schemas.Copy, status_code=201, tags=["Copies"])
def create_copy(copy: schemas.CopyCreate, db: Session = Depends(get_db)):
    db_copy = crud.create_copy(db=db, copy=copy)
    return db_copy

@app.delete("/copies/{copy_id}", status_code=200, tags=["Copies"])
def delete_copy(copy_id: int, db: Session = Depends(get_db)):
    db_copy = crud.get_copy(db, copy_id=copy_id)
    if db_copy is None:
        raise HTTPException(status_code=404, detail="Copy not found")
    crud.delete_copy(db, copy_id=copy_id)
    return {"message": f"Copy {copy_id} deleted"}

@app.get("/copies/", response_model=list[schemas.Copy], status_code=200, tags=["Copies"])
def read_copies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    copies = crud.get_copies(db, skip=skip, limit=limit)
    return copies

@app.get("/copies/{copy_id}", response_model=schemas.Copy, status_code=200, tags=["Copies"])
def read_copy(copy_id: int, db: Session = Depends(get_db)):
    db_copy = crud.get_copy(db, copy_id=copy_id)
    if db_copy is None:
        raise HTTPException(status_code=404, detail="Copy not found")
    return db_copy

@app.get("/copies/book/{book_id}", response_model=list[schemas.Copy], status_code=200, tags=["Copies"])
def read_copies_book(book_id: int, db: Session = Depends(get_db)):
    db_copies = crud.get_copies_by_book(db, book_id=book_id)
    if db_copies is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_copies

@app.get("/copies/book/available/{book_id}", response_model=list[schemas.Copy], status_code=200, tags=["Copies"])
def read_copies_book_available(book_id: int, db: Session = Depends(get_db)):
    db_copies = crud.get_copies_available_by_book(db, book_id=book_id)
    if db_copies is None:
        raise HTTPException(status_code=404, detail="No copies available")
    return db_copies

@app.post("/loans/", response_model=schemas.Loan, status_code=201, tags=["Loans"])
def create_loan(loan: schemas.LoanCreate, db: Session = Depends(get_db)):
    if len(crud.get_active_loans_by_user(db, user_id=loan.user_id)) >= 3:
        raise HTTPException(status_code=400, detail="User has reached the maximum number of loans")
    loan_copy = crud.get_copy(db, copy_id=loan.copy_id)
    if loan_copy.available == False:
        raise HTTPException(status_code=400, detail="Copy not available")
    if loan.return_date <= loan.loan_date:
        raise HTTPException(status_code=400, detail="Return date must be after loan date")
    db_loan = crud.create_loan(db=db, loan=loan)
    crud.update_copy_not_available(db, copy_id=loan.copy_id)
    return db_loan

@app.delete("/loans/{loan_id}", status_code=200, tags=["Loans"])
def delete_loan(loan_id: int, db: Session = Depends(get_db)):
    db_loan = crud.get_loan(db, loan_id=loan_id)
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    crud.update_copy_not_available(db, copy_id=db_loan.copy_id)
    crud.delete_loan(db, loan_id=loan_id)
    
    return {"message": "Loan deleted"}

@app.patch("/loans/{loan_id}", response_model=schemas.Loan, status_code=200, tags=["Loans"])
def update_loan(loan_id: int, loan: schemas.LoanUpdate, db: Session = Depends(get_db)):
    db_loan = crud.get_loan(db, loan_id=loan_id)
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    if loan.return_date <= loan.loan_date:
        raise HTTPException(status_code=400, detail="Return date must be after loan date")
    crud.update_loan(db, loan_id=loan_id, loan=loan)
    
    return crud.get_loan(db, loan_id=loan_id)

@app.get("/loans/", response_model=list[schemas.Loan], tags=["Loans"])
def read_loans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    loans = crud.get_loans(db, skip=skip, limit=limit)
    return loans

@app.get("/loans/{loan_id}", response_model=schemas.Loan, tags=["Loans"])
def read_loan(loan_id: int, db: Session = Depends(get_db)):
    db_loan = crud.get_loan(db, loan_id=loan_id)
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    return db_loan

@app.get("/loans/user/{user_id}", response_model=list[schemas.Loan], status_code=200, tags=["Loans"])
def read_loans_user(user_id: int, db: Session = Depends(get_db)):
    db_loans = crud.get_loans_by_user(db, user_id=user_id)
    if db_loans is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_loans

@app.get("/loans/copy/{copy_id}", response_model=list[schemas.Loan], status_code=200, tags=["Loans"])
def read_loans_copy(copy_id: int, db: Session = Depends(get_db)):
    db_loans = crud.get_loans_by_copy(db, copy_id=copy_id)
    if db_loans is None:
        raise HTTPException(status_code=404, detail="Copy not found")
    return db_loans