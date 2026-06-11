from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import uuid

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

USUARIOS_FILE = "usuarios.json"
LANCA_FILE = "banco.json"


# =========================
# HELPERS USUARIOS
# =========================
def ler_usuarios():
    try:
        with open(USUARIOS_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def salvar_usuarios(dados):
    with open(USUARIOS_FILE, "w") as f:
        json.dump(dados, f, indent=2)


# =========================
# USUARIOS
# =========================
@app.route("/usuarios", methods=["POST"])
def usuarios():
    data = request.get_json()

    usuarios = ler_usuarios()
    usuarios.append(data)
    salvar_usuarios(usuarios)

    return jsonify({"mensagem": "Usuário salvo!"})


# =========================
# HELPERS LANÇAMENTOS
# =========================
def ler_lancamentos():
    try:
        with open(LANCA_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def salvar_lancamentos(dados):
    with open(LANCA_FILE, "w") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


# =========================
# LANÇAMENTOS - GET
# =========================
@app.route("/lancamentos", methods=["GET"])
def get_lancamentos():
    return jsonify(ler_lancamentos())


# =========================
# LANÇAMENTOS - POST
# =========================
@app.route("/lancamentos", methods=["POST"])
def add_lancamento():
    dados = ler_lancamentos()
    novo = request.get_json()

    if not novo:
        return jsonify({"status": "erro"}), 400

    novo["id"] = str(uuid.uuid4())
    dados.append(novo)

    salvar_lancamentos(dados)

    return jsonify({"status": "ok"})


# =========================
# LANÇAMENTOS - DELETE
# =========================
@app.route("/lancamentos/<id>", methods=["DELETE"])
def deletar(id):
    dados = ler_lancamentos()

    novos = [d for d in dados if d.get("id") != id]

    salvar_lancamentos(novos)

    return jsonify({"status": "ok"})


# =========================
# LANÇAMENTOS - PUT
# =========================
@app.route("/lancamentos/<id>", methods=["PUT"])
def editar(id):
    dados = ler_lancamentos()
    atualizado = request.get_json()

    for d in dados:
        if d.get("id") == id:
            d.update(atualizado)
            break

    salvar_lancamentos(dados)

    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)