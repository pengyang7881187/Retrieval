
def partition():
    fp_read = open("STC/train", 'r')
    fp_write1 = open("STC/train_src", 'w')
    fp_write2 = open("STC/train_tgt", 'w')
    count = 0
    for line in fp_read:
        line = line.strip('\n')
        content = line.split('\t')
        fp_write1.write(content[0]+'\n')
        fp_write2.write(content[1]+'\n')
        count += 1
    fp_read.close()
    fp_write1.close()
    fp_write2.close()
    fp_accomplished = open("accomplished_partition", 'w')
    fp_accomplished.write("accomplished "+str(count))
    fp_accomplished.close()

if __name__=="__main__":
    partition()
