from flask import Flask, render_template, request, redirect, url_for
import os
import sqlite3

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
visitadas_db_path = os.path.join(BASE_DIR, "visitadas.db")

# Initialize SQLite database if not exists
def init_db():
    conn = sqlite3.connect(visitadas_db_path)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS visitadas (
        local TEXT PRIMARY KEY
    )""")
    conn.commit()
    conn.close()

init_db()

# Load localidades
with open(localidades_path, encoding="utf-8") as f:
    todas_localidades = [linha.strip() for linha in f if linha.strip()]
total_localidades = len(todas_localidades)
total_paginas = (total_localidades + 99) // 100

def ler_visitadas():
    conn = sqlite3.connect(visitadas_db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT local FROM visitadas")
    rows = cursor.fetchall()
    conn.close()
    return set(row[0] for row in rows)

def marcar_visitada_db(local):
    conn = sqlite3.connect(visitadas_db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT local FROM visitadas WHERE local = ?", (local,))
    exists = cursor.fetchone()
    if exists:
        cursor.execute("DELETE FROM visitadas WHERE local = ?", (local,))
    else:
        cursor.execute("INSERT INTO visitadas (local) VALUES (?)", (local,))
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("home.html", clientes=clientes)

@app.route("/<apelido>", methods=["GET", "POST"])
def index(apelido):
    if apelido not in clientes:
        return redirect(url_for("home"))

    if request.method == "POST" and request.form.get("reset") == "1":
        return redirect(url_for("index", apelido=apelido, pagina=1))

    pagina = int(request.args.get("pagina", 1))
    if pagina < 1:
        pagina = 1
    if pagina > total_paginas:
        pagina = total_paginas

    inicio = (pagina - 1) * 100
    fim = inicio + 100
    itens = todas_localidades[inicio:fim]

    cores_ciclo = ["#90ee90", "#00ffff", "#ffa500"]
    ciclo_index = (pagina - 1) // 7
    cor_localidade = cores_ciclo[ciclo_index % len(cores_ciclo)]

    visitadas = ler_visitadas()
    nome_cliente = clientes[apelido]

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

@app.route("/proxima_pagina/<apelido>")
def proxima_pagina(apelido):
    pagina = int(request.args.get("pagina", 1)) + 1
    return redirect(url_for("index", apelido=apelido, pagina=pagina))

@app.route("/pagina_anterior/<apelido>")
def pagina_anterior(apelido):
    pagina = int(request.args.get("pagina", 1)) - 1
    if pagina < 1:
        pagina = 1
    return redirect(url_for("index", apelido=apelido, pagina=pagina))

@app.route("/marcar_visitada", methods=["POST"])
def marcar_visitada():
    local = request.form.get("local")
    if not local:
        return ("", 204)
    marcar_visitada_db(local)
    return ("", 204)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
