#!venv/bin/python

import unittest
import fileparser
from StringIO import StringIO
import json

class FileParserTestCase(unittest.TestCase):

    def setUp(self):
        fileparser.app.config['TESTING'] = True
        self.app = fileparser.app.test_client()


    # Test '404 Not Found'
    def test_url_not_found(self):
        response = self.app.get('/foo')
        self.assertFalse(response.status_code == 200)
        self.assertTrue(response.status_code == 404, msg='URL Not Found')


    # Test Root of the application
    def test_root(self):
        response = self.app.get('/')
        self.assertTrue(response.status_code == 200, msg='GET request works fine')
        self.assertTrue("I am running!" in response.data)


    # Test uploading a file
    def test_upload(self):
        response = self.app.post('/upload',
                    data={'file':(StringIO('Hello world, hello all!'), 'test.txt')})
        self.assertTrue(response.status_code == 200, msg='POST request works fine')
        data = json.loads(response.data)

        self.assertEqual(data['File Name'], 'test.txt')
        self.assertEqual(data['Number of Lines'], 1)
        self.assertEqual(data['Number of Words'], 4)
        self.assertEqual(data['Words']['hello'], 2)
        self.assertEqual(data['Words']['world'], 1)
        self.assertEqual(data['Words']['all'], 1)


    # Try to upload an unsupported file type
    def test_not_supported_file_type(self):
        response = self.app.post('/upload',
                    data={'file':(StringIO('We are sample contents'), 'test.foo')})
        self.assertTrue(response.status_code == 200, msg='POST request works fine')
        self.assertTrue('Not a supported file type' in response.data)


    # Test uploading a blank file
    def test_upload_a_blank_file(self):
        response = self.app.post('/upload',
                    data={'file':(StringIO(''), 'test-blank.txt')})
        self.assertTrue(response.status_code == 200, msg='POST request works fine')
        data = json.loads(response.data)

        self.assertEqual(data['File Name'], 'test-blank.txt')
        self.assertEqual(data['Number of Lines'], 0)
        self.assertEqual(data['Number of Words'], 0)


    # Check list of files that are already been uploaded
    def test_list_of_files(self):
        response = self.app.get('/files')
        self.assertTrue(response.status_code == 200, msg='GET request works fine')
        data = json.loads(response.data)
        self.assertTrue(len(data) > 0, msg='Possibly there are few uploaded files')


    # Read a file metadata
    def test_file_metadata(self):
        response = self.app.get('/files/jingle.txt')          # 'jingle.txt' is already uploaded onto the 'uploads' folder
        self.assertTrue(response.status_code == 200, msg='GET request works fine')
        data = json.loads(response.data)
        self.assertTrue(data['File Name'] == 'jingle.txt')
        self.assertTrue(data['Size'] == 413, msg='File size: 413 B')


    # Parse a file and count lines, words
    def test_parse_and_count(self):
        response = self.app.get('/parse/jingle.txt')          # 'jingle.txt' is already uploaded onto the 'uploads' folder
        self.assertTrue(response.status_code == 200, msg='GET request works fine')
        data = json.loads(response.data)

        self.assertTrue(data['File Name'] == 'jingle.txt')
        self.assertTrue(data['Number of Lines'] == 18)
        self.assertTrue(data['Number of Words'] == 78)

        self.assertTrue(data['Words']['jingle'] == 6)           # 'jingle' appears 6 times
        self.assertTrue(data['Words']['bells'] == 5)            # 'bells' appears 5 times
        self.assertTrue(data['Words']['ride'] == 3)             # 'ride' appears 3 times
        self.assertTrue(data['Words']['the'] == 5)              # 'the' appears 5 times
        self.assertTrue(data['Words']['snow'] == 1)
        self.assertTrue(data['Words']['laughing'] == 1)
        self.assertTrue(data['Words']['dashing'] == 1)
        self.assertTrue(data['Words']['sing'] == 1)


    # Discard all words that have a matching substring
    def test_discard_with_matching_string(self):
        response = self.app.get('/parse/jingle.txt?discard=ing')          # Discarding all words that have 'ing' within them
        self.assertTrue(response.status_code == 200, msg='GET request works fine')
        data = json.loads(response.data)

        self.assertTrue(data['File Name'] == 'jingle.txt')
        self.assertTrue(data['Number of Lines'] == 18)
        self.assertTrue(data['Number of Words'] == 78)          # Total # of words in the text file

        self.assertFalse(data['Words'].get('jingle'), msg="Discarded this one")
        self.assertTrue(data['Words']['bells'] == 5)
        self.assertTrue(data['Words']['ride'] == 3)
        self.assertTrue(data['Words']['the'] == 5)
        self.assertTrue(data['Words']['snow'] == 1)
        self.assertFalse(data['Words'].get('laughing'), msg="Discarded this one")
        self.assertFalse(data['Words'].get('dashing'), msg="Discarded this one")
        self.assertFalse(data['Words'].get('sing'), msg="Discarded this one")


    # Consider only those words that have a matching substring
    def test_keep_only_with_matching_string(self):
        response = self.app.get('/parse/jingle.txt?only=ing')          # Only keep those words that have 'ing' within them
        self.assertTrue(response.status_code == 200, msg='GET request works fine')
        data = json.loads(response.data)

        self.assertTrue(data['File Name'] == 'jingle.txt')
        self.assertTrue(data['Number of Lines'] == 18)
        self.assertTrue(data['Number of Words'] == 78)          # Total # of words in the text file

        self.assertTrue(data['Words']['jingle'] == 6)
        self.assertFalse(data['Words'].get('bells'), msg="Discarded this one")
        self.assertFalse(data['Words'].get('ride'), msg="Discarded this one")
        self.assertFalse(data['Words'].get('the'), msg="Discarded this one")
        self.assertFalse(data['Words'].get('snow'), msg="Discarded this one")
        self.assertTrue(data['Words']['laughing'] == 1)
        self.assertTrue(data['Words']['dashing'] == 1)
        self.assertTrue(data['Words']['sing'] == 1)


    # Discard and Include words with matching substrings at the same time
    def test_discard_and_keep_with_matching_string(self):
        response = self.app.get('/parse/jingle.txt?discard=dash&only=ing')          # Only keep those words that have 'ing' within them
        self.assertTrue(response.status_code == 200, msg='GET request works fine')
        data = json.loads(response.data)

        self.assertTrue(data['File Name'] == 'jingle.txt')
        self.assertTrue(data['Number of Lines'] == 18)
        self.assertTrue(data['Number of Words'] == 78)          # Total # of words in the text file

        self.assertTrue(data['Words']['jingle'] == 6)
        self.assertFalse(data['Words'].get('bells'), msg="Discarded this one")
        self.assertFalse(data['Words'].get('ride'), msg="Discarded this one")
        self.assertFalse(data['Words'].get('the'), msg="Discarded this one")
        self.assertFalse(data['Words'].get('snow'), msg="Discarded this one")
        self.assertTrue(data['Words']['laughing'] == 1)
        self.assertFalse(data['Words'].get('dashing'), msg="Discarded this one")
        self.assertTrue(data['Words']['sing'] == 1)


    # Checking words that are not in the file
    def test_words_that_are_unavailable(self):
        response = self.app.get('/parse/jingle.txt')          # Only keep those words that have 'ing' within them
        self.assertTrue(response.status_code == 200, msg='GET request works fine')
        data = json.loads(response.data)

        self.assertTrue(data['File Name'] == 'jingle.txt')
        self.assertTrue(data['Number of Lines'] == 18)
        self.assertTrue(data['Number of Words'] == 78)          # Total # of words in the text file

        self.assertTrue(data['Words']['jingle'] == 6)           # 'jingle' appears 6 times
        self.assertTrue(data['Words']['bells'] == 5)            # 'bells' appears 5 times
        self.assertTrue(data['Words']['ride'] == 3)             # 'ride' appears 3 times
        self.assertFalse(data['Words'].get('foo'), msg="'foo' is not there in the file")
        self.assertFalse(data['Words'].get('boom'), msg="'boom' is not there in the file")


if __name__ == '__main__':
    unittest.main()
