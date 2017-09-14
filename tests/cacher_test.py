
import unittest
from sinbad.cacher import *
from io import BytesIO


class Test(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_cacher_stringio(self):
        dir = default_cacher().cache_directory + os.path.sep + "_test_"
        c = default_cacher().update_directory(dir)
        
        sfp = BytesIO("hello world".encode(encoding='ascii'))
        c.add_to_cache("http://example.com", "manual", sfp)
        sfp.close()
        
        pth = c.resolve_path("http://example.com", "manual")
        with open(pth, 'rb') as f:
            self.assertEqual(f.read().decode('ascii'), "hello world")
        
        self.assertTrue(os.path.isdir(dir))
        self.assertTrue(os.path.isfile(pth))
        
        c.clear_cache_data("http://example.com", "manual")
        
        self.assertTrue(os.path.isdir(dir))
        self.assertFalse(os.path.isfile(pth))
        
        c.clear_cache()
        
        self.assertFalse(os.path.isdir(dir))
        self.assertFalse(os.path.isfile(pth))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()