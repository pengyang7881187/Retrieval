#coding=utf-8
import sys, lucene, time, os
from SearchSentence import run
from IndexFiles import IndexFiles

from org.apache.lucene.analysis.cn.smart import SmartChineseAnalyzer

batch_size = 10000
retrieval_size = 15
data_address = "batch1/"

def generate_index():
    abandon_num = 0
    for i in range(batch_size):
        reply_path = data_address + str(i) + '/'
        index_path = data_address + str(i) + '.index/'
        if os.path.exists(reply_path + "-1"):
            abandon_num += 1
            continue
        IndexFiles(reply_path, index_path, SmartChineseAnalyzer(), 1)

def search_best():
    abandon_num = 0
    fp_read1 = open(data_address + "batch_tgt_gen", 'r')
    fp_write2 = open(data_address + "batch_tgt_retr_similar", 'w')
    abandon_pos = []
    i = 0
    # search and write tgt
    for line in fp_read1:
        if i >= batch_size:
            break
        reply_path = data_address + str(i)
        index_path = data_address + str(i) + '.index/'
        if not os.path.exists(index_path):
            abandon_num += 1
            abandon_pos.append(i)
            i += 1
            continue
        else:
            try:
                line = line.strip('\n')
                if line != '':
                    re_answer = run(line, index_path, reply_path, 1)
                    re_answer = re_answer.strip('\n')
                    fp_write2.write(re_answer+'\n')
                    i += 1
                else:
                    abandon_num += 1
                    abandon_pos.append(i)
                    i += 1
            except Exception, e:
                print "Fail to retrieve: ", e
                abandon_num += 1
                abandon_pos.append(i)
                i += 1
    fp_read1.close()
    fp_write2.close()

    # write src
    fp_read2 = open(data_address + "batch_src_raw", 'r')
    fp_write1 = open(data_address + "batch_src_retr_similar", 'w')
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

    fp_accomplished = open(data_address + 'accomplished', 'w')
    fp_accomplished.write("Abandon: "+str(abandon_num)+' Batch size: '+str(batch_size-abandon_num))
    fp_accomplished.close()





if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Please input an arg 0 to generate index, and 1 to search response, 2 both"
        sys.exit()
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    cmd = int(sys.argv[1])

    start = time.time()
    if cmd == 0:
        generate_index()
    elif cmd == 1:
        search_best()
    else:
        generate_index()
        search_best()
    end = time.time()
    print "Time consuming: "
    print end - start



