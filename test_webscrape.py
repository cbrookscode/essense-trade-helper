import unittest
from webscrape import *




# verifying output from webscrape so that I know what data we are getting before parsing, transforming, and storing in dictionary

class TestWebscrape(unittest.TestCase):

    # @classmethod
    # def setUpClass(cls):
    #     cls.html_content = initiate_browser()

    # def test_verify_tr_tags_exist_in_html_data_from_selenium(self):
    #     result = False
    #     if "<tr>" in self.html_content:
    #         if "</tr>" in self.html_content:
    #             result = True
    #     self.assertEqual(result, True)

    def test_essence_dictionary_if_doesnt_exist(self):
        # test to make sure rows have <tr></tr>
        html_content = initiate_browser()
        soup = BeautifulSoup(html_content, 'lxml')
        rows = soup.find_all('tr')[1:]
        for row in rows:
            row_text = row.get_text(strip=True)
            # print(row_text)
            row_text = row_text.replace("wiki", "") 
            modified_row = re.split(r'(\d+)', row_text, maxsplit=1)
            essence_name = modified_row[0]
            print(modified_row)
            print("".join(modified_row[1:]))
            # if len(modified_row) != 3:
            #     break
            # else:
            #     chaos_value = re.split(r'(\.\d)', "".join(modified_row[1:]), maxsplit=1)
            #     print(f"{essence_name}: {chaos_value}")

if __name__ == '__main__':
    unittest.main()
