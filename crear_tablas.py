from app.database import engine
from app.models import autor, libro, comentario  # importa todos los modelos
from app.database import Base

print("⚠️ Esto eliminará todas las tablas existentes. Asegúrate de tener un backup si es necesario.")

# Borra todas las tablas existentes
Base.metadata.drop_all(bind=engine)
print("❌ Tablas eliminadas.")

# Crea todas las tablas según los modelos actuales
Base.metadata.create_all(bind=engine)
print("✅ Tablas creadas correctamente.")
