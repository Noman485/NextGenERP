from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, event, func

from database.connection import Base


class AuditLog(Base):
    """Append-only record of security-relevant business operations.

    The table intentionally has no update/delete API. ORM listeners and
    database triggers (see ``database.migrations``) reject mutation so that an
    audit trail cannot be rewritten through normal application paths.
    """

    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    actor_user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    actor_username = Column(String(80), nullable=True)
    action = Column(String(80), nullable=False, index=True)
    entity_type = Column(String(40), nullable=False, index=True)
    entity_id = Column(Integer, nullable=True, index=True)
    outcome = Column(String(20), nullable=False, default="success")
    request_id = Column(String(64), nullable=True, index=True)
    ip_address = Column(String(64), nullable=True)
    before_values = Column(JSON, nullable=True)
    after_values = Column(JSON, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        index=True,
    )


def _reject_mutation(_mapper, _connection, _target) -> None:
    raise ValueError("audit_logs is append-only; update and delete are forbidden")


event.listen(AuditLog, "before_update", _reject_mutation)
event.listen(AuditLog, "before_delete", _reject_mutation)
