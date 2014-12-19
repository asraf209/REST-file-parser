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
                    data={'file':(StringIO('We are sample contents'), 'test.txt')})
        self.assertTrue(response.status_code == 200, msg='POST request works fine')

        data = json.loads(response.data)
        self.assertEqual(data['File Name'], 'test.txt')
        self.assertEqual(data['Number of Lines'], 1)
        self.assertEqual(data['Number of Words'], 4)


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
        response = self.app.get('/files/rest.txt')          # 'rest.txt' is already uploaded onto the 'uploads' folder
        self.assertTrue(response.status_code == 200, msg='GET request works fine')
        data = json.loads(response.data)
        self.assertTrue(data['File Name'] == 'rest.txt')
        self.assertTrue(data['Size'] == 1174, msg='File size: 1174 B')


if __name__ == '__main__':
    unittest.main()
