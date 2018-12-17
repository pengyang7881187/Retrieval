#!/usr/bin/env python

INDEX_DIR_local = "Train_context.index"
replies_address_local = "./train_replies/"
base_dir = "" 

import lucene
import numpy as np

from org.apache.lucene.analysis.cn.smart import SmartChineseAnalyzer
from org.apache.lucene.queryparser.classic import QueryParser

def run(command, INDEX_DIR, ifsilent, searcher, retrieval_size):
        # input a context, output a reply using retrieval model
        if not ifsilent:
            print "Start for retrieval using Pylucene"

        # initialize remove to where it is imported

        # lucene.initVM(vmargs=['-Djava.awt.headless=true'])

        analyzer = SmartChineseAnalyzer()
        command = command.strip('\n')

        # search x best context
        x = retrieval_size


        if not ifsilent:
            print "Searching for:", command
        query = QueryParser("contents", analyzer).parse(command)
        scoreDocs = searcher.search(query, x).scoreDocs
        if not ifsilent:
            print "%s total matching documents." % len(scoreDocs)

        
        # search for the best x context
        replies = np.zeros(x)
        i = 0
        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            replies[i] = int(doc.get("name"))
          
            if not ifsilent:
                print 'path:', doc.get("path"), 'name:', doc.get("name"),'score:',scoreDoc.score
            i += 1            

        # return the best response
        
        return replies

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
