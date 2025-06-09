import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv  # ← AÑADIDO

load_dotenv()  # ← CARGA .env automáticamente

# ✅ URL de conexión desde variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

# 🧱 Motor de conexión a PostgreSQL
engine = create_engine(DATABASE_URL)

# 🛠️ Generador de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 📦 Base para modelos
Base = declarative_base()

# 🔁 Dependencia para usar en rutas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 📦 Importa modelos para que SQLAlchemy los registre
from app.models import libro, autor, comentario

# ✅ Crea las tablas si no existen
Base.metadata.create_all(bind=engine)
