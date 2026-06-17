# API de Fila de Atendimento — Lista da Vez

API REST para gerenciamento da fila de atendimento de vendedores em uma loja física.  
Desenvolvida com **Python**, **FastAPI** e **SQLite**.

---

## Objetivo

Controlar a ordem de atendimento dos vendedores utilizando o conceito de **"lista da vez"**: o vendedor que for chamado vai automaticamente para o final da fila, garantindo equidade no atendimento.

---

## Tecnologias Utilizadas

| Tecnologia | Versão | Função |
|---|---|---|
| Python | 3.11 | Linguagem de programação |
| FastAPI | 0.115 | Framework web para criação da API |
| SQLAlchemy | 2.0 | ORM para acesso ao banco de dados |
| SQLite | built-in | Banco de dados (arquivo local) |
| Uvicorn | 0.30 | Servidor ASGI para rodar a aplicação |
| Pydantic | 2.9 | Validação de dados |

---

## Estrutura do Projeto

```
sales-queue-api/
├── main.py          # Aplicação FastAPI e todos os endpoints
├── database.py      # Configuração da conexão com SQLite
├── models.py        # Modelos do banco de dados (tabelas)
├── schemas.py       # Schemas de validação (entrada/saída da API)
├── requirements.txt # Dependências do projeto
└── README.md        # Este arquivo
```

---

## Banco de Dados

O banco SQLite é criado automaticamente ao iniciar a aplicação.  
Três tabelas são criadas:

- **vendedores** — cadastro dos vendedores
- **fila** — controle da fila de atendimento
- **atendimentos** — histórico de atendimentos realizados

---

## Como Executar

### 1. Instale as dependências

```bash
pip install -r requirements.txt
```

### 2. Inicie o servidor

```bash
uvicorn main:app --reload --port 8000
```

### 3. Acesse a documentação

Abra no navegador:

```
http://localhost:8000/docs
```

---

## Endpoints Disponíveis

### Vendedores

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/vendedores` | Cadastrar novo vendedor |
| `GET` | `/vendedores` | Listar todos os vendedores |

### Fila de Atendimento

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/fila/{vendedor_id}` | Inserir vendedor na fila |
| `GET` | `/fila` | Consultar fila atual |
| `POST` | `/fila/proximo` | Chamar próximo vendedor |

### Atendimentos

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/atendimentos/iniciar/{vendedor_id}` | Iniciar atendimento |
| `PUT` | `/atendimentos/{atendimento_id}/finalizar` | Finalizar atendimento |

### Relatórios

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/relatorios` | Estatísticas por vendedor |

---

## Exemplo de Uso (Fluxo Completo)

### 1. Cadastrar vendedores
```bash
curl -X POST http://localhost:8000/vendedores \
  -H "Content-Type: application/json" \
  -d '{"nome": "Ana Silva"}'
```

### 2. Inserir vendedores na fila
```bash
curl -X POST http://localhost:8000/fila/1
curl -X POST http://localhost:8000/fila/2
```

### 3. Consultar a fila
```bash
curl http://localhost:8000/fila
```

### 4. Chamar o próximo vendedor
```bash
curl -X POST http://localhost:8000/fila/proximo
```

### 5. Iniciar atendimento
```bash
curl -X POST http://localhost:8000/atendimentos/iniciar/1
```

### 6. Finalizar atendimento com resultado
```bash
curl -X PUT http://localhost:8000/atendimentos/1/finalizar \
  -H "Content-Type: application/json" \
  -d '{"houve_venda": true}'
```

### 7. Ver relatório
```bash
curl http://localhost:8000/relatorios
```

---

## Documentação Automática (Swagger)

O FastAPI gera automaticamente uma interface interativa para testar a API.  
Acesse em: **http://localhost:8000/docs**

Nessa tela você pode:
- Ver todos os endpoints disponíveis
- Testar as requisições diretamente no navegador
- Consultar os schemas de entrada e saída

---

## Decisões de Projeto

- **SQLite**: Escolhido por ser embutido no Python, sem necessidade de instalar um servidor de banco de dados separado.
- **Um arquivo por responsabilidade**: Separado em `database.py`, `models.py`, `schemas.py` e `main.py` para facilitar o entendimento.
- **Sem autenticação**: Projeto acadêmico focado nos conceitos de API REST e fila de atendimento.
- **Lista da vez**: Ao ser chamado, o vendedor vai automaticamente para o final da fila, garantindo rotatividade justa.
