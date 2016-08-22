import TagParser


def readContent():
    content = None
    with open('news1.txt', 'r') as content_file:
        content = content_file.read()
    return content


def main():
    content = readContent()
    tagObj = TagParser.TagParser(content)
    tags = tagObj.getTags()
    print 'Tags are: '
    print tags


if __name__ == '__main__':
    main()
