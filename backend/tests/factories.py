import factory
from factory.alchemy import SQLAlchemyModelFactory
from backend.models import User, Identity, Question, Response

class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = "commit"

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Faker("name")
    email = factory.Faker("email")

class IdentityFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Identity
        sqlalchemy_session_persistence = "commit"

    id = factory.Sequence(lambda n: n + 1)
    provider = "google"
    provider_user_id = factory.Faker("uuid4")
    
    user = factory.SubFactory(UserFactory)

class QuestionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Question
        sqlalchemy_session_persistence = "commit"

    id = factory.Sequence(lambda n: n + 1)
    content = factory.Faker("text", max_nb_chars=200)
    discipline = factory.Faker("word")

class ResponseFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Response
        sqlalchemy_session_persistence = "commit"

    id = factory.Sequence(lambda n: n + 1)
    user_answer = factory.Faker("text", max_nb_chars=100)
    is_correct = factory.Faker("boolean")
    
    user = factory.SubFactory(UserFactory)
    question = factory.SubFactory(QuestionFactory)