
from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Lista de clientes exata conforme você enviou
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

# Garante que o arquivo visitadas.txt exista
visitadas_path = "visitadas.txt"
if not os.path.exists(visitadas_path):
    open(visitadas_path, "w", encoding="utf-8").close()

def ler_visitadas():
    """Retorna um set com os nomes de todas as localidades marcadas como visitadas."""
    with open(visitadas_path, encoding="utf-8") as f:
        return set(linha.strip() for linha in f if linha.strip())

def salvar_visitadas(visitadas):
    """Grava no arquivo visitadas.txt a lista (ordenada) de locais visitados."""
    with open(visitadas_path, "w", encoding="utf-8") as f:
        for v in sorted(visitadas):
            f.write(v + "\n")

@app.route("/")
def home():
    # Passa a lista de clientes para o template home.html
    return render_template("home.html", clientes=clientes)

@app.route("/<apelido>", methods=["GET", "POST"])
def index(apelido):
    if apelido not in clientes:
        return redirect(url_for("home"))

    # Se o formulário POST enviar reset=1, volta à página 1
    if request.method == "POST" and request.form.get("reset") == "1":
        return redirect(url_for("index", apelido=apelido, pagina=1))

    # Número da página atual via query string ?pagina=X (default=1)
    pagina = int(request.args.get("pagina", 1))
    if pagina < 1:
        pagina = 1
    if pagina > total_paginas:
        pagina = total_paginas

    # Define slice de 100 localidades
    inicio = (pagina - 1) * 100
    fim = inicio + 100
    itens = todas_localidades[inicio:fim]

    # Ciclo de cores: verde, ciano, laranja a cada 7 páginas (700 itens)
    cores_ciclo = ["#90ee90", "#00ffff", "#ffa500"]
    ciclo_index = (pagina - 1) // 7
    cor_localidade = cores_ciclo[ciclo_index % len(cores_ciclo)]

    # Carrega as localidades já marcadas como visitadas
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
    # Avança uma página e redireciona
    pagina = int(request.args.get("pagina", 1)) + 1
    return redirect(url_for("index", apelido=apelido, pagina=pagina))

@app.route("/pagina_anterior/<apelido>")
def pagina_anterior(apelido):
    # Retrocede uma página e redireciona
    pagina = int(request.args.get("pagina", 1)) - 1
    if pagina < 1:
        pagina = 1
    return redirect(url_for("index", apelido=apelido, pagina=pagina))

@app.route("/marcar_visitada", methods=["POST"])
def marcar_visitada():
    # Recebe o nome da localidade via form e faz toggle na lista global
    local = request.form.get("local")
    if not local:
        return ("", 204)

    visitadas = ler_visitadas()
    if local in visitadas:
        visitadas.remove(local)
    else:
        visitadas.add(local)
    salvar_visitadas(visitadas)
    return ("", 204)

if __name__ == "__main__":
    # Usa porta definida pela variável de ambiente (padrão do Render e similares)
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
