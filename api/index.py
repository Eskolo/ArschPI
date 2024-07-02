from flask import Flask, request, Response, jsonify
import pyphen
import json
from flask_cors import cross_origin

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/hyphenation', methods=['POST'])
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

    data = {'sylables': sylables}
    json_string = json.dumps(data,ensure_ascii = False)
    #creating a Response object to set the content type and the encoding
    response = Response(json_string,content_type="application/json; charset=utf-8" )
    # add corse header
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/get-hyphenation', methods=['GET'])
def hyphenation():
    text = request.args.get('text', '')
    print(text)
    dic = pyphen.Pyphen(lang='de_DE')
    words = text.split()
    sylables = []
    for word in words:
        sylable = dic.inserted(word)
        sylables.append(sylable)

    data = {'sylables': sylables}
    json_string = json.dumps(data, ensure_ascii=False)
    # Creating a Response object to set the content type and the encoding
    response = Response(json_string, content_type="application/json; charset=utf-8")
    # Add CORS header
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/arsch', methods=['POST'])
def arsch():
    return "Arsch!"

if __name__ == '__main__':
    app.run(debug=True)