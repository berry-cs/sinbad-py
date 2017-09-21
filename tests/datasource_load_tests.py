'''
Created on Aug 24, 2017

@author: nhamid
'''
import unittest
from sinbad import *

from pprint import pprint


class Test(unittest.TestCase):


    def setUp(self):
        #C.defaultCacher().clearCache()
        pass


    def tearDown(self):
        pass


    def testReturns(self):
        ds = DataSource.connect("http://bigscreen.com/xml/nowshowing_new.xml")
        assert ds.set_cache_timeout(60 * 60) is ds
        assert ds.set_param("foo", "bar") is ds
        assert ds.load() is ds
        assert ds.load() is ds   # multiple loads should work


    def testConnect(self):
        ds = DataSource.connect("http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson")
        ds.load()
        obj = ds.fetch()
        print(obj)
        print(type(obj))
        print(isinstance(obj, dict))
        
        
    def testConnectXML(self):
        ds = DataSource.connect("http://bigscreen.com/xml/nowshowing_new.xml")
        ds.set_cache_timeout(60 * 60)
        ds.load()
        obj = ds.fetch()
        ds.print_description()
        #print(obj)
        
        print("Before")
        col = ds.fetch("title", "description", "link", base_path = "channel/item")
        print("After")
        assert len(obj["channel"]["item"]) == len(col)
        print(col[0])
        print(len(col))
        
        
    def testAirport(self):
        ds = DataSource.connect_as("XmL", "http://services.faa.gov/airport/status/ATL")
        ds.set_param("format", "application/xml").set_cache_timeout(300)
        ds.load()
        x = ds.fetch("Name", "State", "Delay", "Weather/Weather")
        #x = ds.fetch()
        pprint(x)
        ds.print_description()
        
        
    def testEarthQuake(self):
        ds = DataSource.connect("http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson")
        ds.set_cache_timeout(180).load()
        x = ds.fetch("title", "time", "mag", base_path = "features/properties")
        y = ds.fetch("features/properties/title", "features/properties/time", "features/properties/mag")
        y = ds.fetch("features/properties/title", "features/properties/time", "features/properties/mag")
        z = ds.fetch("features/properties/title", "features/properties/time", "features/properties/mag", base_path='')
        # note: one produces an array of objects, the second parallel arrays of simple data 
        #print(x)
        #print(y)
        self.assertEqual(len(x) , len(y))
        self.assertEqual(len(z), 3)
        self.assertEqual(len(x), len(z['title']))
       


    def testCSV(self):
        ds = DataSource.connect_as("csv", "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airlines.dat")
        ds.set_option("header", "ID,Name,Alias,IATA,ICAO,Call sign,Country,Active")
        ds.load()
        data = ds.fetch()
        for r in data:
            if r['ID'] == '3871':
                print("PIA: " + str(r))
                assert r['ICAO'] == 'PIA'
                break

        ds2 = DataSource.connect_as("csv", "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airlines.dat")
        ds2.set_option("header", ["ID","Name","Alias","IATA","ICAO","Call sign","Country","Active"])
        ds2.load()
        data2 = ds2.fetch()
        assert data[100] == data2[100]
        
    def testRandom(self):
        print("TEST --- RANDOM")
        ds = DataSource.connect_as("csv", "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airlines.dat")
        ds.set_option("header", "ID,Name,Alias,IATA,ICAO,Call sign,Country,Active")
        ds.load()
        
        data = ds.fetch_random()   
        assert isinstance(data, dict)

        name = ds.fetch_random("Name")
        country = ds.fetch_random("Country")
        assert data["Name"] == name  and data["Country"] == country
        print("done random")
        
        


    def test_zip(self):
        ds = DataSource.connect("http://www.fueleconomy.gov/feg/epadata/vehicles.csv.zip")
        ds.set_option('file-entry', "vehicles.csv")
        print("A")
        #ds.load_sample(10000)
        ds.load()
        print("B")
        data = ds.fetch()
        print(data[1])
        print("C")
        ds.fetch("make")
        print("C2")

        cdata = ds.fetch("make", "model", "city08")
        print("D")
        print("Cars length: {}".format(len(cdata)))
        pprint(cdata[0:5])

        assert len(data) == len(cdata)
        
        print("E")        
        rdata = ds.fetch_random("make", "model", "city08")
        print(rdata)
        print("F")
        rdata2 = ds.fetch_random("make", "model", "city08")
        assert rdata == rdata2
        print("G")
        ds.load()
        print("H")

        rdata3 = ds.fetch_random("make", "model", "city08")
        print("I")
        pprint(rdata)
        pprint(rdata3)
        self.assertNotEqual(rdata, rdata3)


    def test_gzip(self):
        ds = Data_Source.connect("https://www1.ncdc.noaa.gov/pub/data/swdi/stormevents/csvfiles/StormEvents_details-ftp_v1.0_d1950_c20170120.csv.gz")
        ds.load()
        ds.print_description()
        
        ds = DataSource.connect("https://s3.amazonaws.com/weruns/forfun/Kickstarter/Kickstarter_2015-10-22T09_57_48_703Z.json.gz")
        ds.load_sample(100)
        ds.print_description()

        print(ds.data_length("data/projects"))
        
        print("Start fetch")
        x = ds.fetch_random("name", "blurb", "backers_count",  "category/name", "country", "creator/name", "goal", "pledged", "deadline", base_path="data/projects")
        print("Done fetch")

        # well, this is zip, but anyway...
        ds = Data_Source.connect("https://s3.amazonaws.com/weruns/kickstarter_old/Kickstarter_2014-04-22.json.zip")
        ds.set_option("file-entry", "Kickstarter_Kickstarter.json")
        ds.load_sample(1000)
        ds.print_description()

        pprint(x)
        
        print(ds.data_length("projects"))


    def ZZZ_test_TSV(self):
        ds = DataSource.connect_as("TSV", "tls-data.tsv");
        ds.load();
        #ds.printUsageString();
        data = ds.fetch()
        print(len(data))
        agencies = ds.fetch("ParticipatingAgency")
        print( agencies[0:10] )


    def testSatori(self):
        endpoint = 'wss://open-data.api.satori.com'
        appkey = 'b7d4a0CBbaCD5BA87dCCb3a61571C1b8'
        channel = 'webtraffic'
        
        ds = DataSource.connect(endpoint)
        ds.set_option("appkey", appkey)
        ds.set_option("channel", channel)
        ds.load()
        assert ds.description().find("domainName") >= 0
        
        ds.print_description()
        data = ds.fetch()
        pprint(data)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    