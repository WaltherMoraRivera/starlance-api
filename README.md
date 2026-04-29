# 🚀 StarLance API

API REST para gestión de tareas domésticas gamificadas con sistema de recompensas.

## 🧱 Stack
- FastAPI
- MongoDB Atlas
- Motor (async driver)
- Pytest
- OpenTelemetry

## ⚙️ Setup

```bash
git clone https://github.com/WaltherMoraRivera/starlance-api.git
cd starlance-api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

## ▶️ Run

```bash
uvicorn app.main:app --reload
```

## 📘 Docs

http://localhost:8000/docs

## 🧪 Tests

```bash
pytest --cov=app
```

## 📊 CI/CD

GitHub Actions valida cobertura ≥ 80%