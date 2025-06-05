from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# ─── Lista de clientes exata ────────────────────────────────────────────────
clientes = {
    "matt": "André Ferreira",
    "michael": "Brener Stiff",
    "paul": "Danilo Continhola",
    "austin": "Davison Dias",
    "jaime": "Fernando Bernardo",
    "brandon": "Gabriel Batista",
    "jack": "Geraldo Neto",
    "nathan": "Jefferson Campos",
    "dylan": "Lucas Rodrigues",
    "matteo": "Pablo Silverio",
    "blake": "Jonatas Rolim",
    "tyler": "Leonardo Donaldson",
    "joe": "Luciano Guedes",
    "mike": "Luiz Carlos",
    "kevin": "Manoel Messias",
    "james": "Richard Stranssner",
    "mikael": "Rafael Moreira",
    "angelo": "Vinicius Silva"
}

# ─── Caminho absoluto da raiz do projeto ────────────────────────────────────
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# ─── Caminhos absolutos para arquivos de dados ───────────────────────────────
localidades_path = os.path.join(BASE_DIR, "localidades.txt")
visitadas_path  = os.path.join(BASE_DIR, "visitadas.txt")

# ─── Carrega todas as localidades em uma lista ───────────────────────────────
with open(localidades_path, encoding="utf-8") as f:
    todas_localidades = [linha.strip() for linha in f if linha.strip()]

total_localidades = len(todas_localidades)
# ----------------------------------------------
# Cada página mostra 100 items → calcula quantas páginas
total_paginas = (total_localidades + 99) // 100

# ─── Garante que o arquivo visitadas.txt exista ──────────────────────────────
if not os.path.exists(visitadas_path):
    # Se não existir, cria vazio
    open(visitadas_path, "w", encoding="utf-8").close()

def ler_visitadas():
    """
    Lê o arquivo visitadas.txt e retorna um set de locais já marcados.
    Usa o caminho absoluto visitadas_path para garantir consistência.
    """
    with open(visitadas_path, encoding="utf-8") as f:
        return set(linha.strip() for linha in f if linha.strip())

def salvar_visitadas(visitadas):
    """
    Grava no visitadas.txt (em ordem alfabética) a lista de locais marcados.
    Usa caminho absoluto para sempre salvar no mesmo local.
    """
    with open(visitadas_path, "w", encoding="utf-8") as f:
        for v in sorted(visitadas):
            f.write(v + "\n")

# ─── Rota da home: lista de clientes ────────────────────────────────────────
@app.route("/")
def home():
    # Envia a variável 'clientes' para o template
    return render_template("home.html", clientes=clientes)

# ─── Rota de index (listagem de localidades) para cada cliente ──────────────
@app.route("/<apelido>", methods=["GET", "POST"])
def index(apelido):
    if apelido not in clientes:
        # Se não for um cliente válido, volta à home
        return redirect(url_for("home"))

    # Se vier um POST com reset=1, volta para página 1
    if request.method == "POST" and request.form.get("reset") == "1":
        return redirect(url_for("index", apelido=apelido, pagina=1))

    # Qual página exibir? (?pagina=)
    pagina = int(request.args.get("pagina", 1))
    if pagina < 1:
        pagina = 1
    if pagina > total_paginas:
        pagina = total_paginas

    # Calcula slice de 100 localidades
    inicio = (pagina - 1) * 100
    fim    = inicio + 100
    itens  = todas_localidades[inicio:fim]

    # Cálculo de cor de fundo das caixas:
    # Ciclo de 7 páginas (isto é, a cada 700 localidades completas, muda de cor)
    cores_ciclo = ["#90ee90", "#00ffff", "#ffa500"]  # verde, ciano, laranja
    ciclo_index = (pagina - 1) // 7
    cor_localidade = cores_ciclo[ciclo_index % len(cores_ciclo)]

    # Carrega a lista atualizada de locais marcados (persistida em visitadas.txt)
    visitadas = ler_visitadas()

    # Nome do cliente para exibir no template
    nome_cliente = clientes[apelido]

    # Fornece todas as variáveis obrigatórias ao template index.html
    return render_template(
        "index.html",
        apelido=apelido,
        nome=nome_cliente,
        itens=itens,
        visitadas=visitadas,
        pagina_atual=pagina,
        total_paginas=total_paginas,
        cor_localidade=cor_localidade
    )

# ─── Rota “Próxima Página” ───────────────────────────────────────────────────
@app.route("/proxima_pagina/<apelido>")
def proxima_pagina(apelido):
    pagina = int(request.args.get("pagina", 1)) + 1
    return redirect(url_for("index", apelido=apelido, pagina=pagina))

# ─── Rota “Página Anterior” ─────────────────────────────────────────────────
@app.route("/pagina_anterior/<apelido>")
def pagina_anterior(apelido):
    pagina = int(request.args.get("pagina", 1)) - 1
    if pagina < 1:
        pagina = 1
    return redirect(url_for("index", apelido=apelido, pagina=pagina))

# ─── Rota para marcar/desmarcar “visitada” ───────────────────────────────────
@app.route("/marcar_visitada", methods=["POST"])
def marcar_visitada():
    local = request.form.get("local")
    if not local:
        return ("", 204)

    # Lê o set de visitadas (de todos os usuários) e faz toggle
    visitadas = ler_visitadas()
    if local in visitadas:
        visitadas.remove(local)
    else:
        visitadas.add(local)
    # Salva de volta no arquivo
    salvar_visitadas(visitadas)
    return ("", 204)

# ─── Inicia o Flask na porta definida pela variável de ambiente (“PORT”) ───────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
