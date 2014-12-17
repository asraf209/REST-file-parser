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



