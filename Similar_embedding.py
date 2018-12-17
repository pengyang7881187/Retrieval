#coding=utf-8
import time, os
import numpy as np
# src and tgt use a sharing dictionary
word_vec_base = '/home/chenyue/retrieval/opennmt/OpenNMT-py-master/word_embedding/'
dict_filename = word_vec_base + 'src_embeddings_dict'
vec_filename = word_vec_base + 'src_embeddings_vec.txt'
batch_size = 10000
retrieval_size = 15
###
vec_length = 500
###
data_address = "batch1/"
train_reply_address = "train_replies/"

word_vec = np.loadtxt(vec_filename)
f = open(dict_filename, 'r')
a = f.read()
word_dic = eval(a)
f.close()

def calculate_similarity(sentence1, sentence2):
    word_1 = sentence1.split(' ')
    word_2 = sentence2.split(' ')
    vec_1 = np.zeros(vec_length)
    vec_2 = np.zeros(vec_length)

    count = 0
    for word in word_1:
        if word in word_dic.keys():
            vec_1 += word_vec[word_dic[word]]
        else:
            vec_1 += word_vec[0]
        count += 1
    vec_1 = vec_1 / count

    count = 0
    for word in word_2:
        if word in word_dic.keys():
            vec_2 += word_vec[word_dic[word]]
        else:
            vec_2 += word_vec[0]
        count += 1
    vec_2 = vec_2 / count

    score = np.abs((np.inner(vec_1, vec_2)/(np.linalg.norm(vec_1)*np.linalg.norm(vec_2))))
    return score

def search_best():
    abandon_num = 0
    abandon_pos = []
    fp_read1 = open(data_address + "batch_tgt_gen", 'r')
    fp_write2 = open(data_address + "batch_tgt_embedding_similar", 'w')
    
    #word_vec = np.loadtxt(vec_filename)
    #f = open(dict_filename, 'r')
    #a = f.read()
    #word_dic = eval(a)
    #f.close()

    # search and write tgt
    i = 0
    for line in fp_read1:
        reply_path = data_address + str(i)
        if i >= batch_size:
            break
        if os.path.exists(reply_path + "-1"):
            abandon_num += 1
            abandon_pos.append(i)
            i += 1
            continue

        line = line.strip('\n')

        score = np.zeros(retrieval_size)
        content = []
        
        reply_num = np.load(reply_path + '.npy') 

        for j in range(retrieval_size):
            num = int(reply_num[j])
            fp_read = open(train_reply_address + str(int(num)))
            content.append(fp_read.read())
            fp_read.close()
            content[j] = content[j].strip('\n')
            score[j] = calculate_similarity(line, content[j])
        max_num = score.argmax()
        re_answer = content[max_num]
        re_answer = re_answer.strip('\n')
        fp_write2.write(re_answer + '\n')
        i += 1

    fp_read1.close()
    fp_write2.close()

    # write src
    fp_read2 = open(data_address + "batch_src_raw", 'r')
    fp_write1 = open(data_address + "batch_src_embedding_similar", 'w')
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

    start = time.time()
    search_best()
    end = time.time()
    print "Time consuming: "
    print end - start



