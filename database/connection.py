from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config.config import Config
from utils.logger import get_logger

logger = get_logger("database_connection")

engine = create_engine(Config.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    try:
        import models.analysis  # Garante o registro dos modelos
        Base.metadata.create_all(bind=engine)
        logger.info("Banco de dados e tabelas inicializados com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao inicializar o banco de dados: {str(e)}")
        raise e

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()