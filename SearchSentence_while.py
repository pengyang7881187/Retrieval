#!/usr/bin/env python

INDEX_DIR = "train_context.index"
replies_address = "./train_replies/"
base_dir = "" 

import sys, os, lucene

from java.nio.file import Paths
from org.apache.lucene.analysis.cn.smart import SmartChineseAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher

def run():
        # input a context, output a reply using retrieval model
        print "Start for retrieval using Pylucene"

        # initialize
        lucene.initVM(vmargs=['-Djava.awt.headless=true'])
        print 'lucene', lucene.VERSION
        directory = SimpleFSDirectory(Paths.get(os.path.join(base_dir, INDEX_DIR)))
        searcher = IndexSearcher(DirectoryReader.open(directory))
        analyzer = SmartChineseAnalyzer()
        while 1:
            print "Test for SearchSentence, please input a query(input q to exit):"
            command = ''
            while 1:
                temp = raw_input()
                if temp == '':
                    break
                command += temp
                command += ' '
            command = command.strip('\n')
            if command == 'q':
                break
        # search
            print "Searching for:", command
            query = QueryParser("contents", analyzer).parse(command)
            scoreDocs = searcher.search(query, 15).scoreDocs
            print "%s total matching documents." % len(scoreDocs)
            print "These responses are:"
        # search for the best 15 context
            for scoreDoc in scoreDocs:
                doc = searcher.doc(scoreDoc.doc)
                print 'path:', doc.get("path"), 'name:', doc.get("name"),'score:',scoreDoc.score
                name = doc.get("name")
                file_read = open(replies_address + name)
                print file_read.read()
                file_read.close()
        # output the best response
            bestScoreDoc = scoreDocs[0]
            bestDoc = searcher.doc(bestScoreDoc.doc)
            bestNum = bestDoc.get("name")
            print "best match num :", str(bestNum)

            file_read = open(replies_address + bestNum)
            bestReply = file_read.read()
            file_read.close()

            print 'best response :' , bestReply
            print "End for retrieval using Pylucene"
        del searcher
        return

if __name__ == '__main__':
    run()
