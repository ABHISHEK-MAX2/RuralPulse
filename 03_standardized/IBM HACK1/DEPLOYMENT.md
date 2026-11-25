# Production Deployment Instructions

## Docker Compose Production Architecture

```yaml
version: '3.8'

services:
  db:
    image: postgis/postgis:16-3.4
    environment:
      POSTGRES_DB: karnataka_health
      POSTGRES_USER: health_admin
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
    environment:
      - DATABASE_URL=postgresql://health_admin:${DB_PASSWORD}@db:5432/karnataka_health
      - SECRET_KEY=${JWT_SECRET_KEY}
      - DEMO_MODE=false
    ports:
      - "8000:8000"
    depends_on:
      - db

  frontend:
    build: ./frontend
    environment:
      - NEXT_PUBLIC_API_URL=http://api.health.karnataka.gov.in/api/v1
    ports:
      - "3000:3000"
    depends_on:
      - backend

volumes:
  postgres_data:
```
