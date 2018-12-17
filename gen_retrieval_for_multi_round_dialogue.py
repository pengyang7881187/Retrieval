#coding=utf-8
# Generate best retrieval result for some dataset
testfile = "tasktestdata05"
import lucene, os, sys
from SearchSentence import run

def generate(filename):
    f_read = open(testfile,'r')
    f_write = open(testfile+"_retr_gen",'w')
    context = []
    context_sen = ''
    re_answer = ''
    line_count = 0
    count = 0
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    for line in f_read:
        if line != '\n':
            line_count += 1
            context.append(line)
        else:
            for i in range(line_count-1):
                f_write.write(context[i])
                context[i] = context[i].rstrip('\n')
                context[i] += ' '
#                context_sen += context[i]
            context_sen = context[-2]
            f_write.write("原答案： "+context[-1])
            re_answer = run(context_sen,1)
            f_write.write("检索结果： "+re_answer+'\n')

            count += 1
            if count % 10000 == 0:
                print str(count)+':原答案：+'+context[-1]+'检索结果： '+re_answer
            line_count = 0
            context = []
            context_sen=''
            assert len(context) == 0
    f_read.close()
    f_write.close()

if __name__ == "__main__":
    generate(testfile)
            
            
