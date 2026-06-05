"""
Contact router - CRUD operations for contacts
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database import get_db
from app.models import User, Contact, Company
from app.schemas import ContactCreate, ContactResponse, ContactUpdate
from app.routers.dependencies import get_current_user
from typing import Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/contacts", tags=["Contacts"])


@router.get("", response_model=dict)
def list_contacts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    company_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all contacts for the current user with pagination and filtering.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        company_id: Filter by company ID
        search: Search by name or email
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Paginated list of contacts
    """
    query = db.query(Contact).filter(Contact.user_id == current_user.id)
    
    # Filter by company
    if company_id:
        query = query.filter(Contact.company_id == company_id)
    
    # Apply search filter
    if search:
        query = query.filter(
            or_(
                Contact.first_name.ilike(f"%{search}%"),
                Contact.last_name.ilike(f"%{search}%"),
                Contact.email.ilike(f"%{search}%")
            )
        )
    
    total = query.count()
    contacts = query.offset(skip).limit(limit).all()
    
    return {
        "items": [ContactResponse.from_orm(c) for c in contacts],
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific contact by ID.
    
    Args:
        contact_id: Contact ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Contact details
        
    Raises:
        HTTPException: If contact not found or not owned by user
    """
    contact = db.query(Contact).filter(
        Contact.id == contact_id,
        Contact.user_id == current_user.id
    ).first()
    
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    
    return contact


@router.post("", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def create_contact(
    contact_data: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new contact.
    
    Args:
        contact_data: Contact creation data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Created contact object
        
    Raises:
        HTTPException: If company not found or not owned by user
    """
    # Verify company exists and belongs to user
    company = db.query(Company).filter(
        Company.id == contact_data.company_id,
        Company.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    new_contact = Contact(
        user_id=current_user.id,
        **contact_data.dict()
    )
    
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    
    logger.info(f"Contact created: {new_contact.first_name} {new_contact.last_name} (ID: {new_contact.id})")
    return new_contact


@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact(
    contact_id: int,
    contact_data: ContactUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update an existing contact.
    
    Args:
        contact_id: Contact ID
        contact_data: Contact update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Updated contact object
        
    Raises:
        HTTPException: If contact not found or not owned by user
    """
    contact = db.query(Contact).filter(
        Contact.id == contact_id,
        Contact.user_id == current_user.id
    ).first()
    
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    
    # Verify new company if provided
    if contact_data.company_id and contact_data.company_id != contact.company_id:
        company = db.query(Company).filter(
            Company.id == contact_data.company_id,
            Company.user_id == current_user.id
        ).first()
        
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company not found"
            )
    
    # Update only provided fields
    update_data = contact_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(contact, key, value)
    
    db.commit()
    db.refresh(contact)
    
    logger.info(f"Contact updated: {contact.first_name} {contact.last_name} (ID: {contact.id})")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a contact.
    
    Args:
        contact_id: Contact ID
        db: Database session
        current_user: Current authenticated user
        
    Raises:
        HTTPException: If contact not found or not owned by user
    """
    contact = db.query(Contact).filter(
        Contact.id == contact_id,
        Contact.user_id == current_user.id
    ).first()
    
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    
    db.delete(contact)
    db.commit()
    
    logger.info(f"Contact deleted: {contact.first_name} {contact.last_name} (ID: {contact.id})")


@router.get("/search", response_model=dict)
def search_contacts(
    query: str = Query(..., min_length=1),
    title: Optional[str] = Query(None),
    company_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Advanced search for contacts.
    
    Args:
        query: Search query
        title: Optional job title filter
        company_id: Optional company filter
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        List of matching contacts
    """
    search_query = db.query(Contact).filter(
        Contact.user_id == current_user.id,
        or_(
            Contact.first_name.ilike(f"%{query}%"),
            Contact.last_name.ilike(f"%{query}%"),
            Contact.email.ilike(f"%{query}%")
        )
    )
    
    if title:
        search_query = search_query.filter(Contact.title.ilike(f"%{title}%"))
    
    if company_id:
        search_query = search_query.filter(Contact.company_id == company_id)
    
    contacts = search_query.limit(50).all()
    
    return {
        "items": [ContactResponse.from_orm(c) for c in contacts],
        "total": len(contacts)
    }
