import sys,os
# This file is for multi-round dialogue
def seperate():
    f_read = open("./train.txt",'r')
    count = 0
    period_count=0
    file_count = 0
    context = []
    for line in f_read:
        if line !="\n":
            context.append(line)
            count += 1
        else:
            f_write1 = open("./train_context_query/"+str(file_count),'w')
#            f_write2 = open("./train_replies/"+str(file_count),'w')
            f_write1.write(context[-2])
#            f_write2.write(context[-1])
            f_write1.close()
#            f_write2.close()
            count = 0
            file_count += 1
            period_count += 1
            if(period_count==10000):
                print("%d\n" %(file_count))
                period_count=0
            context.clear()
            assert len(context)==0
    f_write = open("accomplish_only_query",'w')
    f_write.write("accomplished all over "+str(file_count)+"\n")
    f_write.close
    f_read.close()
    print("accomplished\n")
if __name__=="__main__":
    seperate()

