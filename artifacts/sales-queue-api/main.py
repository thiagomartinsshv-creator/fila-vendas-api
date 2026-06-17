# =============================================================
# main.py - Aplicação principal FastAPI
# =============================================================
# Este é o arquivo central da API. Aqui ficam todos os
# endpoints (rotas) organizados por funcionalidade.
#
# Como executar:
#   uvicorn main:app --reload --port 8000
#
# Documentação automática disponível em:
#   http://localhost:8000/docs  (Swagger UI)
#   http://localhost:8000/redoc (ReDoc)
# =============================================================

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import List

import models
import schemas
from database import engine, get_db

# Cria todas as tabelas no banco SQLite automaticamente
# Se o arquivo fila.db não existir, ele será criado aqui
models.Base.metadata.create_all(bind=engine)

# Inicializa a aplicação FastAPI com título e descrição
app = FastAPI(
    title="API de Fila de Atendimento",
    description="""
    ## Sistema de Gerenciamento de Fila de Atendimento — Lista da Vez

    Controla a ordem de atendimento dos vendedores em uma loja física.

    ### Funcionalidades:
    - **Vendedores**: Cadastro e listagem de vendedores
    - **Fila**: Controle da fila de atendimento (lista da vez)
    - **Atendimentos**: Registro e finalização de atendimentos
    - **Relatórios**: Estatísticas por vendedor
    """,
    version="1.0.0"
)


# ==============================================================
# SEÇÃO 1 — VENDEDORES
# Endpoints para cadastro e listagem de vendedores
# ==============================================================

@app.post(
    "/vendedores",
    response_model=schemas.VendedorResponse,
    summary="Cadastrar novo vendedor",
    tags=["Vendedores"]
)
def criar_vendedor(vendedor: schemas.VendedorCreate, db: Session = Depends(get_db)):
    """
    Cadastra um novo vendedor no sistema.

    - **nome**: Nome completo do vendedor (obrigatório)
    """
    # Verifica se já existe um vendedor com esse nome
    existente = db.query(models.Vendedor).filter(
        models.Vendedor.nome == vendedor.nome
    ).first()

    if existente:
        raise HTTPException(
            status_code=400,
            detail=f"Já existe um vendedor com o nome '{vendedor.nome}'"
        )

    # Cria o objeto vendedor e salva no banco
    novo_vendedor = models.Vendedor(nome=vendedor.nome)
    db.add(novo_vendedor)
    db.commit()
    db.refresh(novo_vendedor)

    return novo_vendedor


@app.get(
    "/vendedores",
    response_model=List[schemas.VendedorResponse],
    summary="Listar todos os vendedores",
    tags=["Vendedores"]
)
def listar_vendedores(db: Session = Depends(get_db)):
    """
    Retorna a lista de todos os vendedores cadastrados.
    """
    vendedores = db.query(models.Vendedor).all()
    return vendedores


# ==============================================================
# SEÇÃO 2 — FILA DE ATENDIMENTO (LISTA DA VEZ)
# Endpoints para controlar a fila
# ==============================================================

@app.post(
    "/fila/proximo",
    summary="Chamar próximo vendedor da fila",
    tags=["Fila"]
)
def chamar_proximo(db: Session = Depends(get_db)):
    """
    Chama o próximo vendedor da fila.

    O vendedor é removido do início da fila e recolocado no final
    (conceito de 'lista da vez' — quem foi atender vai para o fim).
    """
    # Busca o primeiro da fila (menor posição)
    primeiro = db.query(models.FilaAtendimento).filter(
        models.FilaAtendimento.na_fila == True
    ).order_by(models.FilaAtendimento.posicao).first()

    if not primeiro:
        raise HTTPException(
            status_code=404,
            detail="A fila está vazia. Nenhum vendedor aguardando."
        )

    nome_vendedor = primeiro.vendedor.nome
    vendedor_id = primeiro.vendedor_id

    # Remove o vendedor do início da fila
    primeiro.na_fila = False
    db.commit()

    # Calcula a nova última posição e reinsere o vendedor no final
    ultima_posicao = db.query(func.max(models.FilaAtendimento.posicao)).filter(
        models.FilaAtendimento.na_fila == True
    ).scalar() or 0

    nova_entrada = models.FilaAtendimento(
        vendedor_id=vendedor_id,
        posicao=ultima_posicao + 1
    )
    db.add(nova_entrada)
    db.commit()

    return {
        "mensagem": f"Vendedor '{nome_vendedor}' foi chamado para atendimento",
        "vendedor_id": vendedor_id,
        "nome_vendedor": nome_vendedor,
        "observacao": f"'{nome_vendedor}' foi recolocado no final da fila"
    }


