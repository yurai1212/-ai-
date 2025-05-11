
from flask import Flask, render_template, request, redirect, url_for
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

animals = ['ネコ', 'イヌ', 'アルパカ', 'ナマケモノ', 'オポッサム']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return '画像がありません', 400
    file = request.files['image']
    if file.filename == '':
        return 'ファイル名が空です', 400

    filename = secure_filename(file.filename)
    ext = os.path.splitext(filename)[1]
    uid = str(uuid.uuid4())
    saved_filename = uid + ext
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], saved_filename)
    file.save(save_path)

    import random
    animal = random.choice(animals)

    return render_template('result.html', result={
        'animal_name': animal,
        'filename': saved_filename
    })

@app.route('/gallery')
def gallery():
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    return "<br>".join(images)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
