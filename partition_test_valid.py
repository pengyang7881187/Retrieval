size = 15000 

def partition():
    fp_read = open("STC/testS", 'r')
    fp_write1 = open("STC/valid", 'w')
    fp_write2 = open("STC/test", 'w')
    count = 0
    for line in fp_read:
        if count <= size:
            fp_write1.write(line)
        else:
            fp_write2.write(line)
        count += 1
    fp_read.close()
    fp_write1.close()
    fp_write2.close()

if __name__=="__main__":
    partition()
