# Karnataka Rural Healthcare Intelligence & Decision Support Platform

An AI-assisted healthcare decision-support system designed for Karnataka district/state health administrators and Mobile Medical Unit (MMU) coordinators.

## Core Purpose & Principles

The platform directly answers three fundamental administrative questions at every level:
1. **WHERE** is the healthcare problem? (Geospatial vulnerability mapping across 30,773 LGD villages)
2. **WHY** is it happening? (Explainable AI factor breakdown with SHAP feature attributions across 10 health/infra dimensions)
3. **WHAT** should the health department do next? (Actionable, human-in-the-loop resource allocation and MMU mission dispatch recommendations)

---

## Technical Stack

### Frontend
- **Framework**: Next.js 14+ (App Router) + React 18 + TypeScript 5
- **Styling**: Tailwind CSS v3 + Custom Government Theme
- **Map & Geospatial**: Leaflet / MapLibre GL + OpenStreetMap
- **State & Querying**: TanStack Query v5 + Context API

### Backend
- **Framework**: Python 3.11+ FastAPI (AsyncIO)
- **Database**: PostgreSQL / PostGIS (SQLite compatibility included)
- **ML & Explainability**: Scikit-Learn + SHAP + Custom 10-Dimensional Scoring Engine
- **Auth & Security**: OAuth2 JWT + SHA-256 Tamper-Resistant Audit Logging

---

## Getting Started

### 1. Backend Setup & Ingestion
```bash
cd backend
pip install -r requirements.txt
python -m app.seed_data
python -m uvicorn app.main:app --reload --port 8000
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:3000` in your browser.

---

## Role Personas & Demo Credentials

| Role Persona | Email | Password | Scope |
| :--- | :--- | :--- | :--- |
| **State Health Administrator** | `state_admin@karnataka.gov.in` | `admin123` | Karnataka State-wide |
| **District Health Officer (DHO)** | `dho_bagalkote@karnataka.gov.in` | `dho123` | Bagalkote District (Code 524) |
| **MMU Fleet Coordinator** | `mmu_coord_bagalkote@karnataka.gov.in` | `mmu123` | Sector 1 Fleet Dispatch |
| **System Administrator** | `sysadmin@karnataka.gov.in` | `sys123` | System Ingestion & Security |
