
import unittest

from sinbad.plugin_json import *
from sinbad.util import create_input

class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_json_infer(self):
        inf = JSON_Infer()
        
        self.assertTrue(inf.matched_by("data/mock_data.json"))
        
        self.assertFalse(inf.matched_by("data/mock_data.csv"))
        self.assertFalse(inf.matched_by("data/mock_data.xml"))
        
    
    def test_json_data(self):
        for path in ['data/mock_data.json',
                     'https://raw.githubusercontent.com/berry-cs/sinbad-py/master/tests/data/mock_data.json']:
            df = JSON_Data_Factory()
            with create_input(path)[0] as fp:
                data = df.load_data(fp)
                self.assertTrue(isinstance(data,list))     
                self.assertEqual([k for k in data[0]],     # check keys
                                 'id,first_name,last_name,email,gender,ip_address'.split(','))
                        
            self.assertEqual(data[2],
                             {"id":3,"first_name":"Corny","last_name":"Chillcot",
                              "email":"cchillcot2@google.pl","gender":"Male",
                              "ip_address":"10.84.116.69"})

        
        

if __name__ == "__main__":
    unittest.main()