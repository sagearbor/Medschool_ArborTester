from sqlalchemy.orm import Session
from backend.models import User, Identity

def get_or_create_user_from_identity(
    db: Session,
    provider: str,
    provider_user_id: str,
    email: str,
    name: str
) -> User:
    """
    Finds a user based on their identity or email.
    """
    identity = db.query(Identity).filter(
        Identity.provider == provider,
        Identity.provider_user_id == provider_user_id
    ).first()

    if identity:
        return identity.user

    user = db.query(User).filter(User.email == email).first()

    if not user:
        user = User(email=email, name=name)
        db.add(user)
        db.flush()

    new_identity = Identity(
        provider=provider,
        provider_user_id=provider_user_id,
        user_id=user.id
    )
    db.add(new_identity)
    db.commit()
    db.refresh(user)

    return user