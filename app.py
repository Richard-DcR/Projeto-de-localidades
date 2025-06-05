
from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'chave-secreta-sessao'

# Colors cycle for locality boxes: green, cyan, orange
cores_localidades = ["#90ee90", "#00ffff", "#ffa500"]

# Clients (use your original provided list)
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
    "angelo": "Vinicius Silva"}

# Load localidades
with open("localidades.txt", encoding="utf-8") as f:
    todas_localidades = [linha.strip() for linha in f if linha.strip()]

total_localidades = len(todas_localidades)
# Number of pages (100 items per page)
total_paginas = (total_localidades + 99) // 100

# Visitadas file
visitadas_path = "visitadas.txt"
if not os.path.exists(visitadas_path):
    open(visitadas_path, "w", encoding="utf-8").close()

def ler_visitadas():
    with open(visitadas_path, encoding="utf-8") as f:
        return set(l.strip() for l in f if l.strip())

def salvar_visitadas(visitadas):
    with open(visitadas_path, "w", encoding="utf-8") as f:
        for v in sorted(visitadas):
            f.write(v + "\n")

@app.route("/")
def home():
    return render_template("home.html", clientes=clientes)

@app.route("/<apelido>", methods=["GET", "POST"])
def index(apelido):
    if apelido not in clientes:
        return redirect(url_for("home"))

    prefix = f"{apelido}_"

    # Initialize session values
    if prefix + "pagina" not in session:
        session[prefix + "pagina"] = 1
        session[prefix + "resets"] = 0

    # Handle reset
    if request.method == "POST" and request.form.get("reset") == "1":
        session[prefix + "pagina"] = 1
        session[prefix + "resets"] = 0

    pagina = session[prefix + "pagina"]
    resets = session[prefix + "resets"]

    # Slice of items
    inicio = (pagina - 1) * 100
    fim = inicio + 100
    itens = todas_localidades[inicio:fim]

    # Determine box color: only based on full cycles (resets)
    cor = cores_localidades[resets % len(cores_localidades)]

    visitadas = ler_visitadas()
    nome_cliente = clientes[apelido]

    return render_template("index.html",
                           apelido=apelido,
                           nome=nome_cliente,
                           itens=itens,
                           visitadas=visitadas,
                           pagina_atual=pagina,
                           total_paginas=total_paginas,
                           cor_localidade=cor)

@app.route("/proxima_pagina/<apelido>")
def proxima_pagina(apelido):
    prefix = f"{apelido}_"
    pagina = session.get(prefix + "pagina", 1) + 1
    if pagina > total_paginas:
        # Completed full cycle
        pagina = 1
        session[prefix + "resets"] = session.get(prefix + "resets", 0) + 1
    session[prefix + "pagina"] = pagina
    return redirect(url_for("index", apelido=apelido))

@app.route("/pagina_anterior/<apelido>")
def pagina_anterior(apelido):
    prefix = f"{apelido}_"
    pagina = session.get(prefix + "pagina", 1) - 1
    if pagina < 1:
        pagina = 1
    session[prefix + "pagina"] = pagina
    return redirect(url_for("index", apelido=apelido))

@app.route("/marcar_visitada", methods=["POST"])
def marcar_visitada():
    local = request.form.get("local")
    if not local:
        return "", 204
    visitadas = ler_visitadas()
    if local in visitadas:
        visitadas.remove(local)
    else:
        visitadas.add(local)
    salvar_visitadas(visitadas)
    return "", 204

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
