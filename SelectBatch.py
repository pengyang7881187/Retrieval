#coding=utf-8

# random 

import random

train_src_address = 'STC/train_src'
batch_address = 'batch1/batch_src_raw'
batch_size = 10000

def SelectBatch():
    fp_read = open(train_src_address, 'r')
    sentence_list = fp_read.readlines()
    batch_list = random.sample(sentence_list, batch_size)
    fp_read.close()

    fp_write = open(batch_address, 'w')
    for sentence in batch_list:
        fp_write.write(sentence)
    fp_write.close()


if __name__=="__main__":
    SelectBatch()
