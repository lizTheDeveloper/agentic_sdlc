from sqlalchemy import Column, Integer, String, Boolean

# Import Base from database to share the same metadata
from database import Base


class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    data_access_level = Column(String, nullable=False)
    oauth_scopes = Column(String, nullable=False)
    compliance_certs = Column(String, nullable=False)
    risk_score = Column(Integer, default=0)
    rating = Column(String, default="green")
    active = Column(Boolean, default=True)
