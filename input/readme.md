# SequelSpeak

[![Backend Tests](https://github.com/cognicai/SequelSpeak/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/cognicai/SequelSpeak/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/cognicai/SequelSpeak/branch/main/graph/badge.svg)](https://codecov.io/gh/cognicai/SequelSpeak)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-009688.svg)](https://fastapi.tiangolo.com)
[![React 19](https://img.shields.io/badge/React-19-61DAFB.svg)](https://react.dev)

> **An advanced agentic, schema-aware Text-to-SQL system** that converts natural language queries into safe, validated PostgreSQL SQL using a **PersonaPlex-inspired architecture**.

## 🎯 Overview

SequelSpeak employs an innovative **Router + Personas** architecture that enforces correctness through structural boundaries rather than relying solely on LLM reasoning. The system implements:

- ✅ **Multi-layer security**: Clerk JWT authentication + PostgreSQL credentials + input validation
- ✅ **85% test coverage**: 38 tests with 100% pass rate across connection services
- ✅ **Production-ready observability**: Structured logging, correlation IDs, health monitoring
- ✅ **Fail-fast validation**: SQLGuardian acts as a mandatory security gate
- ✅ **Async-first design**: FastAPI + psycopg connection pooling with retry logic

### Design Philosophy

> *"Don't make the LLM think harder — force correct behavior through architecture."*

Instead of relying on prompt engineering, SequelSpeak enforces correctness through:
- **Explicit architectural boundaries** (Router + isolated Personas)
- **Contract-based interfaces** (no implicit context passing)
- **Observable state transitions** (correlation IDs, structured logging)

---

## 🏗️ Architecture

### Core Pattern: Router + Personas

```mermaid
graph TB
    User[User Query] --> Router[Router/Orchestrator]
    Router --> SchemaExpert[SchemaExpert<br/>Schema scoping & join paths]
    Router --> ContextRetriever[ContextRetriever<br/>Semantic retrieval pgvector]
    Router --> Clarification[Clarification<br/>Question generation & pause]
    
    SchemaExpert --> SQLWriter[SQLWriter<br/>SQL generation only]
    ContextRetriever --> SQLWriter
    
    SQLWriter --> SQLGuardian[SQLGuardian<br/>Mandatory validation gate]
    SQLGuardian --> Executor[Executor<br/>SQL execution with limits]
    
    Executor --> Explainer[Explainer<br/>Plain English explanations]
    Executor --> Analytics[Analytics<br/>Visualization & bucketing]
    
    User -.->|Feedback| Learning[Learning<br/>Feedback capture]
    
    style SQLGuardian fill:#ff6b6b,stroke:#c92a2a,stroke-width:3px
    style Router fill:#4dabf7,stroke:#1971c2,stroke-width:2px
```

### Key Architectural Invariants

1. Each persona accepts **only explicitly passed inputs** (no implicit context)
2. Any ambiguity must be surfaced to the **Router** (fails fast)
3. Personas have **single responsibility** (no Swiss Army knife agents)
4. **No SQL generated before SQLGuardian approval**
5. All state transitions are **observable and traceable**

### Implementation Status

| Component | Status | Description |
|-----------|--------|-------------|
| Connection Management | ✅ Complete | Async pooling, retry logic, health monitoring |
| Security Layer | ✅ Complete | Clerk JWT + credential masking + rate limiting |
| Health Monitoring | ✅ Complete | Latency tracking, circuit breaker patterns |
| Frontend UI | ✅ Complete | Database connection management interface |
| Router/Orchestrator | 🔄 In Development | Intent classification, persona routing |
| Personas | 🔄 In Development | SchemaExpert, SQLWriter, SQLGuardian, etc. |
| Redis State | 🔄 In Development | Conversation state management |
| pgvector Search | 🔄 In Development | Semantic retrieval for context |

---

## 🚀 Quick Start

### Prerequisites

- **Python** 3.10+ (tested on 3.10, 3.11, 3.12)
- **Node.js** 18+
- **PostgreSQL** (for database connections)
- **Redis** (optional, for conversation state - not yet fully integrated)

### Local Development Setup

```bash
# Clone the repository
git clone https://github.com/cognicai/SequelSpeak.git
cd SequelSpeak

# Backend Setup - Create virtual environment at project root
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install backend dependencies
pip install -r backend/requirements.txt

# Configure backend
cp backend/.env.example backend/.env
# Edit backend/.env with your Clerk credentials and database settings

# Frontend Setup
cd frontend
npm install

# Configure frontend
cp .env.example .env
# Edit frontend/.env with your Clerk publishable key
cd ..

# Start both servers (from project root with venv activated)
./start.sh
```

**Access the application:**
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (Swagger UI)

### Docker Setup (Recommended for Production)

```bash
# Start all services (backend + frontend + Redis)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

The Docker setup includes:
- **Backend**: FastAPI on port 8000
- **Frontend**: Nginx serving React build on port 80
- **Redis**: Conversation state storage on port 6379

See [DOCKER.md](DOCKER.md) for detailed Docker configuration and deployment instructions.

---

## 📁 Project Structure

```
SequelSpeak/
├── .venv/                          # Virtual environment (local dev)
├── start.sh                        # Quick start script (both servers)
├── docker-compose.yml              # Docker orchestration
├── backend/                        # FastAPI backend
│   ├── main.py                     # FastAPI app, middleware, lifespan
│   ├── config.py                   # Pydantic Settings (11 validators)
│   ├── logging_config.py           # Structured JSON logging
│   ├── exceptions.py               # Custom exception hierarchy
│   ├── requirements.txt            # Python dependencies
│   ├── Dockerfile                  # Backend container
│   ├── .env.example                # Environment template
│   ├── api/v1/                     # API endpoints
│   │   ├── connection.py           # POST /test-connection
│   │   ├── health.py               # GET /health
│   │   ├── meta.py                 # GET /meta (version info)
│   │   └── query.py                # Router persona endpoint (planned)
│   ├── services/                   # Business logic
│   │   ├── db_connection_service.py  # Connection testing + retry
│   │   ├── connection_pool.py      # Pool manager (one pool per DB)
│   │   └── conversation_state.py   # Redis state management (planned)
│   ├── schemas/                    # Pydantic models
│   │   ├── connection.py           # Connection request/response
│   │   ├── health.py               # Health check models
│   │   ├── router.py               # Router persona models
│   │   └── errors.py               # Error response models
│   ├── utils/                      # Utilities
│   │   └── security.py             # mask_connection_url()
│   └── tests/                      # 38 tests (91% coverage)
│       ├── test_connection.py      # URL parsing tests (21)
│       ├── test_connection_service.py  # Connection logic (16)
│       └── test_no_credential_leak.py  # Security test (1)
└── frontend/                       # React + TypeScript frontend
    ├── src/
    │   ├── App.tsx                 # Main app component
    │   ├── main.tsx                # Entry point (Clerk provider)
    │   ├── components/
    │   │   ├── ConnectionForm.tsx  # Database connection UI
    │   │   ├── ProfileSelector.tsx # Profile management
    │   │   ├── ConnectionStatusBanner.tsx
    │   │   └── ui/                 # Radix UI components
    │   ├── hooks/
    │   │   └── useConnectionTest.ts  # Connection testing logic
    │   ├── services/
    │   │   └── api.ts              # Backend API client
    │   ├── types/
    │   │   ├── connection.ts       # Connection types
    │   │   └── profile.ts          # Profile types
    │   └── data/
    │       └── sampleProfiles.ts   # Default demo profiles
    ├── Dockerfile                  # Frontend container
    ├── package.json
    └── .env.example                # Frontend config template
```

---

## 🔒 Security Architecture

### Dual Authentication Model

```mermaid
graph LR
    Request[API Request] --> ClerkJWT[1. Clerk JWT<br/>User Identity]
    ClerkJWT --> Protected[Protected Endpoints]
    Protected --> DBCreds[2. PostgreSQL Credentials<br/>Database Access]
    DBCreds --> Database[Target Database]
    
    style ClerkJWT fill:#51cf66,stroke:#2f9e44
    style DBCreds fill:#ffd43b,stroke:#fab005
```

**Layer 1: User Authentication (Clerk JWT)**
- JWT tokens validated using Clerk's JWKS (JSON Web Key Set)
- Managed automatically by `@clerk/clerk-react`
- Protects API access

**Layer 2: Database Authentication (PostgreSQL)**
- Credentials provided with each connection request
- Validated directly against target database
- **Never stored or cached** on server (security by design)
- Each user can connect to any database they have credentials for

### Security Features

| Feature | Implementation | Status |
|---------|----------------|--------|
| **Input Validation** | Pydantic models prevent SQL/command injection | ✅ |
| **Credential Protection** | `mask_connection_url()` removes passwords from logs | ✅ |
| **Rate Limiting** | Per-IP/user limiting (10 req/min default) | ✅ |
| **Circuit Breaker** | 5 consecutive failures → 60s timeout | ✅ |
| **CORS Protection** | Wildcard blocked in production | ✅ |
| **SQL Validation** | SQLGuardian persona (planned) | 🔄 |
| **Query Result Limits** | Max rows/timeout (planned) | 🔄 |
| **Read-Only Enforcement** | Block DROP/DELETE/UPDATE (planned) | 🔄 |

### Threat Model Coverage

✅ **Protected Against:**
- SQL Injection (parameterized queries)
- Command Injection (URL validation)
- Credential Leakage (masking + no storage)
- Rate Limiting Bypass (slowapi)
- CORS Attacks (environment-based validation)
- Replay Attacks (JWT expiration)

---

## 🧪 Testing

### Test Coverage

- **38 total tests** with **100% pass rate**
- **85% code coverage** for services layer
- Automated CI/CD with GitHub Actions + Codecov

```bash
# Activate virtual environment
source .venv/bin/activate

# Run all tests with coverage
pytest backend/tests/ -v --cov=backend/services --cov=backend/api --cov=backend/utils --cov-report=term-missing

# Generate HTML coverage report
pytest backend/tests/ --cov=backend/services --cov=backend/api --cov-report=html
# Open backend/htmlcov/index.html to view detailed report

# Run specific test categories
pytest backend/tests/test_connection.py -v              # URL parsing (21 tests)
pytest backend/tests/test_connection_service.py -v      # Connection logic (16 tests)
pytest backend/tests/test_no_credential_leak.py -v      # Security (1 test)

# Run integration tests (requires Redis)
docker run -d -p 6379:6379 redis:7-alpine
pytest backend/tests/ -v -m integration
```

### Test Categories

| Test Suite | Tests | Focus Area | Coverage |
|------------|-------|------------|----------|
| `test_connection.py` | 21 | URL parsing (valid/invalid URLs, special chars) | URL validation |
| `test_connection_service.py` | 16 | Error classification, retry logic, backoff | Connection logic |
| `test_no_credential_leak.py` | 1 | Credential masking in logs/errors | Security |

---

## ⚙️ Configuration

### Backend Environment Variables

Create `backend/.env` from `backend/.env.example`:

```env
# Application
ENVIRONMENT=development                    # development | staging | production
APP_NAME=SequelSpeak
SECRET_KEY=your-secret-key-min-32-chars   # Required in production

# CORS
ALLOWED_ORIGINS=http://localhost:5173     # Use * only in development

# Database Connection
DB_CONNECTION_TIMEOUT=10                   # Connection timeout (seconds)
DB_POOL_MIN_SIZE=1                         # Min connections in pool
DB_POOL_MAX_SIZE=5                         # Max connections in pool
DB_POOL_TIMEOUT=30                         # Pool acquisition timeout
DB_POOL_MAX_IDLE=600                       # Max idle time (seconds)

# Health Check
HEALTH_CHECK_DB_URL=postgresql://user:pass@host:5432/db
HEALTH_CHECK_TIMEOUT=2                     # Fast health checks

# Retry Logic
CONNECTION_RETRY_MAX=2                     # Max retry attempts
CONNECTION_RETRY_INITIAL_DELAY=1.0         # Initial delay (seconds)

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=10

# Circuit Breaker
CIRCUIT_BREAKER_ENABLED=true
CIRCUIT_BREAKER_FAILURE_THRESHOLD=5
CIRCUIT_BREAKER_TIMEOUT=60

# Authentication (Clerk)
CLERK_SECRET_KEY=sk_test_...
CLERK_PUBLISHABLE_KEY=pk_test_...

# Redis (planned)
REDIS_ENABLED=false
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

**Configuration Validation:**
- 11 Pydantic field validators ensure correctness
- Wildcard CORS (`*`) blocked in production
- Secret key must be 32+ characters in production
- Pool size warnings if exceeding PostgreSQL limits

### Frontend Environment Variables

Create `frontend/.env` from `frontend/.env.example`:

```env
# Backend API
VITE_API_URL=http://localhost:8000

# Clerk Authentication
VITE_CLERK_PUBLISHABLE_KEY=pk_test_...
```

---

## 🛠️ Technology Stack

### Backend

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Web Framework** | FastAPI | 0.104+ | High-performance async API |
| **ASGI Server** | Uvicorn | 0.24+ | Production ASGI server |
| **Database Driver** | psycopg | 3.2.3 | Modern async PostgreSQL adapter |
| **Connection Pool** | psycopg-pool | 3.2.3 | Efficient connection management |
| **Authentication** | Clerk | 1.0+ | JWT validation & user management |
| **Rate Limiting** | slowapi | 0.1.9+ | Request throttling |
| **Testing** | pytest + pytest-asyncio | 7.0+ | Async test framework |
| **Configuration** | Pydantic Settings | 2.0+ | Type-safe config management |

### Frontend

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Framework** | React | 19.2.0 | Latest React with modern hooks |
| **Language** | TypeScript | 5.9.3 | Type safety |
| **Build Tool** | Vite | 7.2.4 | Fast HMR & build |
| **Styling** | Tailwind CSS | 4.1.18 | Latest Tailwind v4 |
| **UI Components** | Radix UI | Latest | Accessible primitives |
| **Authentication** | @clerk/clerk-react | 5.60.0 | Auth hooks & components |
| **Icons** | Lucide React | 0.562.0 | Modern icon set |

### Infrastructure (Planned)

- **State Management**: Redis (conversation state)
- **Vector Search**: pgvector (semantic retrieval)
- **Observability**: OpenTelemetry (traces + metrics)
- **Monitoring**: Grafana + Prometheus

---

## 📊 Key Features

### Connection Management
- ✅ Async connection pooling with lazy initialization
- ✅ Automatic retry with exponential backoff (1s → 2s → 4s)
- ✅ Error classification (retryable vs non-retryable)
- ✅ Circuit breaker for database protection
- ✅ Graceful shutdown (cleanup connection pools)
- ✅ One pool per unique database URL (thread-safe)

### Observability
- ✅ Structured JSON logging in production
- ✅ Correlation IDs for request tracing (X-Correlation-ID header)
- ✅ Connection pool statistics tracking
- ✅ Health check endpoint with latency metrics
- ✅ Automatic credential masking in all logs
- ✅ Request/response timing middleware

### User Experience
- ✅ Profile management (save connection metadata, not passwords)
- ✅ Dual input modes (connection URL or individual fields)
- ✅ Real-time validation with user-friendly error messages
- ✅ SSL mode selection (6 modes supported)
- ✅ Responsive design with Tailwind CSS v4
- ✅ Auto-save profiles to LocalStorage (metadata only)

---

## 📡 API Endpoints

### Currently Implemented

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| / | GET | No | Root health check |
| /api/v1/health | GET | No | Database connectivity + latency |
| /api/v1/meta | GET | No | API version & operational status |
| /api/v1/utils/test-connection | POST | Yes | Test PostgreSQL connection with retry |

### Planned (Router Integration)

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| /api/v1/query | POST | Yes | NL → SQL pipeline (Router orchestration) |
| /api/v1/conversations/{id} | GET | Yes | Retrieve conversation state from Redis |
| /api/v1/clarify | POST | Yes | Submit clarification responses |

---

## 🚢 Deployment

### Docker Deployment (Recommended)

The project includes a complete Docker setup with separate containers for backend, frontend, and Redis:

```bash
# Production deployment
docker-compose -f docker-compose.yml up -d

# Development with hot reload
docker-compose -f docker-compose.dev.yml up

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Rebuild after changes
docker-compose build --no-cache

# Stop and remove containers
docker-compose down -v
```

See [DOCKER.md](DOCKER.md) for:
- Detailed Docker configuration
- Multi-stage build optimizations
- Environment variable management
- Production deployment best practices
- Health check configuration

### Manual Deployment

See individual README files for deployment details:
- **Backend**: [backend/README.md](backend/README.md)
- **Frontend**: [frontend/README.md](frontend/README.md)

---

## 🏃 Development Workflow

### Backend Development

```bash
# Activate virtual environment
source .venv/bin/activate

# Start backend with auto-reload
cd backend
uvicorn main:app --reload --port 8000

# Run tests with real-time feedback
pytest --looponfail

# Run specific test file
pytest tests/test_connection_service.py -v -s

# Generate coverage report
pytest --cov=services --cov=api --cov-report=html
```

### Frontend Development

```bash
# Start frontend dev server
cd frontend
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Type checking
npm run type-check

# Linting
npm run lint
```

### Full Stack Development

```bash
# From project root with venv activated
./start.sh

# Or manually:
# Terminal 1 - Backend
cd backend && uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend && npm run dev
```

---

## 📚 Documentation

- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Alternative API Docs**: http://localhost:8000/redoc (ReDoc)
- **Backend Details**: [backend/README.md](backend/README.md)
- **Frontend Details**: [frontend/README.md](frontend/README.md)
- **Docker Guide**: [DOCKER.md](DOCKER.md)
- **Codebase Analysis**: [temp/sequelspeak_codebase_analysis.md](temp/sequelspeak_codebase_analysis.md)

---

## 🎯 Roadmap

### Phase 1: Core Infrastructure ✅ (Complete)
- [x] Connection management with pooling
- [x] Security layer (Clerk + credential masking)
- [x] Health monitoring & logging
- [x] Frontend UI for connections
- [x] 85% test coverage
- [x] Docker configuration

### Phase 2: Persona Pipeline 🔄 (In Progress)
- [ ] Router/Orchestrator implementation
- [ ] SchemaExpert persona (table/column selection)
- [ ] SQLWriter persona (SQL generation)
- [ ] SQLGuardian persona (validation gate)
- [ ] Executor persona (safe query execution)
- [ ] Explainer persona (plain English explanations)

### Phase 3: Advanced Features 📋 (Planned)
- [ ] Redis conversation state management
- [ ] Clarification persona (ambiguity handling)
- [ ] ContextRetriever with pgvector
- [ ] Analytics persona (visualization)
- [ ] Learning persona (feedback capture)
- [ ] Frontend query interface

### Phase 4: Production Hardening 📋 (Planned)
- [ ] OpenTelemetry integration
- [ ] Grafana dashboards
- [ ] Database migrations (Alembic)
- [ ] CI/CD pipeline enhancements
- [ ] Load testing & optimization
- [ ] Comprehensive documentation

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the repository** and create a feature branch
2. **Write tests** for new functionality (maintain 85%+ coverage)
3. **Follow code style**: Backend (Black), Frontend (ESLint + Prettier)
4. **Update documentation** for significant changes
5. **Submit a pull request** with a clear description

### Development Setup for Contributors

```bash
# Install pre-commit hooks (recommended)
pip install pre-commit
pre-commit install

# Run tests before committing
pytest backend/tests/ -v

# Check code formatting
black backend/ --check
```

---

## 📝 License

This project is licensed under the MIT License.

The MIT License is a permissive open-source license that allows anyone to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software.

### What this means

- ✅ Commercial use is allowed  
- ✅ Modification is allowed  
- ✅ Distribution is allowed  
- ✅ Private use is allowed  

### Conditions

- The original copyright notice and license text must be included in all copies or substantial portions of the software.

### Limitation of Liability

This software is provided "as is", without warranty of any kind, express or implied. The authors are not liable for any claims, damages, or other liability arising from its use.

For full details, see the [LICENSE](LICENSE) file in this repository.

---

## 🙏 Acknowledgments

- Architecture inspired by **PersonaPlex** pattern
- Built with **FastAPI** and **React**
- Authentication powered by **Clerk**
- UI components from **Radix UI**

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/cognicai/SequelSpeak/issues)
- **Documentation**: See `/docs` directory
- **API Docs**: http://localhost:8000/docs (when running locally)

---

## 🔍 Project Status

**Current Version**: 0.1.0 (Alpha)  
**Status**: 🟡 Active Development  
**Test Coverage**: [![codecov](https://codecov.io/gh/cognicai/SequelSpeak/branch/main/graph/badge.svg)](https://codecov.io/gh/cognicai/SequelSpeak)  
**Tests Passing**: 38/38 (100%)

**Production Readiness**:
- ✅ Connection Management: Production-ready
- ✅ Security Layer: Production-ready
- ✅ Health Monitoring: Production-ready
- 🔄 Persona Pipeline: In development
- 🔄 Query Interface: In development

---

<p align="center">
  <strong>Built with ❤️ by the CognicAI team</strong>
</p>
