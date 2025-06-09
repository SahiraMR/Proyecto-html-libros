from app.database import engine, Base

# Importar todos los modelos para que se registren correctamente
from app.models import libro
from app.models import autor
from app.models import comentario

# Crear todas las tablas definidas en los modelos
print("📦 Creando tablas en la base de datos...")
Base.metadata.create_all(bind=engine)
print("✅ Tablas creadas exitosamente.")
