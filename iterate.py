# encoding=utf-8
# -*- coding: utf-8 -*-
import os, sys, math, time

train_size = 4400000
batch_size = 32000
training_step = 5000
iter_num = 1
start_training_step = 320000
retrieval_size = 15

batch_sum = math.ceil(train_size/batch_size)
# working directory
absolute_path = "/home/chenyue/retrieval/"
train_src_path = absolute_path + "dataset/STC/train_src"

batch_path = absolute_path + "dataset/batch/batch"
batch_reply_path = batch_path + "_reply"
batch_similar_path = batch_path + "_similar_reply"
batch_process_path = batch_path + "_process"

log_path = absolute_path + "iterate_log/log" + iter_num

retrieval_model_name = "retrieval-model_iter" + iter_num + "_batch"

generate_model_path = absolute_path + "opennmt/OpenNMT-py-master/"
original_model_path = generate_model_path + "baseline-model_step_320000.pt"
retrieval_model_path = generate_model_path + retrieval_model_name

train_py_path = generate_model_path + "train.py"
translate_py_path = generate_model_path + "translate.py"
preprocess_py_path = generate_model_path + "preprocess.py"

data_path = generate_model_path + "data/"

train_cmd_part1 = "python " + train_py_path + " -data " + data_path
train_cmd_part2 = " -save_model "
train_cmd_part3 = " -world_size 1 -gpu_ranks 0 -learning_rate 0.1 -train_from "
train_cmd_part4 = " -train_steps "
train_cmd_part5 = " -save_checkpoint_steps " + str(training_step)

translate_cmd_part1 = "python " + translate_py_path + " -model "
translate_cmd_part2 = " -src " + batch_path
translate_cmd_part3 = " -output " + batch_reply_path
translate_cmd_part4 = " -replace_unk -gpu 1 -beam_size 1"

# This part may be buggy
vocab_path = data_path + "baseline.vocab.pt"
preprocess_cmd_part1 = "python " + preprocess_py_path + " -train_src "
preprocess_cmd_part2 = " -train_tgt "
preprocess_cmd_part3 = " -valid_src "
preprocess_cmd_part4 = " -valid_tgt "
preprocess_cmd_part5 = " -save_data " + data_path
preprocess_cmd_part6 = " -features_vocabs_prefix " + vocab_path

lucene_python = "/home/chenyue/pylucene/lucene/bin/python "
similar_py_path = absolute_path + "dataset/Similar_retrieval_iter.py"
# Embedding version could be used in a lazy way, or it will be too slow
# similar_py_path = absolute_path + "dataset/Similar_embedding_iter.py"


def combine_train_cmd(current_model_name, next_model_name, current_training_step, current_data):
    cmd = train_cmd_part1 + current_data + train_cmd_part2 + next_model_name + train_cmd_part3
    cmd += (current_model_name + train_cmd_part4 + str(current_training_step) + train_cmd_part5)
    return cmd


def combine_translate_cmd(current_batch_num, model_name):
    cmd = translate_cmd_part1 + model_name + translate_cmd_part2 + str(current_batch_num)
    cmd += (translate_cmd_part3 + str(current_batch_num) + translate_cmd_part4)
    return cmd


def combine_preprocess_cmd(current_batch_num, current_data):
    src = batch_process_path + str(current_batch_num)
    tgt = batch_similar_path + str(current_batch_num)
    cmd = preprocess_cmd_part1 + src + preprocess_cmd_part2 + tgt + preprocess_cmd_part3
    cmd += (src + preprocess_cmd_part4 + tgt + preprocess_cmd_part5 + current_data)
    cmd += preprocess_cmd_part6
    return cmd


def combine_similar_cmd(current_batch_num, start_sentence_num):
    cmd = lucene_python + similar_py_path + ' ' + str(batch_size) + ' ' + str(retrieval_size)
    cmd += (' ' + str(start_sentence_num) + ' ' + str(current_batch_num))
    return cmd


def Gen_batch():
    fp_read = open(train_src_path, 'r')
    count = 0
    current_batch_num = 0
    batch_file_address = batch_path + str(current_batch_num)
    fp_write = open(batch_file_address, 'w')
    for line in fp_read:
        if count == batch_size:
            count = 0
            current_batch_num += 1
            batch_file_address = batch_path + str(current_batch_num)
            fp_write.close()
            fp_write = open(batch_file_address, 'w')
        fp_write.write(line)
        count += 1
    fp_read.close()
    fp_accomplished = open(batch_path + "_accomplished", 'w')
    fp_accomplished.write(str(batch_sum) + ' ' + str(current_batch_num))


def Iterate(start_batch_num):
    start_sentence_num = start_batch_num * batch_size  # For similar.py to find the correct reply
    current_model = original_model_path   # with .pt
    current_training_step = start_training_step
    if start_batch_num != 0:
        # These two parameters should be filled again each restart
        current_model = ""
        current_training_step = 0

    log_file = open(log_path, 'w')

    # Determine whether to delete model that is old, without baseline
    delete_flag = 0

    for current_batch_num in range(batch_sum):

        log_file.write("Processing batch " + str(current_batch_num))
        log_file.write("Training steps: " + str(current_training_step))

        start = time.time()
        # batch_raw_address = batch_path + str(current_batch_num)
        # batch_reply_address = batch_reply_path + str(current_batch_num)
        # batch_similar_address = batch_similar_path + str(current_batch_num)
        # batch_process_address = batch_process_path + str(current_batch_num)

        # Update parameter
        next_model = retrieval_model_path + str(current_batch_num)
        current_training_step += training_step
        current_data = retrieval_model_name + str(current_batch_num)

        # Combine the cmd
        translate_cmd = combine_translate_cmd(current_batch_num, current_model)
        similar_cmd = combine_similar_cmd(current_batch_num, start_sentence_num)
        preprocess_cmd = combine_preprocess_cmd(current_batch_num, current_data)
        train_cmd = combine_train_cmd(current_model, next_model, current_training_step, current_data)
        if delete_flag == 1:
            delete_cmd1 = "rm " + current_model
            delete_cmd2 = "rm " + data_path + "retrieval_model*"

        # Exec
        os.system(translate_cmd)
        os.system(similar_cmd)
        os.system(preprocess_cmd)
        os.system(train_cmd)
        if delete_flag == 1:
            if current_model != original_model_path:
                os.system(delete_cmd1)
            os.system(delete_cmd2)


        # Update parameter
        current_model = next_model + "_step_" + str(current_training_step) + ".pt"
        start_sentence_num += batch_size

        end = time.time()
        consume = end - start
        print "Batch " + str(current_batch_num) + ' :'
        print "Consuming :"
        print consume
        log_file.write("Consuming: " + str(consume))
    log_file.close()




if __name__ == "__main__":
    # 1 to indicate gen_batch, 2 to indicate Iterate
    if len(sys.argv)!=2:
        exit()
    # Allow to restart at a certain number
    start_batch_num = 0
    if sys.argv[1]=='1':
        Gen_batch()
    else:
        Iterate(start_batch_num)
