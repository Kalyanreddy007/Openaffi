"""
Authentication router - User registration and login
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse, Token
from app.utils.auth import hash_password, verify_password, create_access_token
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    
    Args:
        user_data: User registration data
        db: Database session
        
    Returns:
        Created user object
        
    Raises:
        HTTPException: If email already exists
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        logger.warning(f"Registration attempt with existing email: {user_data.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    hashed_password = hash_password(user_data.password)
    
    # Create new user
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    logger.info(f"New user registered: {user_data.email}")
    return new_user


@router.post("/login", response_model=Token)
def login(email: str, password: str, db: Session = Depends(get_db)):
    """
    Login user and return JWT token.
    
    Args:
        email: User email
        password: User password
        db: Database session
        
    Returns:
        JWT access token
        
    Raises:
        HTTPException: If credentials are invalid
    """
    # Find user by email
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        logger.warning(f"Login attempt with non-existent email: {email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Verify password
    if not verify_password(password, user.password_hash):
        logger.warning(f"Failed login attempt for email: {email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Create JWT token
    access_token_expires = timedelta(
        minutes=30  # Configurable in settings
    )
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id},
        expires_delta=access_token_expires
    )
    
    logger.info(f"User logged in: {email}")
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 1800  # 30 minutes in seconds
    }


@router.post("/refresh", response_model=Token)
def refresh_token(
    current_user: User = Depends(lambda db: db),
    db: Session = Depends(get_db)
):
    """
    Refresh JWT token (placeholder for token refresh logic).
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        New JWT access token
    """
    # This is a placeholder - implement full token refresh logic as needed
    access_token = create_access_token(
        data={"sub": current_user.email, "user_id": current_user.id}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 1800
    }
