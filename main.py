from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime, date
from typing import Optional
from contextlib import contextmanager

DATABASE_URL = "sqlite:///./expenses.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class ExpenseDB(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker API", version="1.0.0")
app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")


@app.get("/")
async def root():
    return RedirectResponse(url="/frontend/index.html")


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ExpenseCreate(BaseModel):
    amount: float
    category: str
    description: Optional[str] = None


class ExpenseOut(ExpenseCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ExpenseUpdate(BaseModel):
    amount: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None


def get_today_expenses(db):
    today = date.today()
    start = datetime.combine(today, datetime.min.time())
    end = datetime.combine(today, datetime.max.time())
    return db.query(ExpenseDB).filter(ExpenseDB.created_at >= start, ExpenseDB.created_at <= end).all()


@app.get("/")
async def root():
    return RedirectResponse(url="/frontend/index.html")


@app.get("/api/expenses")
def list_today():
    with get_db() as db:
        expenses = get_today_expenses(db)
        return [
            {"id": e.id, "amount": e.amount, "category": e.category, "description": e.description, "created_at": e.created_at.isoformat()}
            for e in expenses
        ]


@app.post("/api/expenses")
def create_expense(expense: ExpenseCreate):
    with get_db() as db:
        db_expense = ExpenseDB(**expense.model_dump())
        db.add(db_expense)
        db.commit()
        db.refresh(db_expense)
        return {"id": db_expense.id, "amount": db_expense.amount, "category": db_expense.category, "description": db_expense.description, "created_at": db_expense.created_at.isoformat()}


@app.put("/api/expenses/{expense_id}")
def update_expense(expense_id: int, expense: ExpenseUpdate):
    with get_db() as db:
        db_expense = db.query(ExpenseDB).filter(ExpenseDB.id == expense_id).first()
        if not db_expense:
            raise HTTPException(status_code=404, detail="Expense not found")
        update_data = expense.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_expense, field, value)
        db.commit()
        db.refresh(db_expense)
        return {"id": db_expense.id, "amount": db_expense.amount, "category": db_expense.category, "description": db_expense.description, "created_at": db_expense.created_at.isoformat()}


@app.delete("/api/expenses/{expense_id}")
def delete_expense(expense_id: int):
    with get_db() as db:
        db_expense = db.query(ExpenseDB).filter(ExpenseDB.id == expense_id).first()
        if not db_expense:
            raise HTTPException(status_code=404, detail="Expense not found")
        db.delete(db_expense)
        db.commit()
        return {"message": "Expense deleted"}


@app.get("/api/expenses/summary")
def get_summary():
    with get_db() as db:
        expenses = get_today_expenses(db)
        total = sum(e.amount for e in expenses)
        by_category: dict[str, float] = {}
        for e in expenses:
            by_category[e.category] = by_category.get(e.category, 0) + e.amount
        return {
            "date": date.today().isoformat(),
            "total": round(total, 2),
            "count": len(expenses),
            "by_category": {k: round(v, 2) for k, v in by_category.items()},
        }
