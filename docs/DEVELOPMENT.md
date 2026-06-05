# Development Guide

## Project Structure

### Backend (`backend/`)
- `app/` - Main application code
  - `main.py` - FastAPI application entry point
  - `config.py` - Configuration and settings
  - `database.py` - Database connection and session management
  - `models.py` - SQLAlchemy ORM models
  - `schemas.py` - Pydantic validation schemas
  - `routers/` - API route handlers
    - `auth.py` - Authentication endpoints
    - `companies.py` - Company CRUD endpoints
    - `contacts.py` - Contact CRUD endpoints
    - `leads.py` - Lead scoring endpoints
    - `dependencies.py` - Dependency injection
  - `services/` - Business logic
    - `lead_scorer.py` - Lead scoring algorithm
  - `agents/` - AI agents (placeholder)
    - `ai_agents.py` - Placeholder AI implementations
  - `utils/` - Utility functions
    - `auth.py` - JWT and password utilities
    - `helpers.py` - General helpers
- `tests/` - Unit tests
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container configuration

### Frontend (`frontend/`)
- `app/` - Next.js app directory
  - `layout.tsx` - Root layout
  - `page.tsx` - Home page
  - `globals.css` - Global styles
  - `providers.tsx` - React providers
- `components/` - Reusable React components
- `lib/` - Utility functions
  - `api.ts` - Axios API client
  - `auth.ts` - Authentication functions
  - `store.ts` - Zustand state management
- `public/` - Static assets
- `package.json` - npm dependencies
- `tsconfig.json` - TypeScript configuration
- `Dockerfile` - Container configuration

## Development Workflow

### 1. Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run migrations
alembic upgrade head

# Seed database
python scripts/seed_data.py

# Start development server
uvicorn app.main:app --reload
```

### 2. Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local
cp .env.example .env.local

# Start development server
npm run dev
```

### 3. Running with Docker Compose

```bash
# From root directory
docker-compose up -d

# View logs
docker-compose logs -f

# Run migrations
docker-compose exec backend alembic upgrade head

# Seed data
docker-compose exec backend python scripts/seed_data.py
```

## Code Style

### Python
- Follow PEP 8
- Use type hints
- Use docstrings for all functions
- Run linting: `pylint app/`
- Format with: `black app/`

### TypeScript/React
- Use strict TypeScript
- Use functional components
- Use React hooks
- Follow Prettier formatting

## Testing

### Backend Tests
```bash
cd backend
pytest
pytest --cov=app  # With coverage
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Adding New Features

### Backend
1. Create model in `app/models.py`
2. Create schema in `app/schemas.py`
3. Create router in `app/routers/`
4. Include router in `app/main.py`
5. Add tests in `tests/`

### Frontend
1. Create API functions in `lib/api.ts`
2. Create components in `components/`
3. Create pages in `app/`
4. Use React Query for data fetching
5. Use Zustand for state management

## Environment Variables

### Backend
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT secret key
- `ENVIRONMENT` - development/production
- `DEBUG` - Enable debug mode

### Frontend
- `NEXT_PUBLIC_API_URL` - Backend API URL
- `NEXT_PUBLIC_APP_NAME` - Application name

## Deployment

### Production Checklist
- [ ] Set `ENVIRONMENT=production`
- [ ] Generate strong `SECRET_KEY`
- [ ] Update `ALLOWED_ORIGINS` CORS settings
- [ ] Configure database backups
- [ ] Set up monitoring and logging
- [ ] Configure SSL/TLS certificates
- [ ] Run database migrations
- [ ] Test all endpoints
- [ ] Set up CI/CD pipeline

## Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL is running
docker-compose ps

# View database logs
docker-compose logs db

# Connect to database
psql postgresql://openaffi:openaffi_password@localhost/openaffi
```

### Backend Issues
```bash
# Check dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Check logs
unicorn app.main:app --log-level debug
```

### Frontend Issues
```bash
# Clear cache
rm -rf .next

# Reinstall dependencies
rm -rf node_modules
npm install

# Check logs
npm run dev
```
