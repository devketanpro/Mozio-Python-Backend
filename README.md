# 🚖 Mozio Backend Project

A **Django REST Framework** application for managing transportation providers and their service areas using spatial data. Shuttle companies can define and manage service areas (custom polygons), and the app provides a fast lookup API to identify which service areas cover a specific geographic point.

---

## 🚀 Features

- CRUD APIs for `Provider` and `ServiceArea`
- Fast geospatial lookup endpoint (latitude & longitude)
- Token-based authentication
- Dockerized setup for easy development & deployment
- PostgreSQL with PostGIS support
- Unit tests for core functionality
- API Gateway simulation with rate limiting
- Optional AWS deployment support

---

## 🧱 Tech Stack

- **Python** 3.10+
- **Django** 5.x
- **Django REST Framework**
- **PostgreSQL** + **PostGIS**
- **Docker** & **Docker Compose**
- **Redis** (optional, for caching/rate limiting)
- **AWS** (optional, for production)

---

## 📦 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/devketanpro/Mozio-Python-Backend.git
cd mozio-backend
```

---

### 2. Create `.env` File in the Root Directory

```env
DEBUG=1
SECRET_KEY=your-secret-key
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
DATABASE_NAME=mozio
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=db
DATABASE_PORT=5432
```

---

### 3. Build & Start Docker Containers

```bash
docker-compose up --build
```

This will start the Django app and a PostgreSQL container with PostGIS enabled.

---

### 4. Create Superuser (for Admin Access)

```bash
docker-compose exec web python manage.py createsuperuser
```

Then visit: [http://localhost:8000/admin/](http://localhost:8000/admin/) to log in.

---

## ✅ Testing

To run tests inside the Docker container:

```bash
docker-compose exec web python manage.py test
```

---

## 📂 API Endpoints

| Endpoint                                          | Method | Description                         |
|---------------------------------------------------|--------|-------------------------------------|
| `/api/providers/`                                 | CRUD   | Manage transportation providers     |
| `/api/service-areas/`                             | CRUD   | Manage service areas (polygons)     |
| `/api/lookup-service-area/?lat=<lat>&lng=<lng>`   | GET    | Find service areas covering a point |
| `/api/auth/signup/`                               | POST   | Sign up a new user                  |
---

## 📘 API Documentation

All endpoints are documented here:  
👉 [Postman Public Docs](https://documenter.getpostman.com/view/47197878/2sB3B8stgs)