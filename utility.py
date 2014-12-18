#!venv/bin/python
# Provides handy methods to modularize specific task

import config
import json
from time import asctime, localtime
from os import stat


# Converts a HashMap into JSON format
def json_dumps(map):
    return json.dumps(map, indent = 4, separators=(',', ': '),sort_keys=True)


# Check extension for allowable file types
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in config.ALLOWED_EXTENSIONS


# Get metadata of a file
def get_info(filename):
    st = stat(config.UPLOAD_FOLDER + '/' + filename)
    out = {}
    out['File Name'] = filename
    out['Size'] = st.st_size
    out['Last Access Time'] = asctime(localtime(st.st_atime))
    out['Last Modify Time'] = asctime(localtime(st.st_mtime))
    return out


# Remove a matching word from HashMap
def remove_from_map(map, word):
    if word is None or word.strip() == '':
        return map
    else:
        word = word.strip()
        for key in map['Words'].keys():
            if word in key:
                del map['Words'][key]


# Keep only those words who contain a specific substring.
# Remove all the rest
def include_only(map, word):
    if word is None or word.strip() == '':
        return map
    else:
        word = word.strip()
        for key in map['Words'].keys():
            if word not in key:
                del map['Words'][key]