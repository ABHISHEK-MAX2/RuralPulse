# Security Controls & Compliance Architecture

## Authentication & Authorization
- **OAuth2 & JWT**: Access tokens carry cryptographic sub, role, and district claims.
- **RBAC Matrix**: Enforced via FastAPI dependency injection middleware (`get_current_user`).

## Audit Logging & Cryptographic Verification
- **SHA-256 Hash Chaining**: Every log entry hashes `{timestamp}|{user_id}|{user_role}|{action}|{resource}|{details}|{prev_hash}`.
- **Tamper Resistance**: Any modification invalidates downstream hashes in the audit chain.

## Data Integrity & Public Protection
- Operational system data (DVDMS medicine stocks, 108 GPS telemetry) display explicit authorization requirement notices rather than fake mock values.
