
from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Lista de clientes conforme enviada
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

# Carrega todas as localidades do arquivo localidades.txt
with open("localidades.txt", encoding="utf-8") as f:
    todas_localidades = [linha.strip() for linha in f if linha.strip()]
total_localidades = len(todas_localidades)
total_paginas = (total_localidades + 99) // 100

# Rota da página inicial (lista de clientes)
@app.route("/")
def home():
    return render_template("home.html", clientes=clientes)

# Rota principal de listagem de localidades para cada cliente
@app.route("/<apelido>", methods=["GET", "POST"])
def index(apelido):
    if apelido not in clientes:
        return redirect(url_for("home"))

    # Se houver um POST com reset, volta à página 1
    if request.method == "POST" and request.form.get("reset") == "1":
        return redirect(url_for("index", apelido=apelido, pagina=1))

    # Obter número da página pela query string (?pagina=...)
    pagina = int(request.args.get("pagina", 1))
    if pagina < 1:
        pagina = 1
    if pagina > total_paginas:
        pagina = total_paginas

    # Calcula o slice de 100 localidades a exibir
    inicio = (pagina - 1) * 100
    fim = inicio + 100
    itens = todas_localidades[inicio:fim]

    # Cor fixa (green) – ajuste o ciclo de 700 conforme queira
    cor_localidade = "#90ee90"

    # Lista (temporária) de "visitadas" (ainda não persistente neste exemplo)
    visitadas = []

    nome_cliente = clientes.get(apelido, "Desconhecido")

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

# Botão “Próxima Página”
@app.route("/proxima_pagina/<apelido>")
def proxima_pagina(apelido):
    pagina = int(request.args.get("pagina", 1)) + 1
    return redirect(url_for("index", apelido=apelido, pagina=pagina))

# Botão “Página Anterior”
@app.route("/pagina_anterior/<apelido>")
def pagina_anterior(apelido):
    pagina = int(request.args.get("pagina", 1)) - 1
    if pagina < 1:
        pagina = 1
    return redirect(url_for("index", apelido=apelido, pagina=pagina))

# Marca/desmarca uma localidade como visitada
@app.route("/marcar_visitada", methods=["POST"])
def marcar_visitada():
    local = request.form.get("local")
    if not local:
        return "", 204
    # (aqui você pode implementar a lógica de persistência em visitadas.txt)
    return "", 204

if __name__ == "__main__":
    # Porta definida pela variável de ambiente (Render, Heroku etc.)
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
