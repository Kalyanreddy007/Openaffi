"""
Pydantic schemas for request/response validation
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


# User Schemas
class UserBase(BaseModel):
    """Base user schema"""
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr


class UserCreate(UserBase):
    """User creation schema"""
    password: str = Field(..., min_length=8, max_length=255)


class UserResponse(UserBase):
    """User response schema"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Company Schemas
class CompanyBase(BaseModel):
    """Base company schema"""
    company_name: str = Field(..., min_length=1, max_length=255)
    website: Optional[str] = Field(None, max_length=255)
    industry: Optional[str] = Field(None, max_length=255)
    employee_count: Optional[int] = None
    country: Optional[str] = Field(None, max_length=255)
    linkedin_url: Optional[str] = Field(None, max_length=255)


class CompanyCreate(CompanyBase):
    """Company creation schema"""
    pass


class CompanyUpdate(BaseModel):
    """Company update schema"""
    company_name: Optional[str] = Field(None, min_length=1, max_length=255)
    website: Optional[str] = Field(None, max_length=255)
    industry: Optional[str] = Field(None, max_length=255)
    employee_count: Optional[int] = None
    country: Optional[str] = Field(None, max_length=255)
    linkedin_url: Optional[str] = Field(None, max_length=255)


class CompanyResponse(CompanyBase):
    """Company response schema"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Contact Schemas
class ContactBase(BaseModel):
    """Base contact schema"""
    first_name: str = Field(..., min_length=1, max_length=255)
    last_name: str = Field(..., min_length=1, max_length=255)
    title: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    linkedin_url: Optional[str] = Field(None, max_length=255)
    company_id: int


class ContactCreate(ContactBase):
    """Contact creation schema"""
    pass


class ContactUpdate(BaseModel):
    """Contact update schema"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=255)
    last_name: Optional[str] = Field(None, min_length=1, max_length=255)
    title: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    linkedin_url: Optional[str] = Field(None, max_length=255)
    company_id: Optional[int] = None


class ContactResponse(ContactBase):
    """Contact response schema"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Lead Score Schemas
class LeadScoreBase(BaseModel):
    """Base lead score schema"""
    company_id: int
    contact_id: int
    score: float = Field(..., ge=0, le=100)
    reason: Optional[str] = None


class LeadScoreCreate(BaseModel):
    """Lead score creation schema"""
    company_id: int
    contact_id: int


class LeadScoreResponse(LeadScoreBase):
    """Lead score response schema"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Pagination Schemas
class PaginationParams(BaseModel):
    """Pagination parameters"""
    skip: int = Field(0, ge=0)
    limit: int = Field(10, ge=1, le=100)


class PaginatedResponse(BaseModel):
    """Generic paginated response"""
    items: List
    total: int
    skip: int
    limit: int


# Authentication Schemas
class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """JWT token payload"""
    user_id: Optional[int] = None
