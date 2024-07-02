from flask import Flask, request, Response, jsonify
import pyphen
from flask_cors import cross_origin

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


def verarschen(data, arschfaktor):
    if "sylables" in data and isinstance(data["sylables"], list):
        # create word array
        words = []
        arschterbuch = {
            "öller": "öllarsch",
            "bundeskanzler": "bundesarschler",
            "grüße": "arsch",
            "oth": "otharsch",
            "connecta": "cocknectarsch",
            "hauptquartier": "hauptquarschtier",
            "an": "an",
            "am": "am",
            "maschinenbau": "arschbau",
            "maschbau": "arschbau",
        }

        for sylable in data["sylables"]:
            # split word into syllables "Hal-lo" -> ["Hal", "lo"]
            sylables = sylable.split("-")
            word = "".join(sylables)

            # if the word contains already arsch, skip
            if "arsch" in word.lower():
                words.append(word)
                continue

            is_upper = word[0].isupper()
            arsch_char = None

            # strip special characters from the word
            last_char = word[-1]
            if last_char in [".", ",", "!", "?"]:
                word = word[:-1]
                arsch_char = last_char

            # check if the word is in the arschterbuch
            if word.lower() in arschterbuch:
                arsch_word = arschterbuch[word.lower()]
                if is_upper:
                    arsch_word = arsch_word[0].upper() + arsch_word[1:]
                if arsch_char:
                    arsch_word += arsch_char
                words.append(arsch_word)
                continue

            # check first syllable
            first_syl = sylables[0].lower()
            if "a" in first_syl:
                if len(first_syl) == 2 and first_syl.startswith("a"):
                    sylables[0] = "arsch"
                else:
                    if "au" not in first_syl:
                        index = first_syl.index("a")
                        last_index = len(first_syl) - 1

                        if index == last_index:
                            sylables[0] = sylables[0].replace("a", "arsch")
                        elif index == 0:
                            sylables[0] = "arsch" + first_syl[2:]
                        else:
                            sylables[0] = first_syl[:index] + \
                                "arsch" + first_syl[index + 2:]

            if "arsch" not in sylables[0].lower():
                for j in range(1, len(sylables)):
                    if len(sylables) <= arschfaktor and "a" in sylables[j]:
                        sylables[j] = sylables[j].replace("a", "arsch")
                        break
                    else:
                        sylables[j] = sylables[j].replace("a", "arsch")

            word = "".join(sylables).lower()

            if arsch_char and word[-1] != arsch_char:
                word += arsch_char

            if word.endswith("arschh"):
                word = word[:-1]
            if word.endswith("arschch"):
                word = word[:-2]
            if word.endswith("arschsch"):
                word = word[:-3]
            if word.startswith("aus"):
                word = word.replace("aus", "arsch")

            if is_upper:
                word = word[0].upper() + word[1:]

            words.append(word)

        output = " ".join(words)
        print(output)
        return output


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
