import factory
from factory.alchemy import SQLAlchemyModelFactory
from backend.models import User, Identity
from backend.tests.conftest import TestingSessionLocal

class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = TestingSessionLocal
        sqlalchemy_session_persistence = "commit"

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Faker("name")
    email = factory.Faker("email")

class IdentityFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Identity
        sqlalchemy_session = TestingSessionLocal
        sqlalchemy_session_persistence = "commit"

    id = factory.Sequence(lambda n: n + 1)
    provider = "google"
    provider_user_id = factory.Faker("uuid4")
    
    user = factory.SubFactory(UserFactory)