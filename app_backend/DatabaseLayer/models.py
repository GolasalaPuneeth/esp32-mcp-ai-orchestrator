from datetime import datetime
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, JSON
from datetime import datetime, timezone
from typing import Optional


class PayloadErrorLogs(SQLModel, table=True):
    __tablename__ = "payload_error_logs"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    payload_hash: str
    source_id: str
    channel: str
    raw_text: str
    error_info:str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
        )