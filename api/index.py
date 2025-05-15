import io
from flask import Flask, request, Response, jsonify
import pyphen
from flask_cors import cross_origin
from werkzeug.utils import secure_filename
import os
from flask import send_file
import fitz  # PyMuPDF

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


def verarschen(data, arschfaktor, respectFirstArsch=True):
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
            "als": "als",
            "maschinenbau": "arschbau",
            "maschbau": "arschbau",
            "ag" : "arschg",
            "gmbh": "gmbharsch",
        }

        for sylable in data["sylables"]:
            # split word into syllables "Hal-lo" -> ["Hal", "lo"]
            sylables = sylable.split("-")
            word = "".join(sylables)

            if not word:
                continue  # Skip empty words

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

            for j in range(1, len(sylables)):
                if respectFirstArsch and "arsch" in sylables[0].lower():
                    break
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
    respectFirstArsch = data.get('respectFirstArsch', True)
    dic = pyphen.Pyphen(lang='de_DE')
    words = text.split()
    sylables = []
    for word in words:
        sylable = dic.inserted(word)
        sylables.append(sylable)

    arsch = verarschen(data={'sylables': sylables}, arschfaktor=arschfaktor, respectFirstArsch=respectFirstArsch)
    return Response(arsch, mimetype='application/text; charset=utf-8')

@app.route('/v1/massenverarschung', methods=['POST'])
@cross_origin()
def mass_verarscher():
    data = request.get_json()
    texts = data.get('texts', [])
    arschfaktor = data.get('arschfaktor', 6)
    respectFirstArsch = data.get('respectFirstArsch', True)
    results = []
    for text in texts:
        dic = pyphen.Pyphen(lang='de_DE')
        words = text.split()
        sylables = []
        for word in words:
            sylable = dic.inserted(word)
            sylables.append(sylable)

        arsch = verarschen(data={'sylables': sylables}, arschfaktor=arschfaktor, respectFirstArsch=respectFirstArsch)
        results.append(arsch)
    # return the results as a json object
    return jsonify({'results': results})

@app.route('/arsch', methods=['GET'])
def arsch():
    return "Arsch!"

@app.route('/v1/arschPDF', methods=['POST'])
@cross_origin()
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    temp_path = os.path.join('/tmp', filename)
    file.save(temp_path)

    try:
        doc = fitz.open(temp_path)
        print("pdf opened.")

        # 1) Alle Text-Spans einsammeln
        spans = []
        for page_num, page in enumerate(doc):
            blocks = page.get_text("dict")["blocks"]
            for b in blocks:
                if "lines" not in b:
                    continue  # Skip non-text blocks
                for line in b["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if not text:
                            continue
                        spans.append({
                            "page": page_num,
                            "bbox": span["bbox"],
                            "size": span["size"],
                            "font": span["font"],
                            "orig": text
                        })


        print("Text-Spans done.")

        # 2) Batch-Übersetzung anfragen
        texts = [s["orig"] for s in spans]
        #resp = requests.post(API_URL, json={"texts": texts, "target": TARGET_LANG})
        
        # verarsch all texts using verarschen function 
        results = []

        for text in texts:
            dic = pyphen.Pyphen(lang='de_DE')
            words = text.split()
            sylables = []
            for word in words:
                sylable = dic.inserted(word)
                sylables.append(sylable)

            arsch = verarschen(data={'sylables': sylables}, arschfaktor=6, respectFirstArsch=True)
            results.append(arsch)

        print("Verarschung done.")

        # 3) Redaktionen setzen
        for span in spans:
            page = doc[span["page"]]
            rect = fitz.Rect(span["bbox"])
            page.add_redact_annot(rect, fill=(1,1,1))
        
        for page in doc:
            page.apply_redactions()

        print("Redaktionen done.")

        # 4) Übersetzte Texte einfügen
        for idx, span in enumerate(spans):
            page = doc[span["page"]]
            x0, y0, x1, y1 = span["bbox"]
            insert_point = fitz.Point(x0, y1)
            page.insert_text(
                insert_point,
                results[idx],
                fontsize=span["size"]
                #fontname=span["font"]
            )

        print("Text einfügen done.")

        # 5) PDF-Bytes erzeugen und zurückliefern
        out = io.BytesIO()
        doc.save(out)
        out.seek(0)

        print("byte write done.")
        return Response(out.read(), mimetype='application/pdf')
        
    except Exception as e:
        print(f"Error processing PDF: {e}")
        os.remove(temp_path)
        print("Temp file deleted.")

        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)
            print("Temp file deleted.")

        


if __name__ == '__main__':
    app.run(debug=True)
