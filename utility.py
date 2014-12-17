#!venv/bin/python

import config
import json
from time import asctime, localtime
from os import stat


def json_dumps(map):
    return json.dumps(map, indent = 4, separators=(',', ': '),sort_keys=True)



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in config.ALLOWED_EXTENSIONS



def get_info(filename):
    st = stat(config.UPLOAD_FOLDER + '/' + filename)

    out = {}
    out['File Name'] = filename
    out['Size'] = st.st_size
    out['Last Access Time'] = asctime(localtime(st.st_atime))
    out['Last Modify Time'] = asctime(localtime(st.st_mtime))

    return out



def remove_from_map(map, word):
    if word is None or word.strip() == '':
        return map
    else:
        word = word.strip()
        for key in map['Words'].keys():
            if word in key:
                del map['Words'][key]



def include_only(map, word):
    if word is None or word.strip() == '':
        return map
    else:
        word = word.strip()
        for key in map['Words'].keys():
            if word not in key:
                del map['Words'][key]