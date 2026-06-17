# =============================================================
# models.py - Modelos do banco de dados (tabelas SQLite)
# =============================================================
# Cada classe representa uma tabela no banco de dados.
# O SQLAlchemy traduz essas classes para comandos SQL.
# =============================================================

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Vendedor(Base):
    """
    Tabela 'vendedores' — armazena os vendedores cadastrados.
    """
    __tablename__ = "vendedores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)           # Nome do vendedor
    ativo = Column(Boolean, default=True)            # Se o vendedor está ativo
    criado_em = Column(DateTime, default=datetime.now)

    # Relacionamentos com outras tabelas
    fila = relationship("FilaAtendimento", back_populates="vendedor")
    atendimentos = relationship("Atendimento", back_populates="vendedor")


class FilaAtendimento(Base):
    """
    Tabela 'fila' — controla a fila de atendimento (lista da vez).
    Cada registro representa um vendedor na fila.
    """
    __tablename__ = "fila"

    id = Column(Integer, primary_key=True, index=True)
    vendedor_id = Column(Integer, ForeignKey("vendedores.id"), nullable=False)
    posicao = Column(Integer, nullable=False)  # Posição na fila (menor = primeiro)
    na_fila = Column(Boolean, default=True)    # Se ainda está aguardando na fila
    entrou_em = Column(DateTime, default=datetime.now)

    # Relacionamento com a tabela de vendedores
    vendedor = relationship("Vendedor", back_populates="fila")


class Atendimento(Base):
    """
    Tabela 'atendimentos' — registra cada atendimento realizado.
    """
    __tablename__ = "atendimentos"

    id = Column(Integer, primary_key=True, index=True)
    vendedor_id = Column(Integer, ForeignKey("vendedores.id"), nullable=False)
    iniciado_em = Column(DateTime, default=datetime.now)  # Quando começou
    finalizado_em = Column(DateTime, nullable=True)        # Quando terminou
    houve_venda = Column(Boolean, nullable=True)           # Se resultou em venda
    status = Column(String, default="em_andamento")        # em_andamento | finalizado

    # Relacionamento com a tabela de vendedores
    vendedor = relationship("Vendedor", back_populates="atendimentos")
