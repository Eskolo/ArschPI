from flask import Flask, request, Response, jsonify
import pyphen
import json
from flask_cors import cross_origin

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

arsch = {}

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

    # check if cache is initialized
    if 'arsch' not in arsch:
        arsch['arsch'] = 0

    arsch['arsch'] = arsch['arsch'] + 1

    return jsonify({'sylables': sylables})


@app.route('/arsch', methods=['GET'])
def arsch():
    return str(arsch['arsch']) + " mal arschgefragt"
        


if __name__ == '__main__':
    app.run(debug=True)
