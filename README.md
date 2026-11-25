# 🏥 Karnataka Rural Healthcare Intelligence Platform (KRHI)

> **AI-Assisted Rural Healthcare Decision Support & Mobile Medical Unit (MMU) Dispatch Platform for Government of Karnataka**

---

## 📌 Executive Overview

The **Karnataka Rural Healthcare Intelligence Platform (KRHI)** is an AI-powered, multi-layered decision-support platform designed for District Health Officers (DHOs), Mobile Medical Unit (MMU) Coordinators, and State Health Administrators in Karnataka, India. 

Leveraging official 6-digit **Local Government Directory (LGD 2026)** codes across **30,771 villages**, **240 taluks**, and **31 districts**, KRHI combines 11 real-world health domain datasets with a **4-Tier AI Fallback Cascade** (powered by **IBM watsonx.ai** and **Groq Cloud API**) to provide real-time vulnerability scoring, explainable risk factors, and automated resource deployment recommendations.

---

## 🌟 Key Platform Capabilities

- **11-Layer Domain Health Indicators**: Real-time integration of demographic, epidemiological, spatial, seasonal, and infrastructural datasets.
- **4-Tier Zero-Failure AI Cascade**: 
  1. **Primary**: IBM watsonx.ai (`ibm/granite-3-8b-instruct`)
  2. **Secondary**: Groq Cloud API (`groq/compound` - Llama 3.3 / Llama 3.1)
  3. **Tertiary**: xAI Grok API (`grok-beta`)
  4. **Deterministic Engine**: Rule-based fallback shield guaranteeing 100% uptime.
- **Multi-Factor Risk Scoring Engine**: Calculates composite vulnerability scores (0–100) and categorizes villages into:
  - 🔴 **CRITICAL** ($\ge 75.0$)
  - 🟡 **HIGH** ($60.0 - 74.9$)
  - 🔵 **MEDIUM** ($40.0 - 59.9$)
  - 🟢 **LOW** ($< 40.0$)
- **Explainable AI (XAI)**: Breaks down risk scores into top contributing factors (e.g., PHC transit distance, seasonal road blockage, ANC gap, water quality index).
- **Strict Role-Based Access Control (RBAC)**: Custom scoped views for District Health Officers (DHO), MMU Coordinators, State Administrators, and System Administrators.

---

## 🔄 High-Level Platform Workflow

```mermaid
flowchart LR
    A["📊 Data Ingestion<br/>(11 Health Domain Datasets)"] --> B["🧮 Scoring Engine<br/>(Composite Risk Score 0-100)"]
    B --> C["🤖 AI Copilot Cascade<br/>(watsonx ➔ Groq ➔ Grok ➔ Fallback)"]
    C --> D["🔑 Role-Based Dashboard (RBAC)<br/>(DHO / MMU / State / Admin Views)"]
    D --> E["🚑 Field Deployment<br/>(MMU Dispatch / Vaccine Buffer / ASHA)"]
```

---

## 🏗 Detailed System Architecture

```mermaid
flowchart TD
    subgraph DataLayer [11-Layer Health Domain Datasets]
        D1[Demographics & LGD]
        D2[PHC Transit & Infra]
        D3[Maternal & Child Health]
        D4[Epidemiological Data]
        D5[Monsoon Road Hazards]
    end

    subgraph Backend [FastAPI Backend Engine - Port 8000]
        API[FastAPI Router /api/v1]
        DB[(SQLite / PostgreSQL krhi.db)]
        RBAC[RBAC JWT Middleware]
        SCORE[7-Dimension Composite Scoring]
        
        subgraph AICascade [4-Tier AI Copilot Cascade]
            T1[Tier 1: IBM watsonx.ai]
            T2[Tier 2: Groq Cloud API]
            T3[Tier 3: xAI Grok API]
            T4[Tier 4: Zero-Failure Engine]
            T1 -->|Fallback| T2
            T2 -->|Fallback| T3
            T3 -->|Fallback| T4
        end
    end

    subgraph Frontend [Next.js 15 Tailwind Dashboard - Port 3000]
        UI1[Executive Dashboard]
        UI2[Village Intelligence Modal]
        UI3[Geospatial Map Intelligence]
        UI4[System User Administration]
    end

    DataLayer --> SCORE
    SCORE --> DB
    API --> RBAC
    API --> AICascade
    Frontend <-->|REST API / JWT| API
```

