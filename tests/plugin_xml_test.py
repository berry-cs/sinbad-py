
import unittest

from collections import OrderedDict
from sinbad.plugin_xml import *
from sinbad.util import create_input

class PluginXMLTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_xml_infer(self):
        inf = XML_Infer()
        
        self.assertTrue(inf.matched_by("data/mock_data.xml"))
        
        self.assertFalse(inf.matched_by("data/mock_data.csv"))
        self.assertFalse(inf.matched_by("data/mock_data.json"))
        
    
    def test_people(self):
        for path in ['data/people.xml',
                     'https://raw.githubusercontent.com/berry-cs/sinbad-py/master/tests/data/people.xml']:
            df = XML_Data_Factory()
            with create_input(path) as fp:
                data = df.load_data(fp)
                self.assertTrue(isinstance(data,list))     
                self.assertEqual([k for k in data[0]],     # check keys
                                 'id,name,email,gender,ip_address'.split(','))
                        
            self.assertEqual(data[0],
                             OrderedDict(
                                 [("id", '1'), 
                                  ("name", OrderedDict([("first_name","Gallard"),("last_name","Jeannet")])),
                                  ("email","gjeannet0@soundcloud.com"),
                                  ("gender","Male"),
                                  ("ip_address","89.87.101.28")]))

        
        

if __name__ == "__main__":
    unittest.main()