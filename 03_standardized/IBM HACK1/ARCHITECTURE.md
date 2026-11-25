# Architecture & Technical Design Document

## System Architecture

```
[ Frontend: Next.js 14 + React 18 + Tailwind ]
                       │ (HTTP / JSON REST)
                       ▼
   [ Backend API: FastAPI Async Web Services ]
      ├── Auth Router & JWT Handler
      ├── Geography & Village Intelligence Router
      ├── AI Vulnerability Scoring & SHAP Explainer Engine
      ├── Human-in-the-Loop Recommendation Engine
      ├── MMU Fleet & Mission Dispatch Engine
      └── Cryptographic SHA-256 Audit Logger
                       │
                       ▼
    [ Database: PostgreSQL / PostGIS (or SQLite) ]
```

## Data Provenance Architecture
Every dataset record is explicitly classified into one of 5 provenance tiers:
1. `REAL_SOURCE_DATA`
2. `DERIVED_DATA`
3. `MODEL_OUTPUT`
4. `NOT_PUBLICLY_AVAILABLE`
5. `SYNTHETIC_DEMO_DATA`

Protected operational datasets (e.g. DVDMS drug stock, real-time MMU GPS telemetry) display:
`"Not publicly available / Authorized government access required"` in Live mode.
