import unittest
import fileparser
from StringIO import StringIO
import json

class FileParserTestCase(unittest.TestCase):

    def setUp(self):
        fileparser.app.config['TESTING'] = True
        self.app = fileparser.app.test_client()

    # Test Root of the application
    def test_root(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        assert "I am running!" in response.data

    # Test uploading a file
    def test_upload(self):
        response = self.app.post('/upload',
                    data={'file':(StringIO('We are sample contents'), 'test.txt')})
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data['File Name'], 'test.txt')
        self.assertEqual(data['Number of Lines'], 1)
        self.assertEqual(data['Number of Words'], 4)



    """def test_all_files(self):
        response = self.app.get('/files')
        self.assertEqual(response.status_code, 200)
        print response.data
    """

if __name__ == '__main__':
    unittest.main()
