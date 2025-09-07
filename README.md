# 🛠️ Sirecom API

**Sirecom API** is a bridge between **ODOO** and the database, designed to automate updates from point-of-sale systems. For example, when a purchase is made, the stock in the database is automatically updated and synchronized across all points of sale.

[![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Learning-blue?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-green?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
---

## ⚡ Technologies Used

- Python  
- FastAPI  
- SQL (PostgreSQL or other relational databases)  
- SQLAlchemy

---

## 📝 Project Structure

- `main.py` – Entry point of the API  
- `auth.py` – Authentication and security logic  
- `config.py` – Configuration settings  
- `create_tables.py` – Script to create database tables  
- `crud.py` – CRUD operations for database models  
- `dependencies.py` – Shared dependencies for routes  
- `models.py` – Database models  
- `schemas.py` – Pydantic schemas for request and response validation  
- `router.py` – API routing  
- `requirements.txt` – Python dependencies  
- `__pycache__/` – Compiled Python files  
- `message/` – Logs or messages related to API operations  

---

## 🚀 Features

- **CRUD Operations** – Create, read, update, delete data in the database  
- **Authentication** – Secure endpoints with token-based auth  
- **Data Synchronization** – Automatically updates the database when changes happen in ODOO  
- **Routing** – Organized endpoints for efficient API access  

---

## 🧩 Dependencies

Install the required dependencies with pip:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

or

```text
fastapi>=0.115.0
uvicorn>=0.31.0
SQLAlchemy>=2.0.35
pydantic>=2.9.2
python-jose>=3.3.0
passlib>=1.7.4
python-multipart>=0.0.12
psycopg2-binary>=2.9.9
bcrypt>=4.2.0
anyio>=4.6.0
typing-extensions>=4.12.2
```

---

## 🚀 How to Run & Deploy
1️⃣ Run the API Locally (Development)

1. Clone the repository:

git clone https://github.com/Yahdiel-Engineer/API.git
cd Sirecom-API

2. Create and activate a virtual environment:

python -m venv venv
.\venv\Scripts\activate

3. Install dependencies:

pip install -r requirements.txt

4. Run the API:

uvicorn main:app --reload
- Access Swagger UI at http://127.0.0.1:8000/docs

  ## ⚠️ Important: Database Setup

Sirecom API requires a PostgreSQL database to store data. **Do not use the database URL provided in this repository**, as it points to a personal Supabase instance.  

### Steps to create your own database:

1. **Install PostgreSQL** locally or create a cloud instance (Supabase, Render, Railway, etc.)  
2. **Create a new database** for Sirecom API:
```sql
CREATE DATABASE db_name;
```
3. Update your DATABASE_URL in config.py:
```DATABASE_URL = "postgresql://sirecom_user:your_secure_password@localhost:5432/sirecom_db"```
4. Run create_tables.py to initialize tables:
```python create_tables.py```
 



