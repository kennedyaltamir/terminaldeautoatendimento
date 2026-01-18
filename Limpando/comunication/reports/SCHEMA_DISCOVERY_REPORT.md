# Database Schema Discovery Report

## Overview
This report represents the **single source of truth** of the current database schema.

## Tables Analysis

### Table: `alembic_version`
**Columns:**
- `version_num` : character varying
- Has `company_id`: **False**
- RLS Enabled: **False**
## ERROR
`(psycopg2.errors.SyntaxError) syntax error at or near ":"
LINE 4:                 WHERE polrelid = :table::regclass;
                                         ^

[SQL: 
                SELECT polname
                FROM pg_policy
                WHERE polrelid = :table::regclass;
            ]
(Background on this error at: https://sqlalche.me/e/20/f405)`