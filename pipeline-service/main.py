from fastapi import FastAPI, HTTPException
from database import engine, Base, SessionLocal
from services.ingestion import ingest_data
from models.customer import Customer

# Author: Tanuj Kumar  || Tanujk95681@gmail.com
# Project: Backend Developer Technical Assessment
# Description: Flask → FastAPI → PostgreSQL data pipeline

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)


# 🔹 Root API
@app.get("/")
def root():
    return {"message": "Pipeline Service Running"}


# 🔹 Ingestion API
@app.post("/api/ingest")
def ingest():
    print("API HIT")
    count = ingest_data()
    return {"status": "success", "records_processed": count}


# 🔹 Get all customers (with pagination)
@app.get("/api/customers")
def get_customers(page: int = 1, limit: int = 10):
    session = SessionLocal()

    try:
        start = (page - 1) * limit

        customers = session.query(Customer).offset(start).limit(limit).all()
        total = session.query(Customer).count()

        result = []
        for c in customers:
            result.append({
                "customer_id": c.customer_id,
                "first_name": c.first_name,
                "last_name": c.last_name,
                "email": c.email,
                "phone": c.phone,
                "address": c.address,
                "date_of_birth": str(c.date_of_birth),
                "account_balance": float(c.account_balance) if c.account_balance else 0,
                "created_at": str(c.created_at)
            })

        return {
            "data": result,
            "total": total,
            "page": page,
            "limit": limit
        }

    finally:
        session.close()


# 🔹 Get single customer
@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: str):
    session = SessionLocal()

    try:
        customer = session.query(Customer).filter_by(customer_id=customer_id).first()

        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        return {
            "customer_id": customer.customer_id,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "email": customer.email,
            "phone": customer.phone,
            "address": customer.address,
            "date_of_birth": str(customer.date_of_birth),
            "account_balance": float(customer.account_balance) if customer.account_balance else 0,
            "created_at": str(customer.created_at)
        }

    finally:
        session.close()