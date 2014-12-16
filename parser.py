import config

map = {}

def parse(filename):
    num_lines = 0
    num_words = 0

    with open(config.UPLOAD_FOLDER + '/' + filename, 'r') as f:
        for line in f:
            num_lines += 1
            words = line.split()
            num_words += len(words)
            populate_map(words)
        return str(map)
        #return str(num_lines) + ', ' + str(num_words)


def populate_map(words):
    for word in words:
        if map.get(word) is None:
            map[word] = 1
        else:
            map[word] = map.get(word) + 1