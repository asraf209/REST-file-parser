#!venv/bin/python

from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename

from os import listdir
from os.path import join, isfile

import config
import parser
from utility import allowed_file, get_info, json_dumps


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = config.MAX_FILE_SIZE


@app.route('/')
def index():
    return "I am running!"


# Upload a file and then parse it
@app.route('/upload/', methods=['POST'])
def upload_file():
    file = request.files['file']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(join(app.config['UPLOAD_FOLDER'], filename))
        map = parser.parse(filename)
        return json_dumps(map)

    else:
        return 'Not supported file type. \n' \
               'These are the valid file extensions: \n' + \
                str(config.ALLOWED_EXTENSIONS)



# Returns list of all files that are uploaded
@app.route('/files/', methods=['GET'])
def get_all_files():
    files = [ f for f in listdir(config.UPLOAD_FOLDER) if isfile(join(config.UPLOAD_FOLDER, f)) ]
    filelist = []
    for filename in files:
        out = get_info(filename)
        filelist.append(out)
    return json_dumps(filelist)



# Returns detail info of an uploaded file
@app.route('/files/<filename>', methods=['GET'])
def get_file(filename):
    if isfile(config.UPLOAD_FOLDER + '/' + filename):
        try:
            out = get_info(filename)
            return json_dumps(out)

        except:
            return 'Failed to get information about the file: ' + filename
    else:
        return 'File not found: ' + filename + '\n'



if __name__ == '__main__':
    app.run(debug=True)