import os
import threading
import time
import tempfile
from flask import Flask, render_template, request, jsonify, send_file
from googletrans import Translator, LANGUAGES
from gtts import gTTS

app = Flask(__name__, static_url_path='/static')
is_playing = False


@app.route('/', methods=['GET', 'POST'])
def home():
    languages = {code: name.capitalize() for code, name in LANGUAGES.items()}

    if request.method == 'POST':
        sentence = request.form.get("sentence")
        language = request.form.get("inputvalue")
        output = Translator().translate(sentence, dest=language).text
    else:
        sentence = ""
        language = ""
        output = ""

    return render_template('index.html', output=output, sentence=sentence, language=language, languages=languages)


@app.route('/play-text', methods=['POST'])
def play_text():
    text = request.form.get("text")

    if not text:
        return jsonify({'status': 'Error', 'message': 'No text to speak'})

    # Convert text to speech using gTTS
    tts = gTTS(text=text, lang='en')
    temp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    temp_filename = temp_file.name
    tts.save(temp_filename)

    # Stream the audio file to the client
    return send_file(temp_filename, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
