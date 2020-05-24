import flask
from flask import Flask, request, jsonify
import crawling

app = Flask(__name__)
 
# 파일 경로를 받아서 load 한 data를 return
def readjson(filename):
    with open(filename, 'rt', encoding='UTF8') as file:
        data = flask.json.load(file)

    return data

@app.route("/api/<name>")
def data(name):
    return flask.jsonify(readjson("data/" + name + ".json"))

if __name__ == "__main__":
    app.run()