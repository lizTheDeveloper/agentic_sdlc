# VendorShield - AI Vendor Risk Assessment Tool

## Overview
Single-page application for assessing and monitoring AI vendor risks with automated scoring and traffic-light dashboard.

## Tech Stack
- **Backend**: Python FastAPI, SQLite
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Database**: SQLite (local development)

## Features
1. Add/edit AI vendors with:
   - Name
   - Data access level (None, Read-only, Read-Write, Admin)
   - OAuth scopes (email, profile, files, admin, etc.)
   - Compliance certifications (SOC2, ISO27001, GDPR, HIPAA)
2. Auto-calculate risk score (0-100)
3. Dashboard with traffic-light ratings (Red/Amber/Green)
4. Vendor detail views with risk breakdown
5. Search and filter capabilities

## Risk Score Algorithm
```
Base Score = 0

Data Access Points:
- None: 0
- Read-only: 15
- Read-Write: 30
- Admin: 40

OAuth Scope Points (cumulative):
- email: 5
- profile: 8
- files: 15
- write: 20
- admin: 35

Compliance Reductions (stacking):
- SOC2: -5
- ISO27001: -5
- GDPR: -8
- HIPAA: -10

Final Score = max(0, min(100, Base + Data Access + OAuth - Compliance))

Rating:
- 0-30: Green (Low Risk)
- 31-60: Amber (Medium Risk)
- 61-100: Red (High Risk)
```

## Project Structure
```
vendorshield/
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── schemas.py
│   └── risk_calculator.py
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── styles.css
│   └── js/
│       ├── app.js
│       ├── api.js
│       └── components.js
└── README.md
```

## API Endpoints
- `GET /api/vendors` - List all vendors
- `GET /api/vendors/{id}` - Get vendor details
- `POST /api/vendors` - Create vendor
- `PUT /api/vendors/{id}` - Update vendor
- `DELETE /api/vendors/{id}` - Delete vendor
- `GET /api/stats` - Dashboard statistics

## Vercel Breach Prevention
This tool would have flagged the Vercel breach scenario by:
1. Detecting high-risk OAuth scopes (admin + files)
2. Identifying excessive data access levels
3. Highlighting missing compliance certifications
4. Providing visual warnings before integration
