#import os
import main
import unittest

class FileParserTestCase(unittest.TestCase):

    def setUp(self):
        main.app.config['TESTING'] = True
        self.app = main.app.test_client()

if __name__ == '__main__':
    unittest.main()
