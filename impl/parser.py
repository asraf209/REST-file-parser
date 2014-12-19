#!venv/bin/python
# Parser to parse a text file and
# then count lines, words and word frequencies

import config as cfg

# Read a file, count lines and individual word
def parse(filename):
    out = {}                # Final JSON response
    mapWord = {}            # HashMap of <word, frequency>

    num_lines = 0           # Number of lines
    num_words = 0           # Number of words

    try:
        with open(cfg.UPLOAD_FOLDER + '/' + filename, 'r') as file:
            for line in file:                           # For each line
                num_lines += 1
                words = line.split()                    # split a line into words
                num_words += len(words)
                add_to_map(mapWord, words)              # put all words into HashMap.

            out[cfg.FILE_NAME] = filename
            out[cfg.LINE_COUNT] = num_lines
            out[cfg.WORD_COUNT] = num_words
            out[cfg.WORD_LIST] = mapWord

            file.close()
            return out

    except IOError:
        return 'No such file: ' + filename
    except:
        return 'Unexpected error while parsing file: ' + filename



# Put all words into HashMap.
# Also update frequency as necessary
def add_to_map(mapWord, words):
    for word in words:
        word = word.lower()
        if word[-1:] in cfg.TRAILING_CHARACTERS:           # Remove trailing characters (, . ; !)
            word = word[:-1]
        if mapWord.get(word) is None:
            mapWord[word] = 1
        else:
            mapWord[word] = mapWord.get(word) + 1