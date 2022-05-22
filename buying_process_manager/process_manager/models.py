from datetime import datetime

from process_manager.database import Base
from sqlalchemy import JSON, Column, DateTime, Integer


class ProcessManager(Base):
    __tablename__ = "process_managers"

    id = Column(Integer(), primary_key=True)
    product_id = Column(Integer(), nullable=False)
    data = Column(JSON(), nullable=False)
    when_created = Column(DateTime(), nullable=False, default=datetime.utcnow)
    when_finished = Column(DateTime(), nullable=True)
    # timeout_at = Column(DateTime(), nullable=False)
