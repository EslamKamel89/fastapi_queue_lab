from enum import Enum

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from core.models_base import Base, IdMixin, TimestampMixin


class JobStatus(str, Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"


class Job(Base, IdMixin, TimestampMixin):
    __tablename__ = "jobs"
    status: Mapped[JobStatus] = mapped_column(
        String(20),
        nullable=False,
        index=True,
        default=JobStatus.pending,
    )
    payload: Mapped[str] = mapped_column(Text, nullable=False)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
