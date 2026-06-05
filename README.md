# OpenAffi

**AI-powered B2B Intelligence and Decision-Maker Discovery Platform**

OpenAffi helps sales teams, recruiters, agencies, and consultants find companies, identify decision-makers, enrich records, score leads, and automate prospecting using advanced AI agents and data intelligence.

## 🎯 Features

- **Company Intelligence**: Search and analyze companies with enriched data
- **Contact Discovery**: Identify and manage decision-makers and key contacts
- **Lead Scoring**: AI-powered lead qualification and scoring
- **Email Personalization**: Generate personalized outreach emails
- **Contact Enrichment**: Automatically enrich contact records with additional data
- **Advanced Search**: Filter and search companies and contacts
- **Pagination**: Efficient data handling for large datasets
- **JWT Authentication**: Secure user authentication
- **Real-time Analytics**: Dashboard with key metrics

## 🛠 Tech Stack

### Frontend
- **Next.js 15** - React framework
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first CSS
- **Shadcn UI** - High-quality React components
- **TanStack Query** - Data fetching and caching

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation
- **JWT** - Authentication

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **PostgreSQL** - Primary database

## 📁 Project Structure

```
openaffi/
├── frontend/                 # Next.js application
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── public/
│   ├── package.json
│   └── tsconfig.json
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── routers/         # API endpoints
│   │   ├── services/        # Business logic
│   │   ├── agents/          # AI agents
│   │   ├── middleware/
│   │   ├── utils/
│   │   └── main.py
│   ├── tests/               # Unit tests
│   ├── requirements.txt
│   └── Dockerfile
├── ai/                       # AI agents and services
│   ├── agents/
│   └── services/
├── data/                     # Seed data and migrations
├── scripts/                  # Utility scripts
├── docs/                     # Documentation
├── docker-compose.yml        # Docker Compose configuration
└── .gitignore               # Git ignore rules
```

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for frontend development)

### Quick Start with Docker Compose

```bash
# Clone the repository
git clone https://github.com/Kalyanreddy007/OpenAffi.git
cd openaffi

# Start all services
docker-compose up -d

# Run database migrations
docker-compose exec backend alembic upgrade head

# Load seed data
docker-compose exec backend python scripts/seed_data.py
```

Access the application:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

### Local Development Setup

#### Backend Setup

```bash
# Navigate to backend
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

#### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.example .env.local

# Run development server
npm run dev
```

## 📚 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh JWT token

### Companies
- `GET /api/companies` - List companies (with pagination)
- `GET /api/companies/{id}` - Get company details
- `POST /api/companies` - Create new company
- `PUT /api/companies/{id}` - Update company
- `DELETE /api/companies/{id}` - Delete company
- `GET /api/companies/search` - Search companies

### Contacts
- `GET /api/contacts` - List contacts (with pagination)
- `GET /api/contacts/{id}` - Get contact details
- `POST /api/contacts` - Create new contact
- `PUT /api/contacts/{id}` - Update contact
- `DELETE /api/contacts/{id}` - Delete contact
- `GET /api/contacts/search` - Search contacts

### Lead Scoring
- `GET /api/leads/scores` - Get lead scores
- `POST /api/leads/score` - Calculate lead score
- `GET /api/leads/scores/{id}` - Get specific lead score

### AI Agents
- `POST /api/ai/research/company` - Research company
- `POST /api/ai/enrich/contact` - Enrich contact data
- `POST /api/ai/personalize/email` - Personalize email

## 🔐 Environment Variables

Create `.env` file in the root directory:

```env
# Backend
DATABASE_URL=postgresql://user:password@db:5432/openaffi
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🧪 Testing

### Run Backend Tests

```bash
cd backend
pytest
pytest --cov=app tests/  # With coverage
```

### Run Frontend Tests

```bash
cd frontend
npm test
```

## 📖 Documentation

- [Installation Guide](./docs/INSTALLATION.md)
- [Development Guide](./docs/DEVELOPMENT.md)
- [API Documentation](./docs/API.md)
- [Database Schema](./docs/DATABASE.md)
- [Architecture](./docs/ARCHITECTURE.md)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎉 Support

For support, email support@openaffi.com or open an issue in the repository.

---

**Built with ❤️ for B2B sales and recruitment teams**
