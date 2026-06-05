"""
Lead Scoring router - Lead score calculations and management
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, LeadScore, Company, Contact
from app.schemas import LeadScoreCreate, LeadScoreResponse
from app.routers.dependencies import get_current_user
from app.services.lead_scorer import calculate_lead_score
from typing import Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/leads", tags=["Lead Scoring"])


@router.get("/scores", response_model=dict)
def list_lead_scores(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    company_id: Optional[int] = Query(None),
    min_score: Optional[float] = Query(None, ge=0, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List lead scores for the current user with pagination and filtering.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        company_id: Optional filter by company
        min_score: Optional filter by minimum score
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Paginated list of lead scores
    """
    query = db.query(LeadScore).filter(LeadScore.user_id == current_user.id)
    
    if company_id:
        query = query.filter(LeadScore.company_id == company_id)
    
    if min_score is not None:
        query = query.filter(LeadScore.score >= min_score)
    
    total = query.count()
    scores = query.order_by(LeadScore.score.desc()).offset(skip).limit(limit).all()
    
    return {
        "items": [LeadScoreResponse.from_orm(s) for s in scores],
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.get("/scores/{score_id}", response_model=LeadScoreResponse)
def get_lead_score(
    score_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific lead score by ID.
    
    Args:
        score_id: Lead score ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Lead score details
        
    Raises:
        HTTPException: If lead score not found or not owned by user
    """
    score = db.query(LeadScore).filter(
        LeadScore.id == score_id,
        LeadScore.user_id == current_user.id
    ).first()
    
    if not score:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead score not found"
        )
    
    return score


@router.post("/score", response_model=LeadScoreResponse, status_code=status.HTTP_201_CREATED)
def calculate_score(
    score_data: LeadScoreCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Calculate and store a lead score for a company-contact pair.
    
    Args:
        score_data: Lead score data with company_id and contact_id
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Created lead score object
        
    Raises:
        HTTPException: If company or contact not found
    """
    # Verify company exists and belongs to user
    company = db.query(Company).filter(
        Company.id == score_data.company_id,
        Company.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    # Verify contact exists and belongs to user
    contact = db.query(Contact).filter(
        Contact.id == score_data.contact_id,
        Contact.user_id == current_user.id
    ).first()
    
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    
    # Check if score already exists
    existing_score = db.query(LeadScore).filter(
        LeadScore.company_id == score_data.company_id,
        LeadScore.contact_id == score_data.contact_id,
        LeadScore.user_id == current_user.id
    ).first()
    
    if existing_score:
        # Update existing score
        score_value, reason = calculate_lead_score(company, contact)
        existing_score.score = score_value
        existing_score.reason = reason
        db.commit()
        db.refresh(existing_score)
        logger.info(f"Lead score updated: Company {company.id} - Contact {contact.id} (Score: {score_value})")
        return existing_score
    
    # Calculate score
    score_value, reason = calculate_lead_score(company, contact)
    
    # Create new lead score
    new_score = LeadScore(
        user_id=current_user.id,
        company_id=score_data.company_id,
        contact_id=score_data.contact_id,
        score=score_value,
        reason=reason
    )
    
    db.add(new_score)
    db.commit()
    db.refresh(new_score)
    
    logger.info(f"Lead score created: Company {company.id} - Contact {contact.id} (Score: {score_value})")
    return new_score


@router.get("/top", response_model=dict)
def get_top_leads(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get top-rated leads ordered by score.
    
    Args:
        limit: Number of top leads to return
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        List of top leads with highest scores
    """
    scores = db.query(LeadScore).filter(
        LeadScore.user_id == current_user.id
    ).order_by(LeadScore.score.desc()).limit(limit).all()
    
    return {
        "items": [LeadScoreResponse.from_orm(s) for s in scores],
        "total": len(scores)
    }
