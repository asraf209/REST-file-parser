#!venv/bin/python
# Provides handy methods to modularize specific task

import json
import config as cfg
from time import asctime, localtime
from os import stat


# Converts a HashMap into JSON format
def json_dumps(map):
    return json.dumps(map, indent = 4, separators=(',', ': '),sort_keys=True)



# Check extension for allowable file types
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in cfg.ALLOWED_EXTENSIONS



# Get metadata of a file
def get_info(filename):
    st = stat(cfg.UPLOAD_FOLDER + '/' + filename)
    out = {}
    out[cfg.FILE_NAME] = filename
    out[cfg.SIZE] = st.st_size
    out[cfg.LAST_ACCESS_TIME] = asctime(localtime(st.st_atime))
    out[cfg.LAST_MODIFY_TIME] = asctime(localtime(st.st_mtime))
    return out



# Remove a word from HashMap, who has a matching substring
def remove_from_map(map, substr):
    if substr is None or substr.strip() == '':
        return map
    else:
        substr = substr.strip()
        for word in map[cfg.WORD_LIST].keys():
            if substr in word:
                del map[cfg.WORD_LIST][word]



# Keep only those words who contain a specific substring.
# Remove all the rest
def keep_only(map, substr):
    if substr is None or substr.strip() == '':
        return map
    else:
        substr = substr.strip()
        for word in map[cfg.WORD_LIST].keys():
            if substr not in word:
                del map[cfg.WORD_LIST][word]