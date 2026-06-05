#!/usr/bin/env python
"""
Seed script to populate database with sample data
Run with: python scripts/seed_data.py
"""
import sys
from datetime import datetime
sys.path.insert(0, '.')

from app.database import SessionLocal
from app.models import User, Company, Contact, LeadScore
from app.utils.auth import hash_password

def seed_database():
    """Populate database with sample data."""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(User).count() > 0:
            print("Database already seeded. Skipping...")
            return
        
        # Create sample user
        user = User(
            name="John Doe",
            email="john@example.com",
            password_hash=hash_password("password123")
        )
        db.add(user)
        db.flush()  # Get user ID
        
        # Create sample companies
        companies = [
            Company(
                user_id=user.id,
                company_name="TechCorp Inc",
                website="https://techcorp.com",
                industry="Technology",
                employee_count=500,
                country="United States",
                linkedin_url="https://linkedin.com/company/techcorp"
            ),
            Company(
                user_id=user.id,
                company_name="StartupXYZ",
                website="https://startupxyz.io",
                industry="SaaS",
                employee_count=50,
                country="United States",
                linkedin_url="https://linkedin.com/company/startupxyz"
            ),
            Company(
                user_id=user.id,
                company_name="GlobalFinance Ltd",
                website="https://globalfinance.com",
                industry="Finance",
                employee_count=2000,
                country="United Kingdom",
                linkedin_url="https://linkedin.com/company/globalfinance"
            )
        ]
        db.add_all(companies)
        db.flush()
        
        # Create sample contacts
        contacts = [
            Contact(
                user_id=user.id,
                company_id=companies[0].id,
                first_name="Alice",
                last_name="Johnson",
                title="CEO",
                email="alice@techcorp.com",
                phone="+1-555-123-4567",
                linkedin_url="https://linkedin.com/in/alice-johnson"
            ),
            Contact(
                user_id=user.id,
                company_id=companies[0].id,
                first_name="Bob",
                last_name="Smith",
                title="VP of Sales",
                email="bob@techcorp.com",
                phone="+1-555-234-5678",
                linkedin_url="https://linkedin.com/in/bob-smith"
            ),
            Contact(
                user_id=user.id,
                company_id=companies[1].id,
                first_name="Charlie",
                last_name="Brown",
                title="Founder",
                email="charlie@startupxyz.io",
                linkedin_url="https://linkedin.com/in/charlie-brown"
            ),
            Contact(
                user_id=user.id,
                company_id=companies[2].id,
                first_name="Diana",
                last_name="Martinez",
                title="Director of Operations",
                email="diana@globalfinance.com",
                phone="+44-20-7946-0958",
                linkedin_url="https://linkedin.com/in/diana-martinez"
            )
        ]
        db.add_all(contacts)
        db.flush()
        
        # Create sample lead scores
        lead_scores = [
            LeadScore(
                user_id=user.id,
                company_id=companies[0].id,
                contact_id=contacts[0].id,
                score=90,
                reason="CEO of tech company - Decision maker | High employee count"
            ),
            LeadScore(
                user_id=user.id,
                company_id=companies[0].id,
                contact_id=contacts[1].id,
                score=85,
                reason="VP of Sales - Key stakeholder | Tech industry"
            ),
            LeadScore(
                user_id=user.id,
                company_id=companies[1].id,
                contact_id=contacts[2].id,
                score=75,
                reason="Founder - Decision maker | SaaS industry"
            ),
            LeadScore(
                user_id=user.id,
                company_id=companies[2].id,
                contact_id=contacts[3].id,
                score=70,
                reason="Director of Operations | Finance industry | UK based"
            )
        ]
        db.add_all(lead_scores)
        
        db.commit()
        print("✅ Database seeded successfully!")
        print(f"   - Created 1 user")
        print(f"   - Created {len(companies)} companies")
        print(f"   - Created {len(contacts)} contacts")
        print(f"   - Created {len(lead_scores)} lead scores")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
