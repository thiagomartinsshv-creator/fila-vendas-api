# =============================================================
# schemas.py - Schemas Pydantic (validação de dados da API)
# =============================================================
# Os schemas definem o formato dos dados que entram e saem
# da API. O FastAPI usa isso para validar automaticamente
# as requisições e gerar a documentação no Swagger.
# =============================================================

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# ---------------------------
# Schemas de Vendedor
# ---------------------------

class VendedorCreate(BaseModel):
    """Dados necessários para criar um vendedor."""
    nome: str


class VendedorResponse(BaseModel):
    """Dados retornados ao consultar um vendedor."""
    id: int
    nome: str
    ativo: bool
    criado_em: datetime

    class Config:
        from_attributes = True  # Permite converter objetos do SQLAlchemy


# ---------------------------
# Schemas de Fila
# ---------------------------

class FilaItemResponse(BaseModel):
    """Representa um vendedor na fila."""
    posicao: int
    vendedor_id: int
    nome_vendedor: str
    entrou_em: datetime


# ---------------------------
# Schemas de Atendimento
# ---------------------------

class AtendimentoResponse(BaseModel):
    """Dados de um atendimento."""
    id: int
    vendedor_id: int
    nome_vendedor: str
    iniciado_em: datetime
    finalizado_em: Optional[datetime]
    houve_venda: Optional[bool]
    status: str

    class Config:
        from_attributes = True


class FinalizarAtendimentoRequest(BaseModel):
    """Dados necessários para finalizar um atendimento."""
    houve_venda: bool  # true = vendeu, false = não vendeu


# ---------------------------
# Schemas de Relatório
# ---------------------------

class RelatorioVendedorResponse(BaseModel):
    """Estatísticas de um vendedor."""
    vendedor_id: int
    nome: str
    total_atendimentos: int
    total_vendas: int
    taxa_conversao: float  # Percentual de atendimentos que resultaram em venda
