from auth_twitter import getTrending


def main():
    """ get the WOEID from this url:
        http://woeid.rosselliot.co.nz/lookup/mumbai
        """
    woeid = 23424848  # india woeid
    woeid = 2295411  # mumbai woeid
    woeid = 2295420  # bangalore woeid
    trends = getTrending(woeid)
    print trends


if __name__ == '__main__':
    main()
