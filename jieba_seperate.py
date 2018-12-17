# encoding=utf-8
import jieba, os, sys
filename_test = "./tasktestdata05"
fileroot_train_context = "./train_context"
fileroot_train_reply = "./train_replies"
fileroot_seperate_train_context = "./seperate_train_context"
fileroot_seperate_train_reply = "./seperate_train_replies"
size = 5000000
def seperate_word():
    # this loop means that process the train context and reply in one time
    reload(sys)
    sys.setdefaultencoding('utf-8')
    for i in range(2):
        if i == 0:
            root = fileroot_train_context
            write_root = fileroot_seperate_train_context
        else :
            root = fileroot_train_reply
            write_root = fileroot_seperate_train_reply
        for j in range(size):
            if j % 10000 == 0:
                print "adding", str(j)
            path = os.path.join(root, str(j))
            fp_read = open(path, 'r')

            path = os.path.join(write_root, str(j))
            fp_write = open(path, 'w')
            for line in fp_read:
                seg_list = jieba.cut(line)
                result = ' '.join(seg_list)
                fp_write.write(result)
            fp_read.close()
            fp_write.close()
    ac_file = open("accomplish_jieba_train_seperate",'w')
    ac_file.write("accomplished")
    return

if __name__ == "__main__":
    seperate_word()

