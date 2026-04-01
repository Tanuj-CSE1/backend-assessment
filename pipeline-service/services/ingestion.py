import requests
from database import SessionLocal
from models.customer import Customer

FLASK_URL = "http://mock-server:5000/api/customers"

def ingest_data():
    session = SessionLocal()
    page = 1
    limit = 5
    total_processed = 0

    try:
        while True:
            print(f"Fetching page {page}")

            response = requests.get(f"{FLASK_URL}?page={page}&limit={limit}", timeout=5)

            if response.status_code != 200:
                print("Flask API failed")
                break

            json_data = response.json()
            data = json_data.get("data", [])

            # ✅ BREAK CONDITION
            if not data:
                print("No more data, breaking loop")
                break

            for item in data:
                existing = session.query(Customer).filter_by(customer_id=item["customer_id"]).first()

                if existing:
                    existing.first_name = item["first_name"]
                    existing.last_name = item["last_name"]
                    existing.email = item["email"]
                    existing.phone = item["phone"]
                    existing.address = item["address"]
                    existing.date_of_birth = item["date_of_birth"]
                    existing.account_balance = item["account_balance"]
                    existing.created_at = item["created_at"]
                else:
                    session.add(Customer(**item))

                total_processed += 1

            session.commit()

            page += 1

            # 🔥 HARD STOP SAFETY
            if page > 20:
                print("Safety break")
                break

    except Exception as e:
        print("ERROR:", e)

    finally:
        session.close()

    return total_processed