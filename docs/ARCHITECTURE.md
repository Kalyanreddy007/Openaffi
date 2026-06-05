# Architecture Overview

## System Design

OpenAffi is built with a modern, scalable architecture using microservices principles.

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Next.js)                       │
│              React Components + TailwindCSS                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTP/REST API
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  Backend (FastAPI)                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              API Routes                              │   │
│  │  • Auth (register, login, refresh)                   │   │
│  │  • Companies (CRUD, search)                          │   │
│  │  • Contacts (CRUD, search)                           │   │
│  │  • Lead Scoring (calculate, list)                    │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Business Logic                          │   │
│  │  • Lead Scoring Service                              │   │
│  │  • AI Agents (Research, Enrichment, Personalization) │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Data Access Layer                       │   │
│  │  • SQLAlchemy ORM                                    │   │
│  │  • Database Models                                   │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ SQL
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  PostgreSQL Database                         │
│  • Users | Companies | Contacts | LeadScores               │
└─────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Frontend
- **Framework**: Next.js 15 (React 18)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: Shadcn/ui + Radix UI
- **State Management**: Zustand
- **Data Fetching**: React Query (TanStack Query)
- **HTTP Client**: Axios
- **Theme**: next-themes (light/dark mode)

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **ASGI Server**: Uvicorn
- **ORM**: SQLAlchemy
- **Database**: PostgreSQL
- **Authentication**: JWT (Python-Jose)
- **Password Hashing**: Bcrypt
- **Validation**: Pydantic
- **API Documentation**: Swagger/OpenAPI

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Database**: PostgreSQL 15
- **Database Management**: PgAdmin (optional)

## Data Flow

### Authentication Flow

```
1. User Registration
   Frontend → POST /api/auth/register → Backend → PostgreSQL
   ✓ Validate email
   ✓ Hash password
   ✓ Create user

2. User Login
   Frontend → POST /api/auth/login → Backend → PostgreSQL
   ✓ Verify credentials
   ✓ Generate JWT token
   ← Return access token

3. Authenticated Request
   Frontend → GET /api/companies
   + Authorization: Bearer {JWT token}
   → Backend (verify token) → PostgreSQL
```

### Company Data Flow

```
1. Create Company
   Frontend → POST /api/companies + JWT
   → Validate user authentication
   → Validate input data
   → Save to PostgreSQL
   ← Return created company

2. List Companies
   Frontend → GET /api/companies?skip=0&limit=10 + JWT
   → Verify JWT token
   → Query companies for user
   → Apply pagination
   ← Return companies list

3. Search Companies
   Frontend → GET /api/companies/search?query=tech + JWT
   → Parse search query
   → Execute full-text search
   ← Return matching companies
```

### Lead Scoring Flow

```
1. Calculate Lead Score
   Frontend → POST /api/leads/score + JWT
   Body: { company_id, contact_id }
   
   → Verify user owns company and contact
   → Call LeadScoringService.calculate_lead_score()
   → Evaluate scoring factors:
      • Company size (employee count)
      • Industry match
      • Decision-maker indicators (title)
      • Contact information completeness
      • LinkedIn availability
   → Generate score (0-100)
   → Save to database
   ← Return lead score with reason
```

## Security Architecture

### Authentication & Authorization

```
1. Password Security
   • Bcrypt hashing with salt
   • Minimum 8 characters required
   • Never stored in plain text

2. JWT Tokens
   • 30-minute expiration
   • Signed with HS256 algorithm
   • Contains user_id claim
   • Refresh token support (future)

3. CORS Protection
   • Whitelist specific origins
   • Allow credentials
   • Control HTTP methods

4. Data Isolation
   • All queries filtered by user_id
   • No cross-user data access
   • Database-level constraints
```

## API Design

### RESTful Principles
- **GET** - Retrieve resources
- **POST** - Create resources
- **PUT** - Update resources
- **DELETE** - Remove resources
- **Pagination** - skip/limit parameters
- **Filtering** - Query parameters
- **Sorting** - Order by parameters

### Response Format

```json
{
  "items": [{ /* resource */ }],
  "total": 100,
  "skip": 0,
  "limit": 10
}
```

### Error Handling

```json
{
  "detail": "Error message",
  "status_code": 400,
  "errors": [
    {
      "field": "email",
      "message": "Invalid email format"
    }
  ]
}
```

## Scalability Considerations

### Horizontal Scaling
- Stateless API servers (FastAPI)
- Load balancer (Nginx/HAProxy)
- Multiple backend instances
- Shared PostgreSQL database

### Vertical Scaling
- Database indexing
- Query optimization
- Connection pooling
- Caching layer (Redis)

### Future Improvements
- GraphQL API
- WebSocket real-time updates
- Message queue (RabbitMQ/Celery)
- Caching layer (Redis)
- Search engine (Elasticsearch)
- ML models for lead scoring

## Monitoring & Logging

### Backend Logging
- Application logs (debug, info, warning, error)
- Request/response logging
- Database query logging
- Error tracking and reporting

### Frontend Monitoring
- Error tracking (Sentry)
- Performance monitoring
- User analytics
- Debug toolbar (development only)

## Performance Optimization

### Database
- Indexes on frequently searched columns
- Connection pooling
- Query optimization
- Lazy loading relationships

### Frontend
- Code splitting
- Image optimization
- Lazy component loading
- Request deduplication (React Query)
- Browser caching

### API
- Response compression (gzip)
- Pagination for large datasets
- Field filtering
- Caching headers
