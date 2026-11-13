from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from database.connection import Base


class RefreshToken(Base):
    """Server-side refresh-token session with rotation and revocation.

    Only the SHA-256 hash of the opaque token is stored. ``family_id`` groups
    every rotation of one login session so reuse detection can revoke the whole
    family, and access tokens carry the same id as their ``sid`` claim.
    """

    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    token_hash = Column(String(64), unique=True, nullable=False, index=True)
    family_id = Column(String(64), nullable=False, index=True)
    issued_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)
    revoked_at = Column(DateTime(timezone=True), nullable=True)
    replaced_by_id = Column(
        Integer,
        ForeignKey("refresh_tokens.id", ondelete="SET NULL"),
        nullable=True,
    )
    user_agent = Column(String(255), nullable=True)
    ip_address = Column(String(64), nullable=True)
    last_used_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User")
    replaced_by = relationship("RefreshToken", remote_side=[id])
