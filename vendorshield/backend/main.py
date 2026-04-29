from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from database import engine, get_db, Base
from schemas import VendorCreate, VendorUpdate, VendorResponse, StatsResponse
from risk_calculator import calculate_risk_score, get_rating
import models

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="VendorShield API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/stats", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics"""
    vendors = db.query(models.Vendor).filter(models.Vendor.active == True).all()
    
    total = len(vendors)
    high_risk = sum(1 for v in vendors if v.rating == "red")
    medium_risk = sum(1 for v in vendors if v.rating == "amber")
    low_risk = sum(1 for v in vendors if v.rating == "green")
    avg_score = sum(v.risk_score for v in vendors) / total if total > 0 else 0
    
    return StatsResponse(
        total_vendors=total,
        high_risk_count=high_risk,
        medium_risk_count=medium_risk,
        low_risk_count=low_risk,
        average_risk_score=round(avg_score, 1)
    )


@app.get("/api/vendors", response_model=List[VendorResponse])
def list_vendors(db: Session = Depends(get_db)):
    """List all active vendors"""
    vendors = db.query(models.Vendor).filter(models.Vendor.active == True).all()
    return vendors


@app.get("/api/vendors/{vendor_id}", response_model=VendorResponse)
def get_vendor(vendor_id: int, db: Session = Depends(get_db)):
    """Get vendor by ID"""
    vendor = db.query(models.Vendor).filter(models.Vendor.id == vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return vendor


@app.post("/api/vendors", response_model=VendorResponse)
def create_vendor(vendor: VendorCreate, db: Session = Depends(get_db)):
    """Create a new vendor"""
    # Check if vendor already exists
    existing = db.query(models.Vendor).filter(models.Vendor.name == vendor.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Vendor with this name already exists")
    
    # Calculate risk score
    risk_score = calculate_risk_score(
        vendor.data_access_level,
        vendor.oauth_scopes,
        vendor.compliance_certs
    )
    rating = get_rating(risk_score)
    
    # Create vendor
    db_vendor = models.Vendor(
        name=vendor.name,
        data_access_level=vendor.data_access_level,
        oauth_scopes=",".join(vendor.oauth_scopes),
        compliance_certs=",".join(vendor.compliance_certs),
        risk_score=risk_score,
        rating=rating
    )
    db.add(db_vendor)
    db.commit()
    db.refresh(db_vendor)
    return db_vendor


@app.put("/api/vendors/{vendor_id}", response_model=VendorResponse)
def update_vendor(vendor_id: int, vendor_update: VendorUpdate, db: Session = Depends(get_db)):
    """Update an existing vendor"""
    db_vendor = db.query(models.Vendor).filter(models.Vendor.id == vendor_id).first()
    if not db_vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    
    # Update fields
    update_data = vendor_update.model_dump(exclude_unset=True)
    
    if "oauth_scopes" in update_data:
        update_data["oauth_scopes"] = ",".join(update_data["oauth_scopes"])
    if "compliance_certs" in update_data:
        update_data["compliance_certs"] = ",".join(update_data["compliance_certs"])
    
    # Recalculate risk score if relevant fields changed
    if any(key in update_data for key in ["data_access_level", "oauth_scopes", "compliance_certs"]):
        oauth_scopes = update_data.get("oauth_scopes", db_vendor.oauth_scopes).split(",") if update_data.get("oauth_scopes") else db_vendor.oauth_scopes.split(",")
        compliance_certs = update_data.get("compliance_certs", db_vendor.compliance_certs).split(",") if update_data.get("compliance_certs") else db_vendor.compliance_certs.split(",")
        data_access = update_data.get("data_access_level", db_vendor.data_access_level)
        
        risk_score = calculate_risk_score(data_access, oauth_scopes, compliance_certs)
        rating = get_rating(risk_score)
        update_data["risk_score"] = risk_score
        update_data["rating"] = rating
    
    for field, value in update_data.items():
        setattr(db_vendor, field, value)
    
    db.commit()
    db.refresh(db_vendor)
    return db_vendor


@app.delete("/api/vendors/{vendor_id}")
def delete_vendor(vendor_id: int, db: Session = Depends(get_db)):
    """Delete a vendor (soft delete)"""
    db_vendor = db.query(models.Vendor).filter(models.Vendor.id == vendor_id).first()
    if not db_vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    
    db_vendor.active = False
    db.commit()
    return {"message": "Vendor deleted successfully"}


@app.get("/")
def root():
    return {"message": "Welcome to VendorShield API", "docs": "/docs"}
