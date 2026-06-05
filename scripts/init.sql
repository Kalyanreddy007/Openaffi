-- Initialize database for OpenAffi
-- This script creates the initial schema and can be run with psql

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- The tables will be created by SQLAlchemy ORM on application startup
-- This file is for reference and can be used for manual setup if needed
