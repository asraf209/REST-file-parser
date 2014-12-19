#!venv/bin/python
# Configuration file for setting up various system wide properties

MAX_FILE_SIZE = 10 * 1024 * 1024        # 10MB
UPLOAD_FOLDER = 'uploads'               # Directory for uploaded files

TRAILING_CHARACTERS = (',', '.', ';', '!', '=')
ALLOWED_EXTENSIONS  = set(['txt','log', 'md', 'rst'])

FILE_NAME  = 'File Name'
LINE_COUNT = 'Line Count'
WORD_COUNT = 'Word Count'
WORD_LIST  = 'Word List'
SIZE       = 'Size'
LAST_ACCESS_TIME = 'Last Access Time'
LAST_MODIFY_TIME = 'Last Modify Time'