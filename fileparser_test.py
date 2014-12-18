#import os
import main
import unittest

class FileParserTestCase(unittest.TestCase):

    def setUp(self):
        main.app.config['TESTING'] = True
        self.app = main.app.test_client()

    # Test Root of the application
    def test_home_page(self):
        rv = self.app.get('/')
        assert "I am running!" in rv.data

if __name__ == '__main__':
    unittest.main()