---

## 📂 Project Structure

```directory
IBM HACK/
├── platform/
│   ├── backend/                 # FastAPI Python Backend
│   │   ├── app/
│   │   │   ├── api/v1/          # REST Endpoints (watsonx, villages, admin, auth)
│   │   │   ├── core/            # Config, Security, RBAC definitions
│   │   │   ├── db/              # SQLAlchemy session & base
│   │   │   ├── models.py        # Database ORM schemas
│   │   │   └── services/        # Scoring, AI Cascade, Audit, Ingestion
│   │   ├── krhi.db              # SQLite Database (30,771 villages)
│   │   ├── requirements.txt     # Python Dependencies
│   │   └── Dockerfile           # Backend Containerfile
│   └── frontend/                # Next.js 15 React Frontend
│       ├── src/
│       │   ├── components/      # UI Views, Modals, Dashboard, Maps
│       │   ├── lib/             # API client, Mock fallbacks, RBAC types
│       │   └── app/             # App Router pages
│       ├── package.json         # Node Dependencies
│       └── Dockerfile           # Frontend Containerfile
├── .env.example                 # Sanitized Environment Template
├── .gitignore                   # Excludes credentials & databases
├── docker-compose.yml           # Local Multi-Container Orchestration
└── render.yaml                  # 1-Click Render Cloud Deployment Blueprint
```

---

## ⚡ Quickstart Guide

### Prerequisites
- **Python**: 3.11+
- **Node.js**: 20+ (for local frontend build)
- **Docker & Docker Compose**: (Optional, for containerized run)

---

### Option 1: Local Development

#### 1. Setup Environment Variables
Copy `.env.example` to `.env` in the root directory and add your API keys:
```bash
cp .env.example .env
```
Key variables inside `.env`:
```env
GROQ_API_KEY=gsk_your_groq_api_key_here
WATSONX_APIKEY=ApiKey-your_watsonx_key_here
WATSONX_PROJECT_ID=your_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_MODEL_ID=ibm/granite-3-8b-instruct
```

#### 2. Launch Backend (FastAPI)
```bash
cd platform/backend
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
- **Backend API**: `http://localhost:8000`
- **Swagger Docs**: `http://localhost:8000/docs`

#### 3. Launch Frontend (Next.js)
```bash
cd platform/frontend
npm install
npm run dev
```
- **Frontend Dashboard**: `http://localhost:3000`

---

### Option 2: Run via Docker Compose

Make sure you are inside the project root directory (`d:\IBM HACK`):

```bash
# Build and start all services in detached mode
docker compose up --build -d

# View container status
docker compose ps

# View live logs
docker compose logs -f
```

---

### Option 3: Deploy to Cloud via Render (1-Click Blueprint)

