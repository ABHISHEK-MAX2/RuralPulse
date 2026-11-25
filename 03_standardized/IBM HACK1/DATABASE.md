# Database Schema & Entity Relationship Specification

## Schema Structure (PostgreSQL / PostGIS & SQLite)

### Core Tables

1. `lgd_villages`
   - `village_code` (INT PRIMARY KEY)
   - `village_name` (VARCHAR)
   - `state_code` (INT)
   - `district_code` (INT)
   - `district_name` (VARCHAR)
   - `taluk_code` (INT)
   - `taluk_name` (VARCHAR)
   - `latitude`, `longitude` (FLOAT)

2. `vulnerability_scores`
   - `village_code` (INT PRIMARY KEY, FK -> `lgd_villages.village_code`)
   - `score` (FLOAT 0-100)
   - `risk_level` (VARCHAR: CRITICAL, HIGH, MEDIUM, LOW)
   - `predicted_score_7d` (FLOAT)
   - 10 Subscores (`healthcare_access_subscore`, `maternal_child_subscore`, etc.)
   - `shap_json` (TEXT)
   - `top_contributing_factors_json` (TEXT)

3. `ai_recommendations`
   - `id` (SERIAL PRIMARY KEY)
   - `village_code` (INT FK -> `lgd_villages.village_code`)
   - `action` (VARCHAR)
   - `reason` (TEXT)
   - `priority` (VARCHAR: CRITICAL, HIGH, MEDIUM, LOW)
   - `status` (VARCHAR: PENDING_REVIEW, APPROVED, REJECTED, MODIFIED)
   - `approved_by` (VARCHAR)
   - `approved_at` (TIMESTAMP)

4. `audit_logs`
   - `id` (SERIAL PRIMARY KEY)
   - `timestamp` (TIMESTAMP)
   - `user_id` (VARCHAR)
   - `user_role` (VARCHAR)
   - `action` (VARCHAR)
   - `resource` (VARCHAR)
   - `prev_hash` (VARCHAR)
   - `log_hash` (VARCHAR SHA-256)
