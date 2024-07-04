from sqlalchemy import Column, String, Integer

from .database import Base


class Debt(Base):
    __tablename__ = 'debts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    reference_id = Column(String)

    bill_url = Column(String)
