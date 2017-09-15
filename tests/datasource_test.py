
import unittest

from sinbad.datasource import *

class DataSourceTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_sample_seed(self):
        ds = Data_Source.connect("http://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip",
                                 format = "csv")

        ds.load_sample(max_elts=5)
        d1 = ds.fetch_first();
        ds.load_fresh_sample(max_elts=5)
        d2 = ds.fetch_first();
        ds.load_sample(max_elts=5, random_seed = 1234)
        d3 = ds.fetch_first();
        ds.load_sample(max_elts=5, random_seed = 42)
        d4 = ds.fetch_first();
        ds.load_sample(max_elts=5, random_seed = 1234)
        d5 = ds.fetch_first();

        self.assertNotEqual(d1, d2)
        self.assertNotEqual(d1, d3)
        self.assertNotEqual(d2, d3)
        self.assertNotEqual(d3, d4)
        self.assertEqual(d3, d5)
        
        

if __name__ == "__main__":
    unittest.main()