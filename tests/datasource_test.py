
import unittest

from sinbad.datasource import *

class DataSourceTest(unittest.TestCase):

    def setUp(self):
        Data_Source.clear_cache()
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
        
        
    def test_has_fields(self):
        ds = DataSource.connect_as("XmL", "http://services.faa.gov/airport/status/ATL")
        ds.set_param("format", "application/xml").set_cache_timeout(300)
        ds.load()
        print(ds.print_description())
        
        self.assertTrue(ds.has_fields("Name"))
        self.assertTrue(ds.has_fields("Name", "State", "Delay", "Weather/Weather"))
        self.assertTrue(ds.has_fields("Name", "Weather/Meta/Url", "Delay", "Weather/Weather"))
        self.assertTrue(ds.has_fields("Name", "Weather/Meta/Url", "Delay", "Weather/Weather", "Status/Reason"))

        self.assertFalse(ds.has_fields("Speed"))
        self.assertFalse(ds.has_fields("Weather/Speed"))
        self.assertFalse(ds.has_fields("Name", "State", "Delay", "Speed"))
        self.assertFalse(ds.has_fields("Name", "Weather/Meta/Url", "Delay", "Weather/Speed", "Status/Reason"))
        self.assertFalse(ds.has_fields("Name", "Weather/Meta/Url", "Speed", "Weather/Weather", "Status/Reason"))
        

if __name__ == "__main__":
    unittest.main()