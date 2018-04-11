import Levenshtein
import random
import dealData
from mpi4py import MPI
import sys
import time

#misspellfilepath = 'misspell.txt'
#correctfilepath = 'correct.txt'
misspellfilepath = 'm_edit.txt'
correctfilepath = 'c_edit.txt'
dictpath = 'dictionary.txt'

#file to record result
resultpath = 'result.txt'

def master_process(comm, misspellfilepath, correctfilepath, size, start_time):
    #count how many words to be corrected
    count = 0
    print 'start'
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
    #print the results
    print ' GED '+str(size)+' cores'
    print 'accuracy: '+str(accuracycount/count)
    print 'precision: '+str(recallcount/predictcount)
    print 'recall: '+str(recallcount/count)
    print 'predict: '+str(predictcount)

    end_time = time.time()
    print 'spend'+str(end_time-start_time)+'s'

#slave_process
def slave_process(comm, rank, size, dictpath):
    #initialize
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
                matchList = bestMatch(mline,dictpath)
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
def bestMatch(string, dictpath):
    with open(dictpath, 'r') as f:
        #word = f.readline().strip()
        wordlist=[]
        lenth='inf'
        for word in f:
            word = word.strip()
            len = Levenshtein.distance(string, word)
            if len < lenth:
                wordlist = []
                wordlist.append(word)
                lenth = len
            elif len == lenth:
                wordlist.append(word)
        return wordlist

def main():
    #get the info
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    if size == 1:
        s = time.time()
        dealData.main(misspellfilepath, correctfilepath, dictpath)
        e = time.time()
        print e - s
    else:
        if rank == 0:
            start_time = time.time()
            master_process(comm, misspellfilepath, correctfilepath, size, start_time)
        else:
            slave_process(comm, rank, size, dictpath)


# Run the actual program
if __name__ == "__main__":
    main()
