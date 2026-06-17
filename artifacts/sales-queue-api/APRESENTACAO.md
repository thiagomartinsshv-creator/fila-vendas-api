# Roteiro de Apresentação — API de Fila de Atendimento (Lista da Vez)

**Duração total:** aproximadamente 10 minutos

---

## 1. Introdução ao Problema (2 minutos)

**Contexto:**
Imagine uma loja física com vários vendedores. Durante o dia, clientes chegam e precisam ser atendidos. Mas como decidir **quem atende**?

**Problema comum:**
- Vendedores se sentem desvalorizados se um mesmo colega sempre pega os "melhores" clientes
- O gerente não tem uma visão confiavel sobre numeros de atendimentos realizados por vendedor
- Não há registro de quantos clientes cada um atendeu ou quantos atendimentos foram convertidos em vendas
- Sem dados, não é possível avaliar o desempenho da equipe

**Pergunta**
> *"Como resolver esse problema? Papel e caneta? Planilha?"*

**Solução proposta:**
Um sistema digital de **"Lista da vez"** — uma fila rotativa onde cada vendedor, ao atender, vai automaticamente para o final. Isso garante **Organização** e **Rastreabilidade**.

---

## 2. Arquitetura da Solução

**Tecnologias utilizadas:**

| Tecnologia | Função |
|---|---|
| **Python** | Linguagem de programação — simples, popular, ótima para iniciantes |
| **FastAPI** | Framework web moderno que gera documentação automática (Swagger) |
| **SQLite** | Banco de dados leve, embutido no Python, sem instalação extra |
| **SQLAlchemy** | ORM que permite escrever código Python em vez de SQL puro |
| **Pydantic** | Validação automática dos dados de entrada e saída |
| **Uvicorn** | Servidor que roda a aplicação FastAPI |

**Estrutura do projeto (4 arquivos):**

```
main.py        ← Endpoints da API (vendedores, fila, atendimentos, relatórios)
database.py    ← Conexão com SQLite e sessões de banco
models.py      ← Tabelas do banco (vendedores, fila, atendimentos)
schemas.py     ← Validação de dados (entrada/saída da API)
```

**Por que essa arquitetura?**
- Cada arquivo tem uma **única responsabilidade** — fácil de entender e manter
- SQLite elimina a necessidade de um servidor de banco separado
- FastAPI gera documentação interativa automaticamente em `/docs`

---

## 3. Demonstração da API

### Abra o navegador em `http://localhost:8000/docs`

**Passo 1 — Cadastrar vendedores**
```
POST /vendedores
Body: {"nome": "Ana Silva"}
POST /vendedores
Body: {"nome": "Carlos Mendes"}
POST /vendedores
Body: {"nome": "Beatriz Costa"}
```
> *"Três vendedores cadastrados no sistema."
> Mostre `GET /vendedores` para listar todos.*

**Passo 2 — Montar a fila**
```
POST /fila/1   ← Ana entra na fila
POST /fila/2   ← Carlos entra na fila
POST /fila/3   ← Beatriz entra na fila
```
> Mostre `GET /fila` — a lista está em ordem:
> 1. Ana Silva
> 2. Carlos Mendes
> 3. Beatriz Costa

**Passo 3 — Chamar o próximo**
```
POST /fila/proximo
```
> *"Ana Silva foi chamada para atender. O sistema a remove do início e..."*

> Mostre `GET /fila` novamente:
> 1. Carlos Mendes
> 2. Beatriz Costa
> 3. **Ana Silva** ← foi recolocada no final!

> *"Esse é o conceito de 'lista da vez' — quem foi atender vai para o final, garantindo que todos tenham chances iguais."

**Passo 4 — Registrar o atendimento**
```
POST /atendimentos/iniciar/1   ← Ana iniciou o atendimento
PUT /atendimentos/1/finalizar
Body: {"houve_venda": true}   ← Fechou a venda!
```
> *"O sistema registra quando começou, quando terminou e se houve venda."

**Passo 5 — Ver o relatório**
```
GET /relatorios
```
> *"O relatório mostra: total de atendimentos, total de vendas e taxa de conversão por vendedor."
> *"Ana Silva tem 100% de conversão — 1 atendimento, 1 venda. Os outros ainda não atenderam ninguém."

> *"Imagine o gerente consultando isso ao final do dia para saber o desempenho da equipe."
> *"Possibilidade de projetar melhor a escala de vendedores."
> *"Melhor entendimento do Fluxo de clientes em loja ao longo dos dias, semanas e meses."
> *"Identificar picos no fluxo de atendimento por horario e dia"
> *"Taxa de clientes atendidos x vendas por vendedor."

---

## 4. Encerramento (1 minuto)

**Recapitule os pontos principais:**

1. **Problema:** Desorganização na ordem de atendimento e falta de dados de desempenho
2. **Solução:** Sistema de fila rotativa com registro de atendimentos e vendas
3. **Arquitetura:** Python + FastAPI + SQLite — stack leve e simples
4. **Demonstração:** A API funciona de ponta a ponta — cadastro, fila, atendimento, relatório


**Fim.**
