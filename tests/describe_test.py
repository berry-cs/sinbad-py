
import unittest
from sinbad.describe import *


class DescribeTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_describe(self):
        self.assertEqual( describe([{ 'name' : { 'first' : "john", 'last' : 'doe'}, 
                                     'age' : 4, 
                                     'cities' : ['Rome', 'Madrid', 'Tokyo']}]),
'''list of:
  dictionary with {
    age : *
    cities : list of *
    name : dictionary with {
             first : *
             last : *
           }
  }''' 
                        )



if __name__ == "__main__":
    unittest.main()
    