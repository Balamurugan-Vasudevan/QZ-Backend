# Quiz Builder API

A modern, async FastAPI backend for creating, managing, and publishing quizzes. Built with MongoDB for scalable data storage and JWT authentication for secure user management.

## Features

- ✅ **User Authentication** - JWT-based auth with bcrypt password hashing
- ✅ **Quiz Management** - Full CRUD operations for quiz creation and management
- ✅ **Draft & Publish Workflow** - Save quizzes as drafts before publishing
- ✅ **Question Management** - Support for multiple-choice questions with correct answer tracking
- ✅ **Access Control** - Private/Public visibility with permission checks
- ✅ **Quiz Metadata** - Time limits, passing scores, max attempts configuration
- ✅ **Async Operations** - High-performance async/await throughout
- ✅ **CORS Enabled** - Ready for frontend integration

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | FastAPI 0.136.3+ |
| **Database** | MongoDB Atlas with Motor (async driver) |
| **Authentication** | JWT (python-jose) + Bcrypt |
| **Validation** | Pydantic v2 |
| **Server** | Uvicorn |
| **Python** | 3.13+ |

## Prerequisites

- Python 3.13 or higher
- MongoDB Atlas account with connection string
- Virtual environment setup

## Installation

### 1. Clone and Navigate
```bash
cd student_maintanence_system_backend
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
```

### 3. Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

## Environment Setup

Create a `.env` file in the `app/` directory with the following variables:

```env
# MongoDB Connection
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/database?retryWrites=true&w=majority
DB_NAME=quizapp

# JWT Configuration
JWT_SECRET=your_secret_key_here
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=10080
```

### Environment Variables Explained

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGO_URI` | MongoDB Atlas connection string | Required |
| `DB_NAME` | Database name | `quizapp` |
| `JWT_SECRET` | Secret key for JWT encoding | Required |
| `JWT_ALGORITHM` | Algorithm for JWT | `HS256` |
| `JWT_EXPIRE_MINUTES` | Token expiration time in minutes | `10080` (7 days) |

## Running the Application

### Development Mode
```bash
uvicorn app.main:app --reload
```

The API will start on `http://localhost:8000`

API documentation will be available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Production Mode
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### Authentication Routes

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "name": "John Doe",
  "email": "john@example.com",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Login User
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

#### Get Current User
```http
GET /api/auth/me
Authorization: Bearer {token}
```

---

### Quiz Routes

All quiz endpoints require authentication (Bearer token in Authorization header)

#### List User's Quizzes
```http
GET /api/quiz
Authorization: Bearer {token}
```

Returns quizzes sorted by creation date (newest first)

#### Create Quiz
```http
POST /api/quiz
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Python Basics",
  "description": "Test your Python knowledge",
  "category": "Programming",
  "difficulty": "Beginner",
  "visibility": "public",
  "time_limit": 30,
  "passing_score": 70,
  "max_attempts": 3,
  "questions": [
    {
      "question": "What is Python?",
      "options": [
        {
          "text": "A programming language",
          "isCorrect": true
        },
        {
          "text": "A type of snake",
          "isCorrect": false
        }
      ]
    }
  ]
}
```

#### Get Single Quiz
```http
GET /api/quiz/{quiz_id}
Authorization: Bearer {token}
```

**Note:** Public quizzes can be accessed by anyone; private quizzes only by the owner

#### Update Quiz
```http
PUT /api/quiz/{quiz_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Updated Title",
  "difficulty": "Intermediate"
}
```

#### Delete Quiz
```http
DELETE /api/quiz/{quiz_id}
Authorization: Bearer {token}
```

#### Publish Quiz
```http
PATCH /api/quiz/{quiz_id}/publish
Authorization: Bearer {token}
```

Changes quiz status from "draft" to "published"

---

## Project Structure

```
app/
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration and environment settings
├── database.py            # MongoDB connection management
│
├── models/                # Pydantic data models
│   ├── user.py           # User data model
│   └── quiz.py           # Quiz data model
│
├── schemas/               # Request/response validation schemas
│   ├── user.py           # User schemas (register, login, response)
│   └── quiz.py           # Quiz schemas (create, update, response)
│
├── routes/                # API route definitions
│   ├── auth.py           # Authentication endpoints
│   └── quiz.py           # Quiz endpoints
│
├── controllers/           # Business logic
│   ├── auth.py           # Auth logic (register, login, password hashing)
│   └── quiz.py           # Quiz CRUD operations
│
└── middleware/
    └── auth.py           # JWT token verification
```

## Data Models

### User
```json
{
  "_id": "507f1f77bcf86cd799439011",
  "name": "John Doe",
  "email": "john@example.com",
  "password": "$2b$12$...",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Quiz
```json
{
  "_id": "507f1f77bcf86cd799439012",
  "user_id": "507f1f77bcf86cd799439011",
  "title": "Python Basics",
  "description": "Test your Python knowledge",
  "category": "Programming",
  "difficulty": "Beginner",
  "visibility": "public",
  "status": "published",
  "time_limit": 30,
  "passing_score": 70,
  "max_attempts": 3,
  "questions": [
    {
      "question": "What is Python?",
      "options": [
        {
          "text": "A programming language",
          "isCorrect": true
        },
        {
          "text": "A type of snake",
          "isCorrect": false
        }
      ]
    }
  ],
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Register/Login** → Receive JWT token
2. **Subsequent Requests** → Include token in Authorization header
3. **Token Format**: `Authorization: Bearer {token}`
4. **Token Expiration**: 10,080 minutes (7 days) by default

### How it Works
- Passwords are hashed using bcrypt before storage
- JWT tokens are signed with a secret key
- Tokens include user ID and expiration time
- Each protected endpoint verifies the token before processing

## CORS Configuration

The API is configured to accept requests from:
- `http://localhost:5173` (React development server)

To modify CORS settings, edit `app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Error Handling

The API returns appropriate HTTP status codes:

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad request (validation error) |
| 401 | Unauthorized (invalid token) |
| 403 | Forbidden (access denied) |
| 404 | Not found (quiz/user doesn't exist) |
| 500 | Server error |

## Development

### Run with Auto-Reload
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Access Interactive Docs
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Dependencies

See `pyproject.toml` for the complete list:
- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **Motor** - Async MongoDB driver
- **Pydantic** - Data validation
- **python-jose** - JWT handling
- **bcrypt** - Password hashing
- **python-dotenv** - Environment variable management
- **certifi** - SSL/TLS certificates

## License

This project is proprietary.

## Support

For issues or questions, please refer to the project documentation or contact the development team.
