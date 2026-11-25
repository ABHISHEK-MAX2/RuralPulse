# Automated & Manual Testing Strategy

## Backend Unit & Integration Tests (Pytest)
```bash
cd backend
python -m pytest tests/ -v
```

### Test Coverage
- `test_scoring.py`: 10-dimensional vulnerability formula & SHAP feature attribution verification.
- `test_api.py`: FastAPI endpoint tests (`/health`, `/geography/districts`, `/geography/villages`, `/vulnerability/kpis`, `/auth/login`).

---

## Frontend Build Verification
```bash
cd frontend
npm run build
```
Validates TypeScript compilation, Next.js page generation, and bundle optimization.
