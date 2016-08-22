from NSLib.Parser.NewsProcessor import NewsProcessor
import time

newsProcessor = NewsProcessor()

while True:
    if not newsProcessor.newsProcess():
        time.sleep(120)
