from flask import Flask, request, Response, jsonify
import pyphen
import json
from flask_cors import cross_origin

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

    # read the int from arschfragen.txt, incremnt by 1 and write it back
    with open('arschfragen.txt', 'r') as file:
        arschfragen = int(file.read())
        arschfragen += 1
        with open('arschfragen.txt', 'w') as file:
            file.write(str(arschfragen))

    return jsonify({'sylables': sylables})


@app.route('/arsch', methods=['GET'])
def arsch():
    # read the int from arschfragen.txt
    with open('arschfragen.txt', 'r') as file:
        # read all text from arschfragen.txt
        arschfragen = file.read()
        return arschfragen + " mal arschgefragt"


if __name__ == '__main__':
    app.run(debug=True)
