batch_src = "batch1/batch_src_raw"
batch_left = "batch1/batch_src_left"
size = 1043580

def seperate():
    fp_read = open(batch_src, 'r')
    fp_write = open(batch_left, 'w')
    count = 0
    for line in fp_read:
        if count < size:
            count+=1
            continue
        fp_write.write(line)
    return




if __name__=="__main__":
    seperate()
