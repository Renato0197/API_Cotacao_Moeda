import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

# Usa o banco da variável de ambiente; se não existir (ex: local), cai no SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cotacoes.db")

# Alguns provedores entregam a URL começando com "postgres://",
# mas o SQLAlchemy espera "postgresql://"
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# check_same_thread só existe no SQLite
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()