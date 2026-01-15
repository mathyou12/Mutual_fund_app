from sqlalchemy import Column, Integer, String, Float
from database import Base

class Investment(Base):
    __tablename__ = "investments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    fund_name = Column(String)
    amount = Column(Float)


class SIP(Base):
    __tablename__ = "sips"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    fund_name = Column(String)
    amount = Column(Float)
    frequency = Column(String)
    status = Column(String)


# ⭐ NEW: Fund Performance (DOCUMENT FEATURE)
class FundPerformance(Base):
    __tablename__ = "fund_performance"

    id = Column(Integer, primary_key=True, index=True)
    fund_name = Column(String)
    category = Column(String)
    return_1y = Column(Float)
    benchmark_return = Column(Float)
