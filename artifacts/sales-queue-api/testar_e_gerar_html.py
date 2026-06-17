# =============================================================
# testar_e_gerar_html.py - Testa a API e gera um HTML de resultados
# =============================================================
# Este script executa um fluxo completo de testes na API e gera
# um arquivo HTML com os resultados, ideal para apresentação.
# =============================================================

import json
import urllib.request
import urllib.error
from datetime import datetime

BASE_URL = "http://localhost:8000"

# Resultados de cada teste
resultados = []


def fazer_requisicao(method, endpoint, data=None, descricao=""):
    """Faz uma requisição HTTP e retorna o resultado."""
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}

    if data:
        data_bytes = json.dumps(data).encode("utf-8")
    else:
        data_bytes = None

    req = urllib.request.Request(url, data=data_bytes, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            body = response.read().decode("utf-8")
            status = response.status
            try:
                json_body = json.loads(body)
            except json.JSONDecodeError:
                json_body = body
            return {
                "sucesso": True,
                "status": status,
                "endpoint": endpoint,
                "method": method,
                "descricao": descricao,
                "resposta": json_body,
                "raw": body
            }
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            json_body = json.loads(body)
        except json.JSONDecodeError:
            json_body = body
        return {
            "sucesso": False,
            "status": e.code,
            "endpoint": endpoint,
            "method": method,
            "descricao": descricao,
            "resposta": json_body,
            "raw": body
        }
    except Exception as e:
        return {
            "sucesso": False,
            "status": 0,
            "endpoint": endpoint,
            "method": method,
            "descricao": descricao,
            "resposta": str(e),
            "raw": str(e)
        }


def adicionar_resultado(r):
    """Adiciona um resultado à lista."""
    resultados.append(r)
    icon = "✅" if r["sucesso"] else "❌"
    print(f"{icon} {r['method']} {r['endpoint']} → {r['status']} | {r['descricao']}")


def gerar_html():
    """Gera o arquivo HTML com os resultados."""
    html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Fila de Atendimento - Resultados dos Testes</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
            color: #333;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
            color: white;
        }
        .header h1 {
            font-size: 2.2em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        .card {
            background: white;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
            transition: transform 0.2s;
        }
        .card:hover {
            transform: translateY(-2px);
        }
        .card-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 2px solid #f0f0f0;
        }
        .badge {
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.75em;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .badge-get { background: #e3f2fd; color: #1565c0; }
        .badge-post { background: #e8f5e9; color: #2e7d32; }
        .badge-put { background: #fff3e0; color: #ef6c00; }
        .badge-ok { background: #e8f5e9; color: #2e7d32; }
        .badge-erro { background: #ffebee; color: #c62828; }
        .endpoint {
            font-family: 'Courier New', monospace;
            font-size: 0.95em;
            color: #555;
            background: #f5f5f5;
            padding: 4px 10px;
            border-radius: 6px;
        }
        .descricao {
            font-size: 1.05em;
            color: #444;
            margin-bottom: 12px;
            font-weight: 500;
        }
        .resposta {
            background: #1e1e2e;
            border-radius: 10px;
            padding: 16px;
            overflow-x: auto;
        }
        .resposta pre {
            color: #a6e3a1;
            font-family: 'Courier New', monospace;
            font-size: 0.85em;
            line-height: 1.5;
            white-space: pre-wrap;
            word-break: break-word;
        }
        .resposta .key {
            color: #89b4fa;
        }
        .resposta .string {
            color: #a6e3a1;
        }
        .resposta .number {
            color: #fab387;
        }
        .resposta .boolean {
            color: #f38ba8;
        }
        .resposta .null {
            color: #f38ba8;
        }
        .status-line {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 12px;
        }
        .status-code {
            font-size: 0.85em;
            font-weight: bold;
            padding: 4px 10px;
            border-radius: 6px;
        }
        .status-200 { background: #d4edda; color: #155724; }
        .status-201 { background: #d4edda; color: #155724; }
        .status-400 { background: #f8d7da; color: #721c24; }
        .status-404 { background: #f8d7da; color: #721c24; }
        .status-500 { background: #f8d7da; color: #721c24; }
        .summary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
        }
        .summary h2 {
            margin-bottom: 16px;
            font-size: 1.5em;
        }
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
        }
        .summary-item {
            background: rgba(255,255,255,0.15);
            border-radius: 12px;
            padding: 16px;
            text-align: center;
        }
        .summary-item .number {
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 4px;
        }
        .summary-item .label {
            font-size: 0.9em;
            opacity: 0.85;
        }
        .footer {
            text-align: center;
            color: white;
            opacity: 0.7;
            margin-top: 40px;
            font-size: 0.9em;
        }
        .fila-table {
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
            font-size: 0.9em;
        }
        .fila-table th {
            background: #667eea;
            color: white;
            padding: 10px;
            text-align: left;
        }
        .fila-table td {
            padding: 10px;
            border-bottom: 1px solid #eee;
        }
        .fila-table tr:nth-child(even) {
            background: #f8f9fa;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛒 API Fila de Atendimento</h1>
            <p>Resultados dos Testes Automatizados - Lista da Vez</p>
            <p style="font-size:0.9em; margin-top:8px;">Gerado em: %%DATA_HORA%%</p>
        </div>

        <div class="summary">
            <h2>📊 Resumo dos Testes</h2>
            <div class="summary-grid">
                <div class="summary-item">
                    <div class="number">%%TOTAL_TESTES%%</div>
                    <div class="label">Total de Testes</div>
                </div>
                <div class="summary-item">
                    <div class="number">%%SUCESSOS%%</div>
                    <div class="label">Sucessos</div>
                </div>
                <div class="summary-item">
                    <div class="number">%%ERROS%%</div>
                    <div class="label">Erros</div>
                </div>
                <div class="summary-item">
                    <div class="number">%%TAXA_SUCESSO%%%</div>
                    <div class="label">Taxa de Sucesso</div>
                </div>
            </div>
        </div>
"""

    sucessos = sum(1 for r in resultados if r["sucesso"])
    erros = sum(1 for r in resultados if not r["sucesso"])
    total = len(resultados)
    taxa = round((sucessos / total) * 100) if total > 0 else 0

    html = html.replace("%%DATA_HORA%%", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    html = html.replace("%%TOTAL_TESTES%%", str(total))
    html = html.replace("%%SUCESSOS%%", str(sucessos))
    html = html.replace("%%ERROS%%", str(erros))
    html = html.replace("%%TAXA_SUCESSO%%", str(taxa))

    for i, r in enumerate(resultados, 1):
        method = r["method"]
        status = r["status"]
        sucesso = r["sucesso"]

        method_class = f"badge-{method.lower()}"
        status_class = f"status-{status}"
        badge_class = "badge-ok" if sucesso else "badge-erro"
        badge_text = "OK" if sucesso else "ERRO"

        # Pretty print JSON
        if isinstance(r["resposta"], (dict, list)):
            resposta_str = json.dumps(r["resposta"], indent=2, ensure_ascii=False)
        else:
            resposta_str = str(r["resposta"])

        # Colorir JSON no HTML
        resposta_colorida = colorir_json(resposta_str)

        html += f"""
        <div class="card">
            <div class="card-header">
                <span class="badge {method_class}">{method}</span>
                <span class="endpoint">{r["endpoint"]}</span>
                <span class="badge {badge_class}">{badge_text}</span>
            </div>
            <div class="status-line">
                <span class="status-code {status_class}">HTTP {status}</span>
                <span style="font-size:0.85em;color:#666;">Teste #{i}</span>
            </div>
            <div class="descricao">{r["descricao"]}</div>
            <div class="resposta">
                <pre>{resposta_colorida}</pre>
            </div>
        </div>
"""

    html += """
        <div class="footer">
            <p>API Fila de Atendimento - Lista da Vez | Python + FastAPI + SQLite</p>
            <p>Projeto Acadêmico</p>
        </div>
    </div>
</body>
</html>
"""

    return html


def colorir_json(texto):
    """Aplica coloração sintática ao JSON para HTML."""
    import re

    # Escapar HTML
    texto = texto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    # Colorir strings
    texto = re.sub(r'"([^"]*)":', r'<span class="key">"\1"</span>:', texto)
    texto = re.sub(r': "([^"]*)"', r': <span class="string">"\1"</span>', texto)
    texto = re.sub(r'"([^"]*)"', r'<span class="string">"\1"</span>', texto)

    # Colorir números
    texto = re.sub(r': (\d+\.?\d*)', r': <span class="number">\1</span>', texto)
    texto = re.sub(r'\b(\d+\.?\d*)\b', r'<span class="number">\1</span>', texto)

    # Colorir booleanos
    texto = re.sub(r'\b(true|false)\b', r'<span class="boolean">\1</span>', texto)

    # Colorir null
    texto = re.sub(r'\bnull\b', r'<span class="null">null</span>', texto)

    return texto


def main():
    print("=" * 60)
    print("🧪 TESTES AUTOMATIZADOS - API Fila de Atendimento")
    print("=" * 60)
    print()

    # ============================================================
    # TESTE 1: Cadastrar Vendedores
    # ============================================================
    print("📋 ETAPA 1: Cadastrar Vendedores")
    print("-" * 40)

    r1 = fazer_requisicao("POST", "/vendedores", {"nome": "Ana Silva"}, "Cadastrar vendedor Ana Silva")
    adicionar_resultado(r1)
    vendedor_1 = r1["resposta"].get("id") if isinstance(r1["resposta"], dict) else None

    r2 = fazer_requisicao("POST", "/vendedores", {"nome": "Carlos Mendes"}, "Cadastrar vendedor Carlos Mendes")
    adicionar_resultado(r2)
    vendedor_2 = r2["resposta"].get("id") if isinstance(r2["resposta"], dict) else None

    r3 = fazer_requisicao("POST", "/vendedores", {"nome": "Beatriz Costa"}, "Cadastrar vendedor Beatriz Costa")
    adicionar_resultado(r3)
    vendedor_3 = r3["resposta"].get("id") if isinstance(r3["resposta"], dict) else None

    # Teste: tentar cadastrar duplicado
    r_dup = fazer_requisicao("POST", "/vendedores", {"nome": "Ana Silva"}, "Tentar cadastrar vendedor duplicado")
    adicionar_resultado(r_dup)

    # Listar vendedores
    r4 = fazer_requisicao("GET", "/vendedores", None, "Listar todos os vendedores cadastrados")
    adicionar_resultado(r4)

    print()

    # ============================================================
    # TESTE 2: Controle da Fila
    # ============================================================
    print("🔄 ETAPA 2: Controle da Fila (Lista da Vez)")
    print("-" * 40)

    if vendedor_1:
        r5 = fazer_requisicao("POST", f"/fila/{vendedor_1}", None, "Inserir Ana Silva na fila")
        adicionar_resultado(r5)
    if vendedor_2:
        r6 = fazer_requisicao("POST", f"/fila/{vendedor_2}", None, "Inserir Carlos Mendes na fila")
        adicionar_resultado(r6)
    if vendedor_3:
        r7 = fazer_requisicao("POST", f"/fila/{vendedor_3}", None, "Inserir Beatriz Costa na fila")
        adicionar_resultado(r7)

    # Tentar inserir duplicado
    if vendedor_1:
        r_dup_fila = fazer_requisicao("POST", f"/fila/{vendedor_1}", None, "Tentar inserir Ana Silva na fila novamente (já está na fila)")
        adicionar_resultado(r_dup_fila)

    # Consultar fila
    r8 = fazer_requisicao("GET", "/fila", None, "Consultar fila atual (3 vendedores)")
    adicionar_resultado(r8)

    # Chamar próximo (Ana vai para o final)
    r9 = fazer_requisicao("POST", "/fila/proximo", None, "Chamar próximo vendedor (Ana Silva atende, vai para o final)")
    adicionar_resultado(r9)

    # Consultar fila após chamar
    r10 = fazer_requisicao("GET", "/fila", None, "Consultar fila após chamar (Ana deve estar no final)")
    adicionar_resultado(r10)

    # Chamar próximo novamente (Carlos vai para o final)
    r11 = fazer_requisicao("POST", "/fila/proximo", None, "Chamar próximo (Carlos Mendes atende, vai para o final)")
    adicionar_resultado(r11)

    r12 = fazer_requisicao("GET", "/fila", None, "Consultar fila após segunda chamada")
    adicionar_resultado(r12)

    # Chamar próximo novamente (Beatriz vai para o final)
    r13 = fazer_requisicao("POST", "/fila/proximo", None, "Chamar próximo (Beatriz Costa atende, vai para o final)")
    adicionar_resultado(r13)

    r14 = fazer_requisicao("GET", "/fila", None, "Consultar fila após terceira chamada (todos rodaram)")
    adicionar_resultado(r14)

    print()

    # ============================================================
    # TESTE 3: Atendimentos
    # ============================================================
    print("💼 ETAPA 3: Atendimentos")
    print("-" * 40)

    if vendedor_1:
        r15 = fazer_requisicao("POST", f"/atendimentos/iniciar/{vendedor_1}", None, "Iniciar atendimento para Ana Silva")
        adicionar_resultado(r15)
        atendimento_1 = r15["resposta"].get("id") if isinstance(r15["resposta"], dict) else None

        if atendimento_1:
            r16 = fazer_requisicao("PUT", f"/atendimentos/{atendimento_1}/finalizar", {"houve_venda": True}, "Finalizar atendimento - Ana VENDEU")
            adicionar_resultado(r16)

    if vendedor_2:
        r17 = fazer_requisicao("POST", f"/atendimentos/iniciar/{vendedor_2}", None, "Iniciar atendimento para Carlos Mendes")
        adicionar_resultado(r17)
        atendimento_2 = r17["resposta"].get("id") if isinstance(r17["resposta"], dict) else None

        if atendimento_2:
            r18 = fazer_requisicao("PUT", f"/atendimentos/{atendimento_2}/finalizar", {"houve_venda": False}, "Finalizar atendimento - Carlos NÃO vendeu")
            adicionar_resultado(r18)

    if vendedor_3:
        r19 = fazer_requisicao("POST", f"/atendimentos/iniciar/{vendedor_3}", None, "Iniciar atendimento para Beatriz Costa")
        adicionar_resultado(r19)
        atendimento_3 = r19["resposta"].get("id") if isinstance(r19["resposta"], dict) else None

        if atendimento_3:
            r20 = fazer_requisicao("PUT", f"/atendimentos/{atendimento_3}/finalizar", {"houve_venda": True}, "Finalizar atendimento - Beatriz VENDEU")
            adicionar_resultado(r20)

    # Tentar iniciar atendimento para vendedor inexistente
    r21 = fazer_requisicao("POST", "/atendimentos/iniciar/999", None, "Tentar iniciar atendimento para vendedor inexistente")
    adicionar_resultado(r21)

    print()

    # ============================================================
    # TESTE 4: Relatórios
    # ============================================================
    print("📊 ETAPA 4: Relatórios")
    print("-" * 40)

    r22 = fazer_requisicao("GET", "/relatorios", None, "Consultar relatório de desempenho")
    adicionar_resultado(r22)

    print()

    # ============================================================
    # GERAR HTML
    # ============================================================
    print("=" * 60)
    print("📝 GERANDO HTML DE RESULTADOS...")
    print("=" * 60)

    html = gerar_html()
    arquivo_saida = "resultados.html"

    with open(arquivo_saida, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Arquivo gerado: {arquivo_saida}")
    print(f"📍 Caminho completo: {__import__('os').path.abspath(arquivo_saida)}")
    print()

    sucessos = sum(1 for r in resultados if r["sucesso"])
    erros = sum(1 for r in resultados if not r["sucesso"])
    print(f"📊 Resultado final: {sucessos}/{len(resultados)} testes passaram")
    print()
    print("🌐 Para visualizar, abra o arquivo resultados.html no navegador")
    print("   ou execute: python -m http.server 8080")
    print("   e acesse: http://localhost:8080/resultados.html")


if __name__ == "__main__":
    main()
