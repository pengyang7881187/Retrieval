#!/usr/bin/env python

INDEX_DIR_local = "Train_context.index"
replies_address_local = "./train_replies/"
base_dir = "" 

import sys, os, lucene

from java.nio.file import Paths
from org.apache.lucene.analysis.cn.smart import SmartChineseAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.search.similarities import TFIDFSimilarity
from org.apache.lucene.search.similarities import BM25Similarity

def run(command, INDEX_DIR, replies_address, ifsilent ):
        # input a context, output a reply using retrieval model
        if not ifsilent:
            print "Start for retrieval using Pylucene"

        # initialize remove to where it is imported

        # lucene.initVM(vmargs=['-Djava.awt.headless=true'])

        if not ifsilent:
            print 'lucene', lucene.VERSION
        directory = SimpleFSDirectory(Paths.get(os.path.join(base_dir, INDEX_DIR)))
        searcher = IndexSearcher(DirectoryReader.open(directory))
        analyzer = SmartChineseAnalyzer()
        command = command.strip('\n')

        # search x best context
        x = 1
        if not ifsilent:
            print "Searching for:", command
        query = QueryParser("contents", analyzer).parse(command)
        scoreDocs = searcher.search(query, x).scoreDocs
        if not ifsilent:
            print "%s total matching documents." % len(scoreDocs)
        # search for the best x context
        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            if not ifsilent:
                print 'path:', doc.get("path"), 'name:', doc.get("name"),'score:',scoreDoc.score

        # output the best response
        bestScoreDoc = scoreDocs[0]
        bestDoc = searcher.doc(bestScoreDoc.doc)
        bestNum = bestDoc.get("name")
        if not ifsilent:
            print "best match num :", str(bestNum)

        file_read = open(replies_address + bestNum)
        bestReply = file_read.read()
        file_read.close()
        del searcher
        
        if not ifsilent:
            print 'best response :' , bestReply
            print "End for retrieval using Pylucene"
        return bestReply

if __name__ == '__main__':
    print "Test for SearchSentence, please input a query(just once):"
    command = ''
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    while 1:
        temp = raw_input()
        if temp == '':
            break
        command += temp
        command += ' '
    run(command, INDEX_DIR_local, replies_address_local, 0)
