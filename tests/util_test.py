
import unittest
from sinbad.util import *

class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_hash(self):
        s1 = "42"
        s2 = str(20 + 22)
        s3 = "24"
        self.assertEqual(hash_string(s1), hash_string(s2))
        self.assertNotEqual(hash_string(s1), hash_string(s3))

    def test_paths(self):
        self.assertTrue(smellsLikeURL("http://cs.berry.edu"))
        self.assertTrue(smellsLikeURL("https://cs.berry.edu"))
        self.assertFalse(smellsLikeURL("wss://satori.org"))
        self.assertFalse(smellsLikeURL("/Users/foo/bar.txt"))

    def test_create_input(self):
        fp, pth, enc = create_input("http://cs.berry.edu")
        self.assertEqual(pth, "http://cs.berry.edu")
        self.assertEqual(enc, "utf-8")
        fp.close()
        
        fp, pth, enc = create_input("util_test.py")
        self.assertEqual(pth, "util_test.py")
        self.assertIsNone(enc)
        
    def test_normalize(self):
        self.assertEqual( normalize_keys({ "hi" : 234, "6435" : "5243", 
                                          "boo" : { "who" : "far" , "foo" : "2384", "1" : "one" } }),
                          { "hi" : 234, "_6435" : "5243", 
                           "boo" : { "who" : "far" , "foo" : "2384", "_1" : "one" } } )
        self.assertEqual( normalize_keys({ "hi" : 234, "6435" : "5243", 
                                          "boo" : [{ "who" : "far" , "foo" : "2384", "1" : "one" },
                                                   { "23" : 23 }] }),
                          { "hi" : 234, "_6435" : "5243", 
                           "boo" : [{ "who" : "far" , "foo" : "2384", "_1" : "one" },
                                    { "_23" : 23 }] } )
    


if __name__ == "__main__":
    unittest.main()