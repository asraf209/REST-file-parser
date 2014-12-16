import config

def count_lines(filename):
    num_lines = 0
    num_words = 0

    with open(config.UPLOAD_FOLDER + '/' + filename, 'r') as f:
        for line in f:
            words = line.split()

            num_lines += 1
            num_words += len(words)
        return str(num_lines) + ', ' + str(num_words)