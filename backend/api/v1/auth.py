import os
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth

from backend import schemas
from backend.models import Identity, SSOConfiguration
from backend.database import get_db
from backend.services.user_service import get_or_create_user_from_identity
from backend.auth.password import get_password_hash, verify_password
from backend.auth.jwt import create_access_token

router = APIRouter()

oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    client_kwargs={'scope': 'openid email profile'}
)

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_identity = db.query(Identity).filter(
        Identity.provider == "password",
        Identity.provider_user_id == user.email
    ).first()

    if existing_identity:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )
    
    new_user = get_or_create_user_from_identity(
        db=db,
        provider="password",
        provider_user_id=user.email,
        email=user.email,
        name=user.name
    )

    hashed_password = get_password_hash(user.password)
    identity = db.query(Identity).filter(Identity.user_id == new_user.id, Identity.provider == "password").first()
    identity.password_hash = hashed_password
    db.commit()

    return {"message": "User created successfully."}

@router.post("/login", response_model=schemas.Token)
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    identity = db.query(Identity).filter(
        Identity.provider == "password",
        Identity.provider_user_id == form_data.username
    ).first()

    if not identity or not identity.password_hash or not verify_password(form_data.password, identity.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": str(identity.user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get('/google/login')
async def google_login(request: Request):
    redirect_uri = request.url_for('google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get('/google/callback', response_model=schemas.Token)
async def google_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get('userinfo')

    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not retrieve user info from Google."
        )

    user = get_or_create_user_from_identity(
        db=db,
        provider="google",
        provider_user_id=user_info['sub'],
        email=user_info['email'],
        name=user_info['name']
    )

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/sso/login")
def sso_login(email: schemas.EmailStr, db: Session = Depends(get_db)):
    domain = email.split('@')[1]
    sso_config = db.query(SSOConfiguration).filter(SSOConfiguration.domain == domain).first()
    if not sso_config or not sso_config.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active SSO configuration for this institution."
        )
    return {"message": "SSO login initiated for domain", "domain": domain}

@router.post("/sso/callback")
def sso_callback(request: Request):
    return {"message": "SSO callback received. User would be processed here."}