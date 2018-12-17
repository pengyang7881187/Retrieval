
def counting():
    fp_write = open("size_of_train",'w')
    fp_read = open("STC/trainS", 'r')
    count = 0
    for line in fp_read:
        count+=1
    fp_write.write(str(count))
    fp_read.close()
    fp_write.close()

if __name__=="__main__":
    counting()
