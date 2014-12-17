import config
import json

out = {}
mapWord = {}

def parse(filename):
    num_lines = 0
    num_words = 0

    try:
        with open(config.UPLOAD_FOLDER + '/' + filename, 'r') as f:
            for line in f:
                num_lines += 1
                words = line.split()
                num_words += len(words)
                populate_map(words)

            out['Number of Lines'] = num_lines
            out['Number of Words'] = num_words
            out['Word Occurrences'] = mapWord

            f.close()
            return json.dumps(out, indent = 4, separators=(',', ': '),sort_keys=True)

    except IOError:
        return 'No such file: ' + filename
    except:
        return 'Unexpected error while parsing file: ' + filename


def populate_map(words):
    for word in words:
        if mapWord.get(word) is None:
            mapWord[word] = 1
        else:
            mapWord[word] = mapWord.get(word) + 1