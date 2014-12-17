#!venv/bin/python

from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename

from os import listdir, stat
from os.path import join, isfile
from time import asctime, localtime

import config
import parser
import json


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

# Upload a file and then parse it
@app.route('/upload/', methods=['POST'])
def upload_file():
    file = request.files['file']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(join(app.config['UPLOAD_FOLDER'], filename))
        return parser.parse(filename)

    else:
        return 'Not supported file type. \n' \
               'These are the valid file extensions: \n' + \
                str(config.ALLOWED_EXTENSIONS)



# Returns list of all files that are uploaded
@app.route('/files/', methods=['GET'])
def get_all_files():
    files = [ f for f in listdir(config.UPLOAD_FOLDER) if isfile(join(config.UPLOAD_FOLDER, f)) ]
    return 'All uploaded files: \n' + '\n'.join(files)




# Returns detail info of an uploaded file
@app.route('/files/<filename>', methods=['GET'])
def get_file(filename):
    if isfile(config.UPLOAD_FOLDER + '/' + filename):
        try:
            st = stat(config.UPLOAD_FOLDER + '/' + filename)

            out = {}
            out['File Name'] = filename
            out['Size'] = st.st_size
            out['Last Access Time'] = asctime(localtime(st.st_atime))
            out['Last Modify Time'] = asctime(localtime(st.st_mtime))

            return json.dumps(out, indent = 4, separators=(',', ': '),sort_keys=True)

        except:
            return 'Failed to get information about the file: ' + filename
    else:
        return 'File not found: ' + filename + '\n'





if __name__ == '__main__':
    app.run(debug=True)