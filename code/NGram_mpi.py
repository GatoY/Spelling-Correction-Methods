import ngram
import random
import dealData
from mpi4py import MPI
import sys
import time

#misspellfilepath = 'm.txt'
#correctfilepath = 'c.txt'
#misspellfilepath = 'misspell.txt'
#correctfilepath = 'correct.txt'
misspellfilepath = 'm_edit.txt'
correctfilepath = 'c_edit.txt'
dictpath = 'dictionary.txt'

#file to record result
resultpath = 'result.txt'

def master_process(comm, misspellfilepath, correctfilepath, dictpath, size, start_time):
    #count how many words to be corrected
    count = 0
    print 'start'
    n = 2
    #send gram list of dictionary to slave_process
    with open(dictpath, 'r') as f:
        list = f.readlines()
        for i in range(len(list)):
            list[i] = list[i].strip()
        G = ngram.NGram(list, N=n)

    for i in range(size-1):
        comm.send(G, dest=(i % (size - 1) + 1), tag=(i % (size - 1) + 1))

    #send misspelled words and correct words to slave_process
    with open(misspellfilepath) as mf:
        with open(correctfilepath) as cf:
            for mline in mf:
                mline= mline.strip()
                cline = cf.readline().strip()
                count = count + 1
                comm.send(mline, dest=(count % (size - 1) + 1), tag=(count % (size - 1) + 1))
                comm.send(cline, dest=(count % (size - 1) + 1), tag=(count % (size - 1) + 1))
    print 'all words sent'
    
    #ask slave_process to exit
    for i in range(size-1):
        comm.send('exit', dest=(i % (size - 1) + 1), tag=(i % (size - 1) + 1))
        comm.send('exit', dest=(i % (size - 1) + 1), tag=(i % (size - 1) + 1))

    #used to receive data from slave_process
    correctcount = 0.0
    #if one single prediction is correct, count
    accuracycount = 0.0
    #if correct word is in the list of predictions, count
    recallcount = 0.0
    #count the number of predictions
    predictcount = 0.0
    
    for i in range(size-1):
        #receive result from slave_process
        correctcount = comm.recv(source=(i+1),tag = (i+1))
        accuracycount = accuracycount + correctcount[0]
        recallcount = recallcount + correctcount[1]
        predictcount = predictcount + correctcount[2]

    #print results
    print str(n)+'-gram on '+str(size)+' cores'
    print 'accuracy: '+str(accuracycount/count)
    print 'precision: '+str(recallcount/predictcount)
    print 'recall: '+str(recallcount/count)
    print 'predict: '+str(predictcount)
    end_time = time.time()
    print 'spend'+str(end_time-start_time)+'s'

#slave_process
def slave_process(comm, rank, size):
    G= comm.recv(source=(0), tag=rank)
    accuracy_count = 0
    precision_count = 0
    recall_count = 0
    predict_count = 0
    with open(resultpath,'w+') as f:
        while (1):
            mline = comm.recv(source=(0), tag=rank)
            cline = comm.recv(source=(0), tag=rank)
            if mline == "exit":
                count = [accuracy_count, recall_count, predict_count]
                comm.send(count, dest=(0), tag=rank)
            exit(0)
            else:
                matchList = bestMatch(mline, G)
                for i in matchList:
                    f.write(i+' ')
                f.write('\n')
                predict_count = predict_count + len(matchList)
                #accuracy
                if cline in random.sample(matchList, 1):
                    accuracy_count = accuracy_count + 1
                if cline in matchList:
                    recall_count = recall_count + 1

#find the best match in dictionary
def bestMatch(string, G):
        wordlist=[]
        max=-1
        result_dist = G.search(string)
        for i in result_dist:
            len = i[1]
            if len>max:
                wordlist=[]
                wordlist.append(i[0])
                max = len
            elif len==max:
                wordlist.append(i[0])
        return wordlist

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    if size == 1:
        s = time.time()
        dealData.main(misspellfilepath, correctfilepath, dictpath)
        e = time.time()
        print
        e - s
    else:
        if rank == 0:
            start_time = time.time()
            master_process(comm, misspellfilepath, correctfilepath, dictpath, size, start_time)
        else:
            slave_process(comm, rank, size)


# Run the actual program
if __name__ == "__main__":
    main()
