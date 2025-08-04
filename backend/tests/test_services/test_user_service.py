from backend.services.user_service import get_or_create_user_from_identity
from backend.tests.factories import UserFactory, IdentityFactory
from backend.models import User, Identity

def test_creates_new_user_and_identity(db_session):
    user_count = db_session.query(User).count()
    identity_count = db_session.query(Identity).count()

    user = get_or_create_user_from_identity(
        db=db_session,
        provider="google",
        provider_user_id="12345",
        email="new.user@example.com",
        name="New User"
    )

    assert db_session.query(User).count() == user_count + 1
    assert db_session.query(Identity).count() == identity_count + 1
    assert user.email == "new.user@example.com"
    assert user.identities[0].provider_user_id == "12345"

def test_returns_existing_user_for_existing_identity(db_session):
    IdentityFactory._meta.sqlalchemy_session = db_session
    UserFactory._meta.sqlalchemy_session = db_session
    
    existing_identity = IdentityFactory(provider="google", provider_user_id="54321")
    user_count = db_session.query(User).count()
    identity_count = db_session.query(Identity).count()

    user = get_or_create_user_from_identity(
        db=db_session,
        provider="google",
        provider_user_id="54321",
        email=existing_identity.user.email,
        name=existing_identity.user.name
    )

    assert db_session.query(User).count() == user_count
    assert db_session.query(Identity).count() == identity_count
    assert user.id == existing_identity.user.id

def test_links_new_identity_to_existing_user_by_email(db_session):
    UserFactory._meta.sqlalchemy_session = db_session
    IdentityFactory._meta.sqlalchemy_session = db_session
    
    existing_user = UserFactory(email="existing.user@example.com")
    user_count = db_session.query(User).count()
    identity_count = db_session.query(Identity).count()

    user = get_or_create_user_from_identity(
        db=db_session,
        provider="github",
        provider_user_id="gh-9876",
        email="existing.user@example.com",
        name=existing_user.name
    )

    assert db_session.query(User).count() == user_count
    assert db_session.query(Identity).count() == identity_count + 1
    assert user.id == existing_user.id
    assert len(user.identities) == 1
    assert user.identities[0].provider == "github"