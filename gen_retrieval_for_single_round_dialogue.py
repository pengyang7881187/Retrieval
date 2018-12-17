#coding=utf-8
# Generate best retrieval result for some dataset
srcfile = "./batch1/batch_src_raw"
import lucene
from SearchSentence import run


def generate():
    f_read = open(srcfile,'r')
# Here, the raw means that it contains PASS 
    f_write = open(srcfile+"_retr_raw_tgt",'w')
    count = 0
    pass_num = 0
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    for line in f_read:
    # if something wrong occurs, we ignore this sentence, and write "PASS" so as to not use this
    # instance in the LSTM
        try:
            line = line.strip('\n')
            if line != '':
                re_answer = run(line ,"Train_context.index", "train_replies/", 1)
                f_write.write(re_answer+'\n')
                if count % 10000 == 0:
                    print str(count)+':Query: '+ line +' Retrieval Answer: '+ re_answer
                count += 1
            else:
                f_write.write("PASS\n")
                pass_num += 1
                count += 1
        except Exception, e:
            print "Fail to retrieve: ", e
            f_write.write("PASS\n")
            pass_num += 1 
            count += 1            
    f_read.close()
    f_write.close()
    f_accomplish = open("accomplished_gen_retr", 'w')
    f_accomplish.write("pass num: " + str(pass_num) + " count: " + str(count))
    f_accomplish.close() 

if __name__ == "__main__":
    generate()
            
            
