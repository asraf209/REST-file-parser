#!venv/bin/python

from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename

import os
import config
import parser


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = config.MAX_FILE_SIZE

@app.route('/')
def index():
    return "I am running!"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in config.ALLOWED_EXTENSIONS


'''def allowed_file(filename):
    if '.' in filename:
           return filename.rsplit('.', 1)[1] in config.ALLOWED_EXTENSIONS

    # Providing support for files with no extension
    # I am assuming they will mostly be unix text files
    return True
'''

@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return parser.parse(filename)

        else:
            return 'Not supported file type. \n' \
                   'These are the valid file extensions: \n' + \
                    str(config.ALLOWED_EXTENSIONS)
    return ''


if __name__ == '__main__':
    app.run(debug=True)