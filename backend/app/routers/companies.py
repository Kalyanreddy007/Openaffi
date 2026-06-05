"""
Company router - CRUD operations for companies
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database import get_db
from app.models import User, Company
from app.schemas import CompanyCreate, CompanyResponse, CompanyUpdate
from app.routers.dependencies import get_current_user
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/companies", tags=["Companies"])


@router.get("", response_model=dict)
def list_companies(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    industry: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all companies for the current user with pagination and filtering.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        search: Search by company name or website
        industry: Filter by industry
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Paginated list of companies
    """
    query = db.query(Company).filter(Company.user_id == current_user.id)
    
    # Apply search filter
    if search:
        query = query.filter(
            or_(
                Company.company_name.ilike(f"%{search}%"),
                Company.website.ilike(f"%{search}%")
            )
        )
    
    # Apply industry filter
    if industry:
        query = query.filter(Company.industry.ilike(f"%{industry}%"))
    
    total = query.count()
    companies = query.offset(skip).limit(limit).all()
    
    return {
        "items": [CompanyResponse.from_orm(c) for c in companies],
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific company by ID.
    
    Args:
        company_id: Company ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Company details
        
    Raises:
        HTTPException: If company not found or not owned by user
    """
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    return company


@router.post("", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
def create_company(
    company_data: CompanyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new company.
    
    Args:
        company_data: Company creation data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Created company object
    """
    new_company = Company(
        user_id=current_user.id,
        **company_data.dict()
    )
    
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    
    logger.info(f"Company created: {new_company.company_name} (ID: {new_company.id})")
    return new_company


@router.put("/{company_id}", response_model=CompanyResponse)
def update_company(
    company_id: int,
    company_data: CompanyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update an existing company.
    
    Args:
        company_id: Company ID
        company_data: Company update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Updated company object
        
    Raises:
        HTTPException: If company not found or not owned by user
    """
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    # Update only provided fields
    update_data = company_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(company, key, value)
    
    db.commit()
    db.refresh(company)
    
    logger.info(f"Company updated: {company.company_name} (ID: {company.id})")
    return company


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a company.
    
    Args:
        company_id: Company ID
        db: Database session
        current_user: Current authenticated user
        
    Raises:
        HTTPException: If company not found or not owned by user
    """
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    db.delete(company)
    db.commit()
    
    logger.info(f"Company deleted: {company.company_name} (ID: {company.id})")


@router.get("/search", response_model=dict)
def search_companies(
    query: str = Query(..., min_length=1),
    industry: Optional[str] = Query(None),
    country: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Advanced search for companies.
    
    Args:
        query: Search query
        industry: Optional industry filter
        country: Optional country filter
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        List of matching companies
    """
    search_query = db.query(Company).filter(
        Company.user_id == current_user.id,
        or_(
            Company.company_name.ilike(f"%{query}%"),
            Company.website.ilike(f"%{query}%")
        )
    )
    
    if industry:
        search_query = search_query.filter(Company.industry.ilike(f"%{industry}%"))
    
    if country:
        search_query = search_query.filter(Company.country.ilike(f"%{country}%"))
    
    companies = search_query.limit(50).all()
    
    return {
        "items": [CompanyResponse.from_orm(c) for c in companies],
        "total": len(companies)
    }
