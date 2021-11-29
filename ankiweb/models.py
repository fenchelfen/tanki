from sqlalchemy import create_engine, Integer, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

import schemas

SQLALCHEMY_DATABASE_URL = "postgresql://tanki:tanki@postgres/tanki"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = "User"

    email = Column(Integer, primary_key=True, index=True)
    cookie = Column(String)


def create_user(db: Session, user: schemas.UserCreate):
    db_user = User(email=user.email, cookie=user.cookie)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
