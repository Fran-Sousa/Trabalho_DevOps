"""Database connection setup."""

import os
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

try:
    from ..config import get_settings
    settings = get_settings()
    DATABASE_URL = settings.database_url
except ImportError:
    project_root = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    db_path = os.path.join(project_root, "src", "database", "exemplo.db")
    DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()


class User(Base):
    """User model."""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String, unique=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime)

    tasks = relationship(
        "Task", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        """String representation of the User."""
        return f"<User(name='{self.name}', username='{self.username}')>"


class Task(Base):
    """User model."""

    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    status = Column(String)
    priority = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="tasks")

    def __repr__(self):
        """String representation of the Task."""
        return (
            f"<Task(id={self.id}, title='{self.title}', "
            f"status='{self.status}')>"
        )


# Database initialization moved to migrations
# Use: alembic upgrade head

Session = sessionmaker(bind=engine)


def get_session():
    """Get database session."""
    return Session()
