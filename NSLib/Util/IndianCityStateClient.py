from IndianCityState import IndianCityState


def readCityName():
    city = raw_input("Enter Indian city: ")
    return city.strip()


def testIndianCityStateMap():
    indcitystate = IndianCityState()
    city = readCityName()
    if len(city) < 1:
        print "Bad city name"
        return
    city = city.lower()
    state = indcitystate.getStateFromCity(city)
    if state:
        print "City: %s belongs to state: %s" % (city, state)
    else:
        print "No state found for city: %s" % city


def main():
    testIndianCityStateMap()


if __name__ == '__main__':
    main()
