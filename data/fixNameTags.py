#!/usr/bin/python

'''
Created on Jan 4, 2015

@author: rsingh
'''

import sys, json, os

ORIGINAL_FILE_DIR = './original'

def clean(line):
    if line.find(',') != -1:
        token = line.split(',')
        return json.dumps({'name': token[0].strip(), 'tag': token[1].strip()})

    else:
        return json.dumps({'name': line, 'tag': line})

def processCityState(line):
    line = line.strip()
    tokens = line.split(',')

    return json.dumps({'name': tokens[0].strip(), 'tag': tokens, 'city': tokens[0], 'state': tokens[1]})

if __name__ == '__main__':
    fileList = os.listdir(ORIGINAL_FILE_DIR)
    for fileName in fileList:
        filePath = ORIGINAL_FILE_DIR + '/' + fileName
        if os.path.isdir(filePath):
            continue

        print "** processing %s **" % fileName
        inFile = open(filePath, 'r')
        outFile = open(fileName, 'w')

        lines = inFile.readlines()
        fixed_data = []

        if fileName == 'india_city_state.txt':
            for line in lines:
                outFile.write(processCityState(line.strip()) + '\n')
        else:
            for line in lines:
                outFile.write(clean(line.strip()) + '\n')

        inFile.close()
        outFile.close()