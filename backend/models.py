import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text,
    Boolean
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    """
    Represents a user in the system.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    identities = relationship("Identity", back_populates="user", cascade="all, delete-orphan")
    responses = relationship("Response", back_populates="user", cascade="all, delete-orphan")
    memory = relationship("UserMemory", uselist=False, back_populates="user")

class Identity(Base):
    """
    Represents a method a user can use to authenticate.
    """
    __tablename__ = "identities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider = Column(String, nullable=False)
    provider_user_id = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=True)

    user = relationship("User", back_populates="identities")

class Question(Base):
    """
    Represents a question presented to a user.
    """
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    discipline = Column(String, index=True)
    options = Column(Text, nullable=True)  # JSON string of multiple choice options
    correct_answer = Column(String, nullable=True)
    explanation = Column(Text, nullable=True)
    difficulty = Column(String, nullable=True)
    topics = Column(Text, nullable=True)  # JSON string of topic tags
    upvotes = Column(Integer, default=0)
    downvotes = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    responses = relationship("Response", back_populates="question")

class Response(Base):
    """
    Represents a user's answer to a specific question.
    """
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    user_answer = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=True)
    feedback = Column(Text, nullable=True)  # AI-generated feedback
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="responses")
    question = relationship("Question", back_populates="responses")

class SSOConfiguration(Base):
    """
    Stores SAML/OIDC configuration details for partner institutions.
    """
    __tablename__ = "sso_configurations"

    id = Column(Integer, primary_key=True, index=True)
    institution_name = Column(String, unique=True, nullable=False)
    domain = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    idp_entity_id = Column(String)
    idp_sso_url = Column(String)
    idp_x509_cert = Column(Text)

class UserMemory(Base):
    """
    Stores a continually condensed summary of a user's chat history.
    """
    __tablename__ = "user_memory"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    condensed_history = Column(Text, nullable=True)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="memory")