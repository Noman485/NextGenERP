from sqlalchemy import Boolean, Column, DateTime, Integer, String, func, text

from database.connection import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=True, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(
        String(20),
        nullable=False,
        default="USER",
        server_default=text("'USER'"),
        index=True,
    )
    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
    )
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    last_login_at = Column(DateTime(timezone=True), nullable=True)
