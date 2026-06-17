# =============================================================
# database.py - Configuração do banco de dados SQLite
# =============================================================
# Este arquivo cria a conexão com o banco SQLite e fornece
# uma "sessão" que os endpoints usam para acessar o banco.
# =============================================================

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL do banco de dados SQLite — o arquivo fila.db será criado
# automaticamente na mesma pasta do projeto
SQLALCHEMY_DATABASE_URL = "sqlite:///./fila.db"

# Cria o motor (engine) de conexão com o banco
# check_same_thread=False é necessário para o FastAPI funcionar
# corretamente com SQLite em múltiplas requisições
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Fábrica de sessões — cada requisição HTTP usa uma sessão separada
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para todos os modelos (tabelas) do banco de dados
Base = declarative_base()


def get_db():
    """
    Função geradora que fornece uma sessão de banco de dados.
    Usada como dependência (Depends) nos endpoints do FastAPI.
    Garante que a sessão seja fechada ao final de cada requisição.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