@app.post(
    "/fila/{vendedor_id}",
    summary="Inserir vendedor na fila",
    tags=["Fila"]
)
def inserir_na_fila(vendedor_id: int, db: Session = Depends(get_db)):
    """
    Insere um vendedor no final da fila de atendimento.

    - **vendedor_id**: ID do vendedor a ser inserido na fila
    """
    # Verifica se o vendedor existe
    vendedor = db.query(models.Vendedor).filter(
        models.Vendedor.id == vendedor_id
    ).first()

    if not vendedor:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")

    # Verifica se o vendedor já está na fila
    ja_na_fila = db.query(models.FilaAtendimento).filter(
        models.FilaAtendimento.vendedor_id == vendedor_id,
        models.FilaAtendimento.na_fila == True
    ).first()

    if ja_na_fila:
        raise HTTPException(
            status_code=400,
            detail=f"O vendedor '{vendedor.nome}' já está na fila"
        )

    # Calcula a próxima posição (final da fila)
    ultima_posicao = db.query(func.max(models.FilaAtendimento.posicao)).filter(
        models.FilaAtendimento.na_fila == True
    ).scalar() or 0

    nova_posicao = ultima_posicao + 1

    # Cria o registro na fila
    entrada_fila = models.FilaAtendimento(
        vendedor_id=vendedor_id,
        posicao=nova_posicao
    )
    db.add(entrada_fila)
    db.commit()

    return {
        "mensagem": f"Vendedor '{vendedor.nome}' inserido na fila",
        "posicao": nova_posicao
    }


@app.get(
    "/fila",
    response_model=List[schemas.FilaItemResponse],
    summary="Consultar fila atual",
    tags=["Fila"]
)
def consultar_fila(db: Session = Depends(get_db)):
    """
    Retorna a fila de atendimento atual em ordem de posição.
    O primeiro da lista é o próximo a ser atendido.
    """
    # Busca vendedores que estão na fila, ordenados pela posição
    fila = db.query(models.FilaAtendimento).filter(
        models.FilaAtendimento.na_fila == True
    ).order_by(models.FilaAtendimento.posicao).all()

    if not fila:
        return []

    # Monta a resposta com nome do vendedor incluído
    resultado = []
    for i, item in enumerate(fila, start=1):
        resultado.append(schemas.FilaItemResponse(
            posicao=i,
            vendedor_id=item.vendedor_id,
            nome_vendedor=item.vendedor.nome,
            entrou_em=item.entrou_em
        ))

    return resultado


# ==============================================================
# SEÇÃO 3 — ATENDIMENTOS
# Endpoints para iniciar e finalizar atendimentos
# ==============================================================

@app.post(
    "/atendimentos/iniciar/{vendedor_id}",
    response_model=schemas.AtendimentoResponse,
    summary="Iniciar atendimento para um vendedor",
    tags=["Atendimentos"]
)
def iniciar_atendimento(vendedor_id: int, db: Session = Depends(get_db)):
    """
    Inicia um atendimento para o vendedor especificado.

    - **vendedor_id**: ID do vendedor que está iniciando o atendimento
    """
    # Verifica se o vendedor existe
    vendedor = db.query(models.Vendedor).filter(
        models.Vendedor.id == vendedor_id
    ).first()

    if not vendedor:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")

    # Verifica se o vendedor já tem um atendimento em andamento
    em_andamento = db.query(models.Atendimento).filter(
        models.Atendimento.vendedor_id == vendedor_id,
        models.Atendimento.status == "em_andamento"
    ).first()

    if em_andamento:
        raise HTTPException(
            status_code=400,
            detail=f"Vendedor '{vendedor.nome}' já possui um atendimento em andamento (ID: {em_andamento.id})"
        )

    # Cria o registro de atendimento
    novo_atendimento = models.Atendimento(
        vendedor_id=vendedor_id,
        status="em_andamento"
    )
    db.add(novo_atendimento)
    db.commit()
    db.refresh(novo_atendimento)

    return schemas.AtendimentoResponse(
        id=novo_atendimento.id,
        vendedor_id=novo_atendimento.vendedor_id,
        nome_vendedor=vendedor.nome,
        iniciado_em=novo_atendimento.iniciado_em,
        finalizado_em=None,
        houve_venda=None,
        status=novo_atendimento.status
    )


