'''
Created on Jan 31, 2015

@author: rsingh
'''
import unittest

from NSLib.Parser.RefData import RefData

class Test(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.refdata = RefData()

    def testTags(self):
        cityTags, stateTags = self.refdata.getLocationTags("Uttar Pradesh patna HC commutes Nithari convict Surendra Koli's death sentence to life")

        assert self.verifyTags(['patna'], cityTags)
        assert self.verifyTags(['bihar', 'uttar-pradesh'], stateTags)

        cityTags, stateTags = self.refdata.getLocationTags("hyderabad bangalore mysore elections: BJP plans aggressive campaign; counter AAP")

        assert self.verifyTags(['hyderabad', 'bangalore', 'mysore'], cityTags)
        assert self.verifyTags(['karnataka', 'andhra-pradesh'], stateTags)

        reportedTags = self.refdata.getRefTags("Forged Alliance With BJP Out AAP of Conviction, Not Convenience,' Says Jammu and Kashmir Chief Minister: Highlights")
        assert self.verifyTags([u'aap', u'bjp'], reportedTags)

        reportedTags = self.refdata.getRefTags("meenakshi lekhi said lalal salman khan")
        assert self.verifyTags([u'politics', u'salman-khan', u'meenakshi-lekhi', u'movies'], reportedTags)

        reportedTags = self.refdata.getRefTags("uma bharti's: meenakshi lekhi said lalal")
        assert self.verifyTags([u'politics', u'uma-bharti', u'meenakshi-lekhi'], reportedTags)

    def verifyTags(self, actualTags, reportedTags):
        if len(actualTags) != len(reportedTags):
            return False

        for tag in actualTags:
            try:
                reportedTags.index(tag)
            except:
                return False

        return True

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()