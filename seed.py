"""
Seed script — populates MongoDB with initial data for Belagavi Smart City platform.
Run once: python seed.py
"""
from utils.db import get_db
from utils.auth import hash_password
from utils.helpers import BELAGAVI_WARDS, COMPLAINT_CATEGORIES, DEPARTMENTS, generate_complaint_id
from datetime import datetime, timedelta
import random

db = get_db()

def clear_collections():
    for col in ["citizens", "officers", "complaints", "alerts", "service_requests", "audit_logs"]:
        db[col].drop()
    print("✅ Collections cleared.")

def seed_officers():
    officers = [
        {"name": "Suresh Patil", "email": "suresh.patil@bmc.gov.in", "employee_id": "EMP-001",
         "department": "Administration", "role": "super_admin", "password": "admin@123"},
        {"name": "Kavitha Nair", "email": "kavitha.nair@bmc.gov.in", "employee_id": "EMP-002",
         "department": "Roads & Infrastructure", "role": "dept_head", "password": "dept@123"},
        {"name": "Ramesh Kulkarni", "email": "ramesh.k@bmc.gov.in", "employee_id": "EMP-003",
         "department": "Water Supply", "role": "dept_head", "password": "dept@123"},
        {"name": "Priya Desai", "email": "priya.d@bmc.gov.in", "employee_id": "EMP-004",
         "department": "Sanitation & Garbage", "role": "field_officer", "password": "field@123"},
        {"name": "Anil Joshi", "email": "anil.j@bmc.gov.in", "employee_id": "EMP-005",
         "department": "Power Supply", "role": "field_officer", "password": "field@123"},
    ]
    for o in officers:
        db.officers.insert_one({
            "name": o["name"], "email": o["email"], "employee_id": o["employee_id"],
            "department": o["department"], "role": o["role"],
            "password_hash": hash_password(o["password"]),
            "is_active": True, "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()
        })
    print(f"✅ {len(officers)} officers seeded.")

def seed_citizens():
    citizens_data = [
        {"first_name": "Rajesh", "last_name": "Kumar", "email": "rajesh@gmail.com",
         "phone": "9876543210", "ward": "Ward 12 - Gandhi Nagar", "password": "citizen@123"},
        {"first_name": "Meera", "last_name": "Sharma", "email": "meera@gmail.com",
         "phone": "9876543211", "ward": "Ward 1 - Camp", "password": "citizen@123"},
        {"first_name": "Vikram", "last_name": "Bhat", "email": "vikram@gmail.com",
         "phone": "9876543212", "ward": "Ward 4 - Tilakwadi", "password": "citizen@123"},
    ]
    for c in citizens_data:
        db.citizens.insert_one({
            "first_name": c["first_name"], "last_name": c["last_name"],
            "email": c["email"], "phone": c["phone"], "ward": c["ward"],
            "password_hash": hash_password(c["password"]),
            "is_active": True, "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()
        })
    print(f"✅ {len(citizens_data)} citizens seeded.")

def seed_complaints():
    statuses = ["pending", "in_progress", "resolved", "escalated"]
    priorities = ["low", "medium", "high", "emergency"]
    categories = list(COMPLAINT_CATEGORIES.keys())
    sample_citizens = list(db.citizens.find())
    complaints = []
    for i in range(25):
        cat = random.choice(categories)
        sub_cat = random.choice(COMPLAINT_CATEGORIES[cat])
        citizen = random.choice(sample_citizens) if sample_citizens else {"_id": "anon", "first_name": "Citizen", "last_name": f"{i}"}
        status = random.choice(statuses)
        created = datetime.utcnow() - timedelta(days=random.randint(0, 30))
        complaints.append({
            "complaint_id": generate_complaint_id(),
            "citizen_id": str(citizen["_id"]),
            "citizen_name": f"{citizen.get('first_name','')} {citizen.get('last_name','')}",
            "category": cat, "sub_category": sub_cat,
            "title": f"{sub_cat} issue at {random.choice(BELAGAVI_WARDS[:10])}",
            "description": f"There is a {sub_cat.lower()} problem that needs immediate attention near the main road.",
            "priority": random.choice(priorities),
            "ward": random.choice(BELAGAVI_WARDS[:20]),
            "location_text": f"Near {random.choice(['market', 'school', 'hospital', 'park', 'junction'])}",
            "media_urls": [],
            "status": status,
            "assigned_to": "EMP-002" if status != "pending" else None,
            "assigned_dept": random.choice(DEPARTMENTS) if status != "pending" else None,
            "timeline": [{"status": "pending", "note": "Filed by citizen.", "updated_by": "system", "timestamp": created}],
            "created_at": created, "updated_at": datetime.utcnow()
        })
    db.complaints.insert_many(complaints)
    print(f"✅ {len(complaints)} complaints seeded.")

def seed_alerts():
    alerts = [
        {"title": "Flood Warning", "description": "Heavy rainfall expected in low-lying areas of Camp and Shahpur wards. Citizens advised to stay indoors.", "alert_type": "emergency", "wards": []},
        {"title": "Road Work on MG Road", "description": "Construction work underway on MG Road from Monday to Friday 9AM–5PM. Expect delays.", "alert_type": "warning", "wards": ["Ward 1 - Camp", "Ward 2 - Shahpur"]},
        {"title": "Water Supply Maintenance", "description": "Scheduled maintenance in Ward 12. Water supply will be interrupted from 10AM to 4PM.", "alert_type": "info", "wards": ["Ward 12 - Gandhi Nagar"]},
    ]
    officer = db.officers.find_one({"role": "super_admin"})
    for a in alerts:
        db.alerts.insert_one({
            "title": a["title"], "description": a["description"],
            "alert_type": a["alert_type"], "wards": a["wards"],
            "is_active": True,
            "created_by": str(officer["_id"]) if officer else "system",
            "created_at": datetime.utcnow()
        })
    print(f"✅ {len(alerts)} alerts seeded.")



if __name__ == "__main__":
    print("🌱 Seeding Belagavi Smart City database...")
    clear_collections()
    seed_officers()
    seed_citizens()
    seed_complaints()
    seed_alerts()

    print("\n✅ Database seeding complete!")
    print("\n📋 Login Credentials:")
    print("  CORPORATION PORTAL:")
    print("  Super Admin  → EMP-001 / admin@123")
    print("  Dept Head    → EMP-002 / dept@123")
    print("  Field Officer→ EMP-004 / field@123")
    print("\n  CITIZEN PORTAL:")
    print("  Rajesh Kumar → rajesh@gmail.com / citizen@123")
