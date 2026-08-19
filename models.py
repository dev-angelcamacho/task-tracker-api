from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class PersonaModel(Base):
    __tablename__ = "personas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    phone = Column(String(10))
    is_actived = Column(Boolean, default=False)


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)    
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)