#coding=utf-8
#encoding=utf-8
# Generate best retrieval result for some dataset
import lucene, os, numpy, sys

from java.nio.file import Paths
from SearchSentence_multi import run
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher

base_dir = ""
data_address = "batch1/"
srcfile = data_address + "batch_src_raw"
batch_size = 4990000
retrieval_size = 15
INDEX_DIR = "Train_context.index"
end_num = 3200000


def generate():
    f_read = open(srcfile,'r')
    count = 0
    failure = 0
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    directory = SimpleFSDirectory(Paths.get(os.path.join(base_dir, INDEX_DIR)))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    for line in f_read:
    # if something wrong occurs, we ignore this sentence, and write a num+'-1' in the directory
        reply_path = data_address + str(count)
        if os.path.exists(reply_path + '.npy'):
            count += 1
            continue
        if count>=end_num:
            break
        line = line.strip('\n')
        line = unicode(line, 'utf-8')
        line = line.replace('?','')
        line = line.replace('*','')
        line = line.replace('\"','')
        line = line.replace('\'','')
        try:
            if line != '':
                reply_list = run(line, INDEX_DIR, 1, searcher, retrieval_size)
                numpy.save(reply_path, reply_list)
                if count % 50 == 0:
                        print str(count)
                count += 1
            else:
                f_write = open(reply_path + '-1', 'w')
                f_write.write(' ')
                f_write.close()
                count += 1
                failure += 1
        except Exception, e:
            print "Error: ", e
            f_write = open(reply_path + '-1', 'w')
            f_write.write(' ')
            f_write.close()
            count += 1
            failure += 1      
    del searcher
    f_read.close()
    f_accomplish = open(data_address + "accomplished_gen_retr_for_batch_para1", 'w')
    f_accomplish.write("Count: "+str(count)+" Failure: "+str(failure))
    f_accomplish.close() 

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    generate()
            
            
