import unittest
from webscrape import *




# verifying output from webscrape so that I know what data we are getting before parsing, transforming, and storing in dictionary

class TestWebscrape(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.html_content = initiate_browser()

    def test_verify_tr_tags_exist_in_html_data_from_selenium(self):
        result = False
        if "<tr>" in self.html_content:
            if "</tr>" in self.html_content:
                result = True
        self.assertEqual(result, True)
          

if __name__ == '__main__':
    unittest.main()
