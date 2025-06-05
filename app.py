
from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Página inicial
@app.route("/")
def home():
    return render_template("home.html")

# Página do cliente
@app.route("/<apelido>")
def index(apelido):
    return render_template("index.html", apelido=apelido)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
