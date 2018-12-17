#coding=utf-8
import os, sys, lucene
import numpy as np
from java.nio.file import Paths
from org.apache.lucene.analysis.cn.smart import SmartChineseAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.analysis.standard import StandardAnalyzer

# src and tgt use a sharing dictionary
#batch_size = 10000
#retrieval_size = 15
#data_address = "batch1/"
#train_reply_address = "train_replies/"


def search_best(batch_size, retrieval_size, start_sentence_num, batch_num):

    absolute_path = "/home/chenyue/retrieval/"

    REPLY_INDEX_DIR = absolute_path + "dataset/Train_reply.index"
    data_address = absolute_path + "dataset/retr_tgt/"
    train_reply_address = absolute_path + "dataset/train_replies/"

    batch_path = absolute_path + "dataset/batch/batch"
    batch_address = batch_path + str(batch_num)
    batch_reply_address = batch_path + "_reply" + str(batch_num)
    batch_similar_address = batch_path + "_similar_reply" + str(batch_num)
    batch_process_address = batch_path + "_process" + str(batch_num)


    abandon_num = 0
    abandon_pos = []
    fp_read1 = open(batch_reply_address, 'r')
    fp_write2 = open(batch_similar_address, 'w')
    
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    directory = SimpleFSDirectory(Paths.get(REPLY_INDEX_DIR)) 
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = SmartChineseAnalyzer()   
    analyzer_for_name = StandardAnalyzer()

    i = 0
    for line in fp_read1:
        reply_path = data_address + str(i+start_sentence_num)  # Here requires an offset
        if i >= batch_size:
            break
        if os.path.exists(reply_path + "-1"):
            abandon_num += 1
            abandon_pos.append(i)
            i += 1
            continue
        try:
            line = line.strip('\n')
    
            score = np.zeros(retrieval_size)
            content = []
            
            reply_num = np.load(reply_path + '.npy') 
    
            for j in range(retrieval_size):
        # Get doc_id
                num = int(reply_num[j])
                print num
                query_name = QueryParser("name", analyzer_for_name).parse(str(num))
                scoreDocs = searcher.search(query_name, 1).scoreDocs
                doc_id = scoreDocs[0].doc
              
                query = QueryParser("contents", analyzer).parse(line)
                
                fp_read = open(train_reply_address + str(num), 'r')
                content.append(fp_read.read())
                fp_read.close()
                content[j] = content[j].strip('\n')
                explain = searcher.explain(query, doc_id)
                score[j] = explain.getValue()
            max_num = score.argmax()
            re_answer = content[max_num]
            re_answer = re_answer.strip('\n')
            fp_write2.write(re_answer + '\n')
            i += 1
        except Exception, e:
            print "Fail to compute similarity:", e
            abandon_num += 1
            abandon_pos.append(i)
            i += 1
    fp_read1.close()
    fp_write2.close()
    del searcher
    # write src
    fp_read2 = open(batch_address, 'r')
    fp_write1 = open(batch_process_address, 'w')
    i = 0
    for line in fp_read2:
        if i in abandon_pos:
            i += 1
            continue
        fp_write1.write(line)
        i += 1
        if i >= batch_size:
            break
    fp_read2.close()
    fp_write1.close()



if __name__ == "__main__":
    if len(sys.argv)!=5:
        print "Similar needs more argv!"
        exit()
    search_best(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]))



