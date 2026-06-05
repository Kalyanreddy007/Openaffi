# Database Schema

## Overview

OpenAffi uses PostgreSQL as its primary database. All tables are managed through SQLAlchemy ORM.

## Tables

### Users

Stores user account information and authentication credentials.

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Fields:**
- `id` - Primary key, auto-increment
- `name` - User full name
- `email` - Unique email address
- `password_hash` - Bcrypt hashed password
- `created_at` - Account creation timestamp

### Companies

Stores company information and business details.

```sql
CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    company_name VARCHAR(255) NOT NULL,
    website VARCHAR(255),
    industry VARCHAR(255),
    employee_count INTEGER,
    country VARCHAR(255),
    linkedin_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Fields:**
- `id` - Primary key, auto-increment
- `user_id` - Foreign key to users
- `company_name` - Company name (indexed)
- `website` - Company website URL
- `industry` - Industry classification (indexed)
- `employee_count` - Number of employees
- `country` - Company location (indexed)
- `linkedin_url` - LinkedIn company profile URL
- `created_at` - Creation timestamp

**Indexes:**
- `company_name` - For full-text search
- `industry` - For filtering
- `country` - For geographic filtering

### Contacts

Stores individual contact information linked to companies.

```sql
CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    company_id INTEGER NOT NULL REFERENCES companies(id),
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    title VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(20),
    linkedin_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Fields:**
- `id` - Primary key, auto-increment
- `user_id` - Foreign key to users
- `company_id` - Foreign key to companies
- `first_name` - Contact first name (indexed)
- `last_name` - Contact last name (indexed)
- `title` - Job title/position (indexed)
- `email` - Email address (unique, indexed)
- `phone` - Phone number
- `linkedin_url` - LinkedIn profile URL
- `created_at` - Creation timestamp

**Indexes:**
- `first_name`, `last_name` - For name-based search
- `email` - Unique constraint
- `title` - For job title filtering

### Lead Scores

Stores calculated lead scores for company-contact pairs.

```sql
CREATE TABLE lead_scores (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    company_id INTEGER NOT NULL REFERENCES companies(id),
    contact_id INTEGER NOT NULL REFERENCES contacts(id),
    score FLOAT NOT NULL,
    reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Fields:**
- `id` - Primary key, auto-increment
- `user_id` - Foreign key to users
- `company_id` - Foreign key to companies
- `contact_id` - Foreign key to contacts
- `score` - Lead score (0-100)
- `reason` - Explanation for the score
- `created_at` - Calculation timestamp

## Relationships

### One-to-Many
- User → Companies (one user has many companies)
- User → Contacts (one user has many contacts)
- User → LeadScores (one user has many lead scores)
- Company → Contacts (one company has many contacts)
- Company → LeadScores (one company has many lead scores)
- Contact → LeadScores (one contact has many lead scores)

### Cascading Deletes
- Deleting a user cascades to all related companies, contacts, and lead scores
- Deleting a company cascades to related contacts and lead scores
- Deleting a contact cascades to related lead scores

## Migrations

### Running Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migrations
alembic downgrade -1
```

## Backup and Recovery

### Backup Database

```bash
# PostgreSQL dump
pg_dump postgresql://user:password@localhost/openaffi > backup.sql

# Using Docker
docker-compose exec db pg_dump -U openaffi openaffi > backup.sql
```

### Restore Database

```bash
# From dump file
psql postgresql://user:password@localhost/openaffi < backup.sql

# Using Docker
docker-compose exec -T db psql -U openaffi openaffi < backup.sql
```

## Performance Optimization

### Indexes
Key fields are indexed for optimal query performance:
- `companies.company_name` - For full-text search
- `companies.industry` - For filtering
- `contacts.first_name, last_name` - For name search
- `contacts.email` - Unique index
- `contacts.title` - For job title filtering

### Query Optimization
- Use pagination (limit, offset)
- Filter before full table scans
- Use JOINs for related data
- Cache frequently accessed data

## Data Types

| Python | PostgreSQL | Usage |
|--------|-----------|-------|
| int | SERIAL | Auto-increment IDs |
| str | VARCHAR | Text fields |
| float | FLOAT | Lead scores |
| datetime | TIMESTAMP | Timestamps |
| bool | BOOLEAN | Boolean flags |
