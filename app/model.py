from .db import db  # Your SQLAlchemy instance from db.py
from datetime import datetime

class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))

    category = db.relationship("Category", back_populates="expenses")


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    expenses = db.relationship("Expense", back_populates="category", cascade="all, delete-orphan")
