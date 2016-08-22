# class for creating tags out of the news contents
import nltk
import string
from RefData import RefData


class TagParser:

    def __init__(self, content, title=False):
        self.content = content
        self.tags = []
        self.tokens = None
        self.refPOS = ('NN', 'NNS', 'NNP', 'NNPS')
        self.tokenize()
        self.freqThreshold = 3
        self.title = title
        self.refdata = RefData()
        self.stopw = self.stopWords()

    def stopWords(self):
        stopWords = nltk.corpus.stopwords.words('english')
        stopw = [s.encode("ascii") for s in stopWords]
        return stopw

    def tokenize(self):
        self.content = self.content.strip(" ,.")
        self.tokens = nltk.word_tokenize(self.content.lower())
        sanitizedToks = []
        for t in self.tokens:
            t = t.strip(string.whitespace)
            t = t.strip(",.")
            sanitizedToks.append(t)

        self.tokens = sanitizedToks

    def parseTags(self):
        tokPosData = nltk.pos_tag(self.tokens)

        for token, pos in tokPosData:
            if pos in self.refPOS:
                self.tags.append(token.lower())
        return self.tags

    def getTags(self):

        tks = []
        finalTags = []
        for t in self.tokens:
            if t not in self.stopw:
                tks.append(t)

        tagText = " ".join(tks)
        celebrityTags = self.refdata.getRefTags(tagText)
        cityTags, stateTags = self.refdata.getLocationTags(tagText)
        celebrityTags.extend(cityTags)
        celebrityTags.extend(stateTags)
        finalTags.extend(celebrityTags)

        return finalTags, cityTags, stateTags

    def biGramTokenCounter(self):
        ''' create bigrams '''
        bgs = nltk.bigrams(self.tokens)
        # compute bigram frequency for all the tokens
        fdist = nltk.FreqDist(bgs)
        for k, v in fdist:
            print k, v
