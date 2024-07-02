from flask import Flask, request, Response, jsonify
import pyphen
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/hyphenation', methods=['POST'])
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

    data = {'sylables': sylables}
    json_string = Flask.json.dumps(data,ensure_ascii = False)
    #creating a Response object to set the content type and the encoding
    response = Response(json_string,content_type="application/json; charset=utf-8" )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/arsch', methods=['POST'])
def arsch():
    return "Arsch!"

if __name__ == '__main__':
    app.run(debug=True)