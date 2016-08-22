import re
import urllib2


def top_videos_india():
    url = "http://gdata.youtube.com/feeds/api/standardfeeds/IN/most_popular?orderby=viewCount"
    request = urllib2.urlopen(url)
    text = request.read()
    videos = re.findall("http:\/\/www\.youtube\.com\/watch\?v=[\w-]+", text)
    # print (videos)
    # print ("TOTAL VIDEOS: ", len(videos))
    return videos


def main():
    top_videos_india()


if __name__ == '__main__':
    main()
