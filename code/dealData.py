import Levenshtein
import time
import random

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

def precision(wordList, correctfilepath):
    accuracy_count = 0
    precision_count = 0
    recall_count = 0
    predict_count = 0.0
    with open(correctfilepath, 'r') as f:
        word = f.readline().strip()
        i = 0.0
        while(word != ''):
            predict_count = predict_count + len(wordList[int(i)])
            if word == random.sample(wordList[int(i)], 1)[0]:
                accuracy_count = accuracy_count + 1
            if word in wordList[int(i)]:
                #print 'match'
                recall_count = recall_count + 1
            word = f.readline().strip()
            i = i + 1
        #print results
        print 'accuracy: '+str(accuracy_count/i)
        print 'precision: '+str(recall_count/predict_count)
        print 'recall: '+str(recall_count/i)


def main(misspellfilepath, correctfilepath, dictpath):
    with open(misspellfilepath, 'r') as f:
        line = f.readline().strip()
        matchedWord = []
        while(line!=''):
            matchedWord.append(bestMatch(line, dictpath))
            line = f.readline().strip()
        precision(matchedWord, correctfilepath)

if __name__ == "__main__":
    main()


