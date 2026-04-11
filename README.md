# 🚀 FastAPI Project – Scalable CSV Processing & User Management System

## 📌 Overview

This project is a **modular FastAPI backend** designed with clean architecture principles.
It supports:

* 📂 Large CSV file upload (streaming)
* ⚡ Efficient bulk user insertion
* 🔐 Authentication & security
* 🧱 Layered architecture (API → Service → Repository → DB)

---

## 🏗️ Project Structure

```text
app/
├── api/                # API layer (routes)
│   ├── endpoints/      # Route definitions
│   ├── app.py          # FastAPI app instance
│   └── deps.py         # Dependencies (DB, auth, etc.)
│
├── core/               # Core configuration
│   ├── config.py       # Settings
│   ├── security.py     # Auth logic
│   ├── exceptions.py   # Custom exceptions
│   └── status.py       # Status codes/constants
│
├── infrastructure/     # External integrations
│   ├── database/       # DB connection/session
│   └── external/       # Third-party services
│
├── models/             # SQLAlchemy models
│   └── user_model.py
│
├── repositories/       # DB access layer
│   └── user_repository.py
│
├── schemas/            # Request/Response models
│   ├── user.py
│   ├── ResponseModel.py
│   └── PaginatedData.py
│
├── services/           # Business logic layer
│   ├── user_service.py
│   ├── auth_service.py
│   └── file_service.py   👈 CSV streaming logic
│
├── utils/              # Helper utilities
│   ├── helper.py
│   └── Response.py
│
└── main.py             # Application entry point
```

---

## 🧠 Architecture Pattern

```text
Client
   ↓
API Layer (endpoints)
   ↓
Service Layer (business logic)
   ↓
Repository Layer (DB queries)
   ↓
Database
```

---

## 🚀 Key Features

### 📂 1. CSV Streaming Engine

* Reads large files without loading into memory
* Uses `TextIOWrapper` for efficient parsing
* Supports row-by-row processing

---

### ✅ 2. Header Validation

* Ensures correct CSV structure before processing
* Prevents invalid data ingestion

---

### ⚡ 3. Bulk Insert Optimization

* Batch insertion (high performance)
* Uses DB-level conflict handling (`ON CONFLICT`)
* Avoids duplicate records

---

### 🔁 4. Duplicate Handling

* Email uniqueness enforced at DB level
* Skips duplicate records safely

---

### 🧩 5. Modular Design

* Clean separation of concerns
* Easy to extend and maintain

---

## 🔄 CSV Processing Flow

```text
Upload CSV
   ↓
FileService.read_file()
   ↓
Header Validation
   ↓
Streaming Rows
   ↓
Transformation (optional)
   ↓
Batch Insert (UserService)
   ↓
Database
```

---

## 📡 API Example

### Upload Users CSV

```http
POST /users/upload
```

### Request:

* multipart/form-data
* file: CSV

### Response:

```json
{
  "total": 1000,
  "inserted": 950,
  "skipped": 50,
  "duplicate_users": ["test@mail.com"]
}
```

---

## ⚙️ Tech Stack

* FastAPI
* SQLAlchemy
* PostgreSQL
* Alembic (migrations)
* Python 3.x

---

## ⚡ Performance Optimizations

* Streaming file processing
* Batch DB insert (500 records)
* Binary row counting
* DB-level duplicate handling

---

## 🔐 Security

* Authentication via `auth_service.py`
* Secure dependency injection (`deps.py`)
* Input validation via Pydantic schemas

---

## 🧪 Error Handling

* Custom exceptions (`core/exceptions.py`)
* Row-level error skipping
* Structured API responses

---

## 📈 Future Enhancements

* Background job processing (Celery/Kafka)
* Progress tracking API
* Error report CSV download
* Real-time dashboard

---

## 👨‍💻 Author

Chandan Rao
