
from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

clientes = {
    "adryan": "Adryan",
    "arthur": "Arthur",
    "brendo": "Brendo",
    "felipe": "Felipe",
    "lucas": "Lucas"
}

# Load localidades
with open("localidades.txt", encoding="utf-8") as f:
    todas_localidades = [linha.strip() for linha in f if linha.strip()]
total_localidades = len(todas_localidades)
total_paginas = (total_localidades + 99) // 100

@app.route("/")
def home():
    return render_template("home.html", clientes=clientes)

@app.route("/<apelido>")
def index(apelido):
    pagina = int(request.args.get("pagina", 1))
    if pagina < 1:
        pagina = 1
    if pagina > total_paginas:
        pagina = total_paginas

    inicio = (pagina - 1) * 100
    fim = inicio + 100
    itens = todas_localidades[inicio:fim]

    cor_localidade = "#90ee90"  # default green
    visitadas = []  # opcional, não implementado persistente neste exemplo

    nome_cliente = clientes.get(apelido, "Desconhecido")

    return render_template("index.html",
                           apelido=apelido,
                           nome=nome_cliente,
                           itens=itens,
                           visitadas=visitadas,
                           pagina_atual=pagina,
                           total_paginas=total_paginas,
                           cor_localidade=cor_localidade)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
