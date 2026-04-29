from pydantic import BaseModel, field_validator
from typing import List, Optional


class VendorBase(BaseModel):
    name: str
    data_access_level: str  # none, read-only, read-write, admin
    oauth_scopes: List[str]
    compliance_certs: List[str]


class VendorCreate(VendorBase):
    pass


class VendorUpdate(BaseModel):
    name: Optional[str] = None
    data_access_level: Optional[str] = None
    oauth_scopes: Optional[List[str]] = None
    compliance_certs: Optional[List[str]] = None


class VendorResponse(BaseModel):
    id: int
    name: str
    data_access_level: str
    oauth_scopes: List[str]
    compliance_certs: List[str]
    risk_score: int
    rating: str
    active: bool

    @field_validator('oauth_scopes', 'compliance_certs', mode='before')
    @classmethod
    def split_strings(cls, v):
        if isinstance(v, str):
            return [x for x in v.split(',') if x.strip()] if v else []
        return v

    class Config:
        from_attributes = True


class StatsResponse(BaseModel):
    total_vendors: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    average_risk_score: float
