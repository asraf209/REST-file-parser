#import os
import fileparser
import unittest

class FileParserTestCase(unittest.TestCase):

    def setUp(self):
        fileparser.app.config['TESTING'] = True
        self.app = fileparser.app.test_client()

    # Test Root of the application
    def test_root(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        assert "I am running!" in response.data


    """def test_all_files(self):
        response = self.app.get('/files')
        self.assertEqual(response.status_code, 200)
        print response.data
    """

if __name__ == '__main__':
    unittest.main()
