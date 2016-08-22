import csv

INDIA_CITY_STATE_FILE = "india_city_state.csv"


class IndianCityState:

    def __init__(self):
        """Assumes fname is the csv file containing "city,state" entries in
        each line """
        self.fname = INDIA_CITY_STATE_FILE
        self.cityStateMap = self.parseFile()

    def parseFile(self):
        cityStateMap = {}
        fhandle = open(self.fname, 'r')
        try:
            reader = csv.reader(fhandle)
            for row in reader:
                if len(row) == 2:
                    city = row[0]
                    state = row[1]
                    if len(city) > 0 and len(state) > 0:
                        city = city.strip()
                        city = city.lower()
                        state = state.strip()
                        state = state.lower()
                    cityStateMap[city] = state
        except:
            print "Error reading city state mapping file"
        finally:
            fhandle.close()
        return cityStateMap

    def getStateFromCity(self, city):
        if len(city) < 1:
            return None
        city = city.lower()
        if city in self.cityStateMap:
            return self.cityStateMap[city]
        else:
            return None
