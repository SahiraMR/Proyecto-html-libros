import csv
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models.autor import Autor
from app.models.libro import Libro
from app.models.comentario import Comentario

# Iniciar sesión de base de datos
db: Session = SessionLocal()

# === Cargar Autores ===
with open("data/autores.csv", encoding="utf-8") as archivo:
    reader = csv.DictReader(archivo)
    for row in reader:
        autor = Autor(
            id=int(row["id"]),
            nombre=row["nombre"],
            genero=row.get("genero", "N/A")
        )
        db.merge(autor)  # merge evita duplicados

# Confirmar autores antes de pasar a libros
db.commit()

# === Cargar Libros ===
with open("data/libros.csv", encoding="utf-8") as archivo:
    reader = csv.DictReader(archivo)
    for row in reader:
        libro = Libro(
            id=int(row["id"]),
            titulo=row["titulo"],
            autor_id=int(row["autor_id"]),
            anio_publicacion=row.get("anio_publicacion"),
            genero=row.get("genero"),
            plataforma=row.get("plataforma"),
            viral_en_tiktok=row.get("viral_en_tiktok") == "True",
            portada=row.get("portada"),
            eliminado=row.get("eliminado", "False") == "True"
        )
        db.merge(libro)

db.commit()  # ✅ Guardar libros antes de pasar a comentarios

# === Cargar Comentarios ===
with open("data/comentarios.csv", encoding="utf-8") as archivo:
    reader = csv.DictReader(archivo)
    for row in reader:
        comentario = Comentario(
            id=int(row["id"]),
            libro_id=int(row["libro_id"]),
            usuario=row["usuario"],
            contenido=row["contenido"],
            fecha=row["fecha"],
            eliminado=row.get("eliminado", "False") == "True"
        )
        db.merge(comentario)

db.commit()
print("✅ Datos cargados correctamente en la base de datos.")
