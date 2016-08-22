from NSLib.Parser.TagParser import TagParser


def main():
    content = "Heavy rain lashes Maharashtra"
    tp = TagParser(content, True)
    tags = tp.getTags()

    print tags


if __name__ == '__main__':
    main()
