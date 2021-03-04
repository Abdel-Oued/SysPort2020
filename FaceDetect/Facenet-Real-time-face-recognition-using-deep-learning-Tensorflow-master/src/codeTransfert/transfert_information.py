import json
from flask import Flask, request, Response

app = Flask(__name__)


@app.route("/")
def index():
    return "Welcome to SysPort !"


@app.route("/information/")
def information():
    # information = [{"nom": "Sunny", "prenom": "Deol", "dette": 30, "tauxAlcool": 0},
    #                {"nom": "Salman", "prenom": "Khan", "dette": 0, "tauxAlcool": 1.6}]
    # return Response(response=json.dumps(information), status=200, mimetype="application/json")

    #cas ou les infos sont enregistrées dans  un fichier
    out_file = open("information.json", "r")
    return Response(response=out_file, status=200, mimetype="application/json")


if __name__ == "__main__":
    # app.run(host="127.0.0.1", port=8080)
    app.run(host="0.0.0.0", port=8080)  # ssl_context='adhoc')  # https
