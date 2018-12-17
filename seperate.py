import sys,os
def seperate():
    f_read = open("./STC/train",'r')
    file_count = 0
    content = []
    for line in f_read:
        f_write1 = open("./train_context/"+str(file_count),'w')
        f_write2 = open("./train_replies/"+str(file_count),'w')
        
        line = line.strip('\n')
        content = line.split('\t')
        
        f_write1.write(content[0])
        f_write2.write(content[1])
        f_write1.close()
        f_write2.close()
        file_count += 1
        if(file_count%10000==0):
            print "add ",str(file_count)
        content = []
    f_write = open("accomplish",'w')
    f_write.write("accomplished all over "+str(file_count)+"\n")
    f_write.close()
    f_read.close()
    print("accomplished\n")
if __name__=="__main__":
    seperate()

