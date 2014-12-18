#!venv/bin/python
# Main entry point of the application.
# Provides various end points

from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename

from os import listdir
from os.path import join, isfile

import config
import parser
from utility import allowed_file, get_info, json_dumps, remove_from_map, keep_only


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = config.MAX_FILE_SIZE


# Home page
@app.route('/')
def index():
    return "I am running!"


# Upload a file and parse
@app.route('/upload/', methods=['POST'])
def upload_file():
    file = request.files['file']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(join(app.config['UPLOAD_FOLDER'], filename))      # Save the file in upload directory
        map = parser.parse(filename)                                # Parse and get word frequencies in a HashMap
        return json_dumps(map)                                      # Return the responses as JSON format

    else:
        return 'Not supported file type. \n' \
               'These are the valid file extensions: \n' + \
                str(config.ALLOWED_EXTENSIONS)


# Returns list of all files that are uploaded,
# with their metadata
@app.route('/files/', methods=['GET'])
def get_all_files():
    files = [ f for f in listdir(config.UPLOAD_FOLDER) if isfile(join(config.UPLOAD_FOLDER, f)) ]
    filelist = []
    for filename in files:
        out = get_info(filename)                # Get metadata of a file
        filelist.append(out)                    # And append those info into a list
    return json_dumps(filelist)                 # Returns response as JSON


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


# Parse and get word count for any specific file that has already been uploaded.
# Can take parameters; like;
# a matching string that must be in a word, and/or
# a matching string that should not be in a word
@app.route('/parse/<filename>', methods=['GET'])
def parse_file(filename):
    if isfile(config.UPLOAD_FOLDER + '/' + filename):
        map = parser.parse(filename)

        wordToRemove = request.args.get('discard', None)
        remove_from_map(map, wordToRemove)                          # Remove all words from HashMap who has a substring same as wordToRemove

        wordToInclude = request.args.get('only', None)
        keep_only(map, wordToInclude)                               # Only keep those words who has a substring same as wordToInclude

        return json_dumps(map)
    else:
        return 'File not found: ' + filename + '\n'



if __name__ == '__main__':
    app.run(debug=True)