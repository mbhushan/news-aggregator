'''
Created on Nov 23, 2014

@author: rsingh
'''

#POS ref: https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html

import nltk

#text = "Mumbai youth arrested on return after fighting for Islamic State sent to NIA custody till December 8"
text = "Mumbai youth Areeb Majeed arrested for fighting for Islamic State in Iraq has been sent to eight days of custody of the National Investigation Agency (NIA). Majeed was arrested on Friday on his return from Iraq after fighting for Islamic State in Iraq. \
He is being jointly grilled by NIA and the Maharashtra ATS. The NIA has been getting more details about his accomplices. Accordinf to sources, the NIA has found him to be highly radicalised and has shown no remorse for his actions while he was with the Islamic State. \
The 23-year-old was believed to be dead until he called his parents and expressed a desire to return home. In May earlier this year, four youths from Kalyan-Shaheen Tanki, Fahad Shaikh and Aman Tandel, besides Arif - had left India to visit holy places in West Asia but they disappeared thereafter and since then were suspected to have joined the Sunni extremist group. \
A case has been slapped against ISIS and its operatives under Sec 125 of the IPC which deals with waging war against any Asiatic country which has friendly ties with India, entailing maximum punishment of life imprisonment. A notification was issued by the Union Home Ministry late on Friday directing NIA to register the case. \
Meanwhile, Home Minister Rajnath Singh during his visit to Guwahati said that the impact of the terror outfit in India is a cause of concern. However, he also said that he was confident that the security forces in the country are fully capable of facing any challenge."

tokens = nltk.word_tokenize(text.lower())

finalTokens = []
for token in tokens:
    token = token.strip(',.?;!')
    if token.isalnum():
        finalTokens.append(token)

tokens = finalTokens
posData = nltk.pos_tag(tokens)

posDict = {}
tags = []
for token, pos in posData:
    if pos in ('NN', 'NNS', 'NNP', 'NNPS'):
        tags.append(token)
        posDict[token] = pos

print tags
print
print posDict.keys()
bigrams = nltk.bigrams(tokens)

freqDist = nltk.FreqDist(tokens)

for k,v in freqDist.items():
    if posDict.has_key(k[0]):# and posDict.has_key(k[1]):
        print k,v
