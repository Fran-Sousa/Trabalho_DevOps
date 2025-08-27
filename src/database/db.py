"""Database connection setup."""
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

engine = create_engine('sqlite:///exemplo.db', echo=True)

Base = declarative_base()


class User(Base):
    """User model."""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String, unique=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime)

    tasks = relationship(
        "Task",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        """String representation of the User."""
        return f"<User(name='{self.name}', username='{self.username}')>"


class Task(Base):
    """User model."""
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    status = Column(String)
    priority = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship("User", back_populates="tasks")

    def __repr__(self):
        """String representation of the Task."""
        return (
            f"<Task(id={self.id}, title='{self.title}', "
            f"status='{self.status}')>"
        )


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