@app.put(
    "/atendimentos/{atendimento_id}/finalizar",
    response_model=schemas.AtendimentoResponse,
    summary="Finalizar atendimento",
    tags=["Atendimentos"]
)
def finalizar_atendimento(
    atendimento_id: int,
    dados: schemas.FinalizarAtendimentoRequest,
    db: Session = Depends(get_db)
):
    """
    Finaliza um atendimento em andamento e registra se houve venda.

    - **atendimento_id**: ID do atendimento a ser finalizado
    - **houve_venda**: `true` se resultou em venda, `false` caso contrário
    """
    # Busca o atendimento pelo ID
    atendimento = db.query(models.Atendimento).filter(
        models.Atendimento.id == atendimento_id
    ).first()

    if not atendimento:
        raise HTTPException(status_code=404, detail="Atendimento não encontrado")

    if atendimento.status == "finalizado":
        raise HTTPException(
            status_code=400,
            detail="Este atendimento já foi finalizado"
        )

    # Atualiza os dados do atendimento
    atendimento.finalizado_em = datetime.now()
    atendimento.houve_venda = dados.houve_venda
    atendimento.status = "finalizado"
    db.commit()
    db.refresh(atendimento)

    return schemas.AtendimentoResponse(
        id=atendimento.id,
        vendedor_id=atendimento.vendedor_id,
        nome_vendedor=atendimento.vendedor.nome,
        iniciado_em=atendimento.iniciado_em,
        finalizado_em=atendimento.finalizado_em,
        houve_venda=atendimento.houve_venda,
        status=atendimento.status
    )


# ==============================================================
# SEÇÃO 4 — RELATÓRIOS
# Endpoints para estatísticas de desempenho
# ==============================================================

@app.get(
    "/relatorios",
    response_model=List[schemas.RelatorioVendedorResponse],
    summary="Relatório de desempenho por vendedor",
    tags=["Relatórios"]
)
def relatorios(db: Session = Depends(get_db)):
    """
    Retorna estatísticas de desempenho para cada vendedor:

    - **total_atendimentos**: Quantos atendimentos o vendedor realizou
    - **total_vendas**: Quantos atendimentos resultaram em venda
    - **taxa_conversao**: Percentual de atendimentos convertidos em venda
    """
    vendedores = db.query(models.Vendedor).all()

    if not vendedores:
        return []

    resultado = []

    for vendedor in vendedores:
        # Conta os atendimentos finalizados do vendedor
        total_atendimentos = db.query(models.Atendimento).filter(
            models.Atendimento.vendedor_id == vendedor.id,
            models.Atendimento.status == "finalizado"
        ).count()

        # Conta quantos atendimentos resultaram em venda
        total_vendas = db.query(models.Atendimento).filter(
            models.Atendimento.vendedor_id == vendedor.id,
            models.Atendimento.status == "finalizado",
            models.Atendimento.houve_venda == True
        ).count()

        # Calcula a taxa de conversão (evita divisão por zero)
        if total_atendimentos > 0:
            taxa_conversao = round((total_vendas / total_atendimentos) * 100, 2)
        else:
            taxa_conversao = 0.0

        resultado.append(schemas.RelatorioVendedorResponse(
            vendedor_id=vendedor.id,
            nome=vendedor.nome,
            total_atendimentos=total_atendimentos,
            total_vendas=total_vendas,
            taxa_conversao=taxa_conversao
        ))

    return resultado


# ==============================================================
# Rota raiz — apenas para verificar se a API está online
# ==============================================================

@app.get("/", tags=["Status"])
def raiz():
    """Verifica se a API está funcionando."""
    return {
        "status": "online",
        "mensagem": "API de Fila de Atendimento está funcionando!",
        "documentacao": "/docs"
    }
