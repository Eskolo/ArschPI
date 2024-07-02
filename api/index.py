from flask import Flask, request, Response, jsonify
import pyphen
import os
import sys
from flask_cors import cross_origin

sys.path.append(os.path.dirname(__file__))
from verarscher import verarschen

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/v1/hyphenation', methods=['POST'])
@cross_origin()
def hyphenation():
    data = request.get_json()
    print(data)
    text = data.get('text', '')
    dic = pyphen.Pyphen(lang='de_DE')
    words = text.split()
    sylables = []
    for word in words:
        sylable = dic.inserted(word)
        sylables.append(sylable)

    return jsonify({'sylables': sylables})

@app.route('/v1/verarscher', methods=['POST'])
@cross_origin()
def verarscher():
    data = request.get_json()
    print(data)
    text = data.get('text', '')
    arschfaktor = data.get('arschfaktor', 6)
    dic = pyphen.Pyphen(lang='de_DE')
    words = text.split()
    sylables = []
    for word in words:
        sylable = dic.inserted(word)
        sylables.append(sylable)

    arsch = verarschen(data={'sylables': sylables}, arschfaktor=arschfaktor)
    return jsonify(arsch)

@app.route('/arsch', methods=['GET'])
def arsch():
    return "Arsch!"

if __name__ == '__main__':
    app.run(debug=True)
