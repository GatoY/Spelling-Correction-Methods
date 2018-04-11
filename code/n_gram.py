import time
import random
import ngram

def bestMatch(string, dictpath):
    with open(dictpath, 'r') as f:
        word = f.readline().strip()
        wordlist=[]
        lenth='inf'
        while(word != ''):
            len = ngram.NGram.compare(string, word, N=3)
            if len < lenth:
                wordlist = []
                wordlist.append(word)
                lenth = len
            if len == lenth:
                wordlist.append(word)
            word = f.readline().strip()
        return wordlist

def precision(wordList, s, correctfilepath):
    accuracy_count = 0
    precision_count = 0
    recall_count = 0
    predict_count = 0.0
    #print 'precision'
    with open(correctfilepath, 'r') as f:
        word = f.readline().strip()
        i = 0.0
        while(word != ''):
            #print wordList
            #print i
            predict_count = predict_count + len(wordList[int(i)])
            
            if word == random.sample(wordList[int(i)], 1)[0]:
                accuracy_count = accuracy_count + 1
            if word in wordList[int(i)]:
                #print 'match'
                recall_count = recall_count + 1
            word = f.readline().strip()
            i = i + 1
        
        print 'accuracy: '+str(accuracy_count/i)
        print 'precision: '+str(recall_count/predict_count)
        print 'recall: '+str(recall_count/i)
        
        e = time.time()
        print str(e - s) + 's'

def main(misspellfilepath, correctfilepath, dictpath):
    s = time.time()
    with open(misspellfilepath, 'r') as f:
        line = f.readline().strip()
        matchedWord = []
        #print line
        while(line!=''):
            matchedWord.append(bestMatch(line, dictpath))
            line = f.readline().strip()
    #print matchedWord
        precision(matchedWord, s, correctfilepath)

if __name__ == "__main__":
    main()


