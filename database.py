import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from flask import Flask

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    try:
        engine = create_engine(
            DATABASE_URL,
            pool_size=5,
            max_overflow=2,
            pool_timeout=30,
            pool_recycle=1800,
            pool_pre_ping=True
        )
        print("✅ Conectado a base remota")
    except Exception as e:
        print("⚠️ Error al conectar con base remota, usando SQLite local:", e)
        engine = create_engine(
            "sqlite:///listaapp.db",
            connect_args={"check_same_thread": False}
        )
else:
    print("💾 Usando base de datos local SQLite")
    engine = create_engine(
        "sqlite:///listaapp.db",
        connect_args={"check_same_thread": False}
    )

SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_app(app: Flask):
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        SessionLocal.remove()
