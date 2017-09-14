
import unittest
from tests.cacher_test import *
from tests.describe_test import *
from tests.util_test import *

from tests.plugin_csv_test import *
from tests.plugin_json_test import *
from tests.plugin_xml_test import *


suite = unittest.TestSuite()

for cls in [CacherTest, DescribeTest, UtilTest,
            PluginCSVTest, PluginJsonTest, PluginXMLTest]:
    suite.addTest(unittest.makeSuite(cls))

runner=unittest.TextTestRunner()
runner.run(suite)
