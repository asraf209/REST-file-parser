#!venv/bin/python

import config

out = {}
mapWord = {}

def parse(filename):
    num_lines = 0
    num_words = 0

    try:
        with open(config.UPLOAD_FOLDER + '/' + filename, 'r') as file:
            for line in file:
                num_lines += 1
                words = line.split()
                num_words += len(words)
                add_to_map(words)

            out['File Name'] = filename
            out['Number of Lines'] = num_lines
            out['Number of Words'] = num_words
            out['Words'] = mapWord

            file.close()
            return out

    except IOError:
        return 'No such file: ' + filename
    except:
        return 'Unexpected error while parsing file: ' + filename


def add_to_map(words):
    for word in words:
        if mapWord.get(word) is None:
            mapWord[word] = 1
        else:
            mapWord[word] = mapWord.get(word) + 1