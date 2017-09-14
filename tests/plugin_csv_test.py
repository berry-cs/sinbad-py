
import unittest

from sinbad.plugin_csv import *
from sinbad.util import create_input

class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_csv_infer(self):
        inf = CSV_Infer()
        self.assertTrue(inf.matched_by("data/mock_data.csv"))
        self.assertFalse('delimiter' in inf.options)

        self.assertTrue(inf.matched_by("data/mock_data.tsv"))
        self.assertEqual(inf.options['delimiter'], '\t')
        
        self.assertFalse(inf.matched_by("data/mock_data.xml"))
        
    
    def test_csv_header_data(self):
        for path in ['data/mock_data.csv',
                     'https://raw.githubusercontent.com/berry-cs/sinbad-py/master/tests/data/mock_data.csv']:
            df = CSV_Data_Factory()
            with create_input(path)[0] as fp:
                data = df.load_data(fp)
                self.assertEqual(df.field_names, 
                                 'id,first_name,last_name,email,gender,ip_address'.split(','))
                        
            self.assertEqual([data[2][k] for k in data[2]], 
                             "3,Reeta,Aubrun,raubrun2@bing.com,Female,118.80.136.241".split(","))
        
        
    def test_csv_no_header_data(self):
        df = CSV_Data_Factory()
        with open('data/mock_data_no_header.csv', 'rb') as fp:
            data = df.load_data(fp)
            self.assertEqual(df.field_names,
                             ['_col_0', '_col_1', '_col_2', '_col_3', '_col_4', '_col_5'])
            
        self.assertEqual([data[0][k] for k in data[0]], 
                         "1,Ronnie,Gregory,rgregory0@themeforest.net,Male,24.201.232.16".split(","))
            
        df = CSV_Data_Factory()
        df.set_option('header', 'id,first_name,last_name,email,gender,ip_address')
        with open('data/mock_data_no_header.csv', 'rb') as fp:
            self.assertIsNone(df.delimiter)   # updated later...
            data = df.load_data(fp)
            self.assertEqual(df.field_names, 
                             'id,first_name,last_name,email,gender,ip_address'.split(','))
            self.assertEqual(df.delimiter, ',')

        self.assertEqual([data[99][k] for k in data[99]], 
                         "100,Valentin,Kelsow,vkelsow2r@wired.com,Male,237.195.182.163".split(","))


    def test_tsv_header_data(self):
        df = CSV_Data_Factory()
        df.set_option("delimiter", "\t")
        self.assertEqual(df.delimiter, '\t')
        
        with open('data/mock_data.tsv', 'rb') as fp:
            data = df.load_data(fp)
            self.assertEqual(df.field_names, 
                             'id,first_name,last_name,email,gender,ip_address'.split(','))
            
        self.assertEqual([data[99][k] for k in data[99]], 
                         "100,Sherm,Cristobal,scristobal2r@timesonline.co.uk,Male,226.160.185.124".split(","))


    def test_tsv_no_header_data(self):
        df = CSV_Data_Factory()
        df.set_option("delimiter", "\t")
        self.assertEqual(df.delimiter, '\t')

        with open('data/mock_data_no_header.tsv', 'rb') as fp:
            data = df.load_data(fp)
            self.assertEqual(df.field_names,
                             ['_col_0', '_col_1', '_col_2', '_col_3', '_col_4', '_col_5'])
            
        self.assertEqual([data[15][k] for k in data[15]], 
                         "16,Cayla,Richemond,crichemondf@google.pl,Female,220.238.128.13".split(","))
            
        df = CSV_Data_Factory()   # is going to infer the delimiter... see later...
        df.set_option('header', 'id,first_name,last_name,email,gender,ip_address')
        with open('data/mock_data_no_header.tsv', 'rb') as fp:
            self.assertIsNone(df.delimiter)   # updated later...
            data = df.load_data(fp)
            self.assertEqual(df.field_names, 
                             'id,first_name,last_name,email,gender,ip_address'.split(','))
            self.assertEqual(df.delimiter, '\t')

        self.assertEqual([data[15][k] for k in data[15]], 
                         "16,Cayla,Richemond,crichemondf@google.pl,Female,220.238.128.13".split(","))


if __name__ == "__main__":
    unittest.main()