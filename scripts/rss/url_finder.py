import re
# import urllib
import os.path


def parseurls(fname, rssurl):
    # rssurl = 'http://timesofindia.indiatimes.com/rssfeeds.*'
    result = []
    with open(fname, "r") as fconn:
        for line in fconn:
            urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|\
                      (?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
            # print ("URLs: ", urls)
            if len(urls) < 1:
                continue
            for u in urls:
                match = re.match(rssurl, u)
                # print ("Match1: ", match)
                if match is not None:
                    result.append(match.group())
                    # print("Match: ", match.group())
    return result


def write_file(fname, result):
    f = open(fname, 'w')
    for r in result:
        f.write("%s\n" % r)
    print ("Written %d rss urls" % len(result))
    print ("File %s Success!" % fname)
    f.close()


def main():
    infile = input("Enter file to parse: ")
    infile = infile.strip()
    isfile = os.path.isfile(infile)
    if isfile:
        rssurl = input("Enter regex for rss url: ")
        rssurl = rssurl.strip()
        result = parseurls(infile, rssurl)
        if len(result) > 0:
            fname = input("Enter output file name: ")
            # remove duplicates
            result = set(result)
            write_file(fname, result)
        else:
            print ("No RSS URL Found! - Check for errors.")
    else:
        print ("%s file does not exists" % infile)


if __name__ == '__main__':
    main()
