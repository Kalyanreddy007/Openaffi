"""
Lead Scoring Service - Business logic for calculating lead scores
"""
from app.models import Company, Contact
import logging

logger = logging.getLogger(__name__)


def calculate_lead_score(company: Company, contact: Contact) -> tuple[float, str]:
    """
    Calculate a lead score based on company and contact information.
    
    Scoring Criteria:
    - Company size (employee count)
    - Industry relevance
    - Contact title (decision-maker indicator)
    - Email availability
    - Company website presence
    
    Args:
        company: Company object
        contact: Contact object
        
    Returns:
        Tuple of (score: float, reason: str)
    """
    score = 0.0
    reasons = []
    
    # Company Size Score (0-25 points)
    # Assumes companies with 50-1000 employees are ideal targets
    if company.employee_count:
        if 50 <= company.employee_count <= 1000:
            score += 25
            reasons.append("Ideal company size (50-1000 employees)")
        elif 10 <= company.employee_count < 50:
            score += 15
            reasons.append("Small company (10-50 employees)")
        elif 1000 < company.employee_count <= 5000:
            score += 20
            reasons.append("Mid-size company (1000-5000 employees)")
        elif company.employee_count > 5000:
            score += 10
            reasons.append("Large enterprise (5000+ employees)")
    
    # Industry Score (0-15 points)
    # Add more industries as needed
    high_value_industries = [
        "technology", "saas", "software", "fintech",
        "healthcare", "biotech", "finance", "consulting"
    ]
    if company.industry:
        industry_lower = company.industry.lower()
        if any(ind in industry_lower for ind in high_value_industries):
            score += 15
            reasons.append(f"High-value industry: {company.industry}")
        else:
            score += 5
            reasons.append(f"Standard industry: {company.industry}")
    
    # Contact Title Score (0-30 points)
    # Decision-makers have higher scores
    decision_maker_titles = [
        "ceo", "cto", "cfo", "vp", "vice president", "director",
        "head of", "president", "founder", "chief", "executive"
    ]
    if contact.title:
        title_lower = contact.title.lower()
        if any(title in title_lower for title in decision_maker_titles):
            score += 30
            reasons.append(f"Decision-maker identified: {contact.title}")
        else:
            score += 10
            reasons.append(f"Regular contact title: {contact.title}")
    else:
        reasons.append("Contact title not specified")
    
    # Email Availability Score (0-15 points)
    if contact.email:
        score += 15
        reasons.append("Email available for outreach")
    else:
        reasons.append("Email not available")
    
    # Website Presence Score (0-10 points)
    if company.website:
        score += 10
        reasons.append("Company website verified")
    
    # LinkedIn Score (0-5 points)
    if contact.linkedin_url:
        score += 5
        reasons.append("LinkedIn profile available")
    
    # Cap score at 100
    final_score = min(score, 100.0)
    reason_text = " | ".join(reasons) if reasons else "Default score"
    
    logger.debug(f"Lead score calculated: {final_score} - {reason_text}")
    
    return final_score, reason_text