1. Push this repository to **GitHub**.
2. Go to [Render Dashboard](https://dashboard.render.com) $\rightarrow$ **New +** $\rightarrow$ **Blueprint**.
3. Connect your repository; Render will automatically detect `render.yaml`.
4. Enter your `GROQ_API_KEY`, `WATSONX_APIKEY`, and `WATSONX_PROJECT_ID` when prompted.
5. Click **Apply**.

---

## 🔐 Default Demo Accounts

| Role | Email | Password | Scope |
| :--- | :--- | :--- | :--- |
| **System Administrator** | `admin@karnataka.demo` | `Demo@2026` | Statewide / Full Control |
| **District Health Officer** | `dho@karnataka.demo` | `Demo@2026` | Davanagere / Bagalkote Scope |
| **MMU Coordinator** | `mmu@karnataka.demo` | `Demo@2026` | MMU Fleet Routing |
| **State Health Admin** | `state@karnataka.demo` | `Demo@2026` | Statewide Analytics |

---

## 🛠 Technology Stack Architecture

### Technology Stack Flowchart

```mermaid
flowchart TD
    subgraph UI ["🎨 1. Frontend Layer (Client Side)"]
        N1["Next.js 15 App Router"]
        N2["React 19 & Tailwind CSS v4"]
        N3["MapLibre GL Geospatial Map"]
        N4["Recharts Analytics & Lucide Icons"]
        N5["TanStack React Query API Client"]
        N1 --- N2 --- N3 --- N4 --- N5
    end

    subgraph API ["⚡ 2. API Gateway & Security Layer"]
        A1["FastAPI ASGI Router (/api/v1)"]
        A2["PyJWT OAuth2 Bearer Auth"]
        A3["RBAC District Scoping Middleware"]
        A4["Pydantic v2 Input/Output Validation"]
        A1 --- A2 --- A3 --- A4
    end

    subgraph CORE ["🧮 3. Business & Scoring Engine"]
        C1["7-Dimension Composite Risk Scorer"]
        C2["Explainable AI (XAI) Factor Extractor"]
        C3["Audit Logging & Provenance Tracker"]
        C1 --- C2 --- C3
    end

    subgraph AI ["🤖 4. Multi-Tier AI Cascade"]
        L1["Tier 1: IBM watsonx.ai (ibm/granite-3-8b-instruct)"]
        L2["Tier 2: Groq Cloud API (groq/compound)"]
        L3["Tier 3: xAI Grok API (grok-beta)"]
        L4["Tier 4: Zero-Failure Deterministic Engine"]
        L1 -->|Fallback| L2
        L2 -->|Fallback| L3
        L3 -->|Fallback| L4
    end

    subgraph DATA ["💾 5. Data Foundation & Storage"]
        D1[("SQLite (krhi.db) / PostgreSQL")]
        D2["SQLAlchemy 2.0 ORM"]
        D3["11-Layer LGD 2026 Village Datasets"]
        D1 --- D2 --- D3
    end

    subgraph INFRA ["🚀 6. Containerization & Cloud Deployment"]
        I1["Docker & Docker Compose"]
        I2["Render Blueprint (render.yaml)"]
        I3["Uvicorn ASGI Server"]
        I1 --- I2 --- I3
    end

    UI <-->|REST API / JSON| API
    API --> CORE
    CORE --> AI
    CORE <--> DATA
    API --> INFRA
```

---

### Tech Stack Component Summary

| Layer | Technologies & Frameworks | Function |
| :--- | :--- | :--- |
| **Frontend** | Next.js 15, React 19, Tailwind CSS v4, MapLibre GL, Recharts | Interactive DHO/MMU dashboards, geospatial village maps, XAI factor modals |
| **API Gateway** | Python 3.11, FastAPI, Pydantic v2, PyJWT | REST API endpoints, JWT authentication, RBAC role scoping |
| **Scoring Engine** | Python, NumPy, Pandas, Scikit-learn | 7-dimension composite risk scoring (0–100) & risk driver extraction |
| **AI Copilot** | IBM watsonx.ai, Groq Cloud API, xAI Grok, Rule Engine | 4-tier LLM fallback cascade for 100% reliable executive briefing generation |
| **Data & ORM** | SQLite (`krhi.db`), PostgreSQL, SQLAlchemy 2.0 | 30,771 villages linked via 6-digit LGD 2026 codes across 11 health domains |
| **DevOps & Cloud** | Docker, Docker Compose, Render Blueprint (`render.yaml`) | Multi-container orchestration & 1-click cloud deployment |

---

## 📜 License & Compliance

Developed for Government of Karnataka Health & Family Welfare Department hackathons and public health decision support. Utilizes official LGD 2026 geographical codes.

