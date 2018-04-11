#Spelling Correction Methods

##Introduction

####This project aims to compare and analyze the performance of four spelling correction methods which are N-Gram and Global Edit Distance, Jaro Distance and Jaro_Winkler Distance, based on a peculiar data set. Performance are evaluated on three methods which are accuracy, precision and recall ratio.
####In order to have faster computation, I implement MPI in this project. To run program on 8 cores is turned out to have the best performance, at least on my MacPro. ;)##Usage
####Firstly, there are some dependent libraries you should install:  
* Levenshtein
* mpi4py
* ngram

####Then
    #Python 2.7.10
    #N is how many cores you'd like to use. 8 cores recommended.
    #file.py is the file of correction method you'd like to use.
    mpirun -np N python file.py####Output, which comprises of accuracy, precision, recall ratio and time cost, will print in the console.
####Correction result will record in resultpath which is hardcoded in the top of every method file.

####If you would like to clean dataset firstly, following is the way to do it:
    python preprocess.py
###Attention
####If you would like to use other dataset other than the three files, just change the file name in the top of the correction method files, same as the preprocess.py .####Make sure your node is more than 1, if not, things will be really slow.##DataSet

* misspell.txt :


###### A list of 716 headwords, one per line, that have been automatically identified as misspelled.
* correct.txt :

###### The correct spelling for each of the 716 misspelled headwords, one per line.
* dictionary.txt :


###### A list of about 400K tokens from the English language, which is compiled from various sources.


##Preprocessing:
####preprocess.py is used to preprocess the dataset. The cleaned data file is named as 'correct.txt' -> 'c_edit.txt'.

##Correction Methods

* Levenshtein Distance : Lev_mpi.py
* N-Gram :NGram_mpi.py
* Jaro :jaro_mpi.py
* Jaro\_Winkler : jaro\_Winkler_mpi.py

##Evaluation Metrics
*	Accuracy: Algorithms predict only one most possible headword. When it is exact the correct headword, we count that as a correct prediction. Then calculate the proportion of the number of being successfully predicted to the number of attempted headwords. High accuracy means the method can output a single word and the word is the right prediction.*	Precision: Algorithms predict one or more possible headwords. Count as a correct prediction when the correct headword is in the result. Calculate the proportion of the number of being successfully predicted to the number of whole prediction result. High precision means the method can output the right word out of not too many predictions.*	Recall ratio: Algorithms predict one or more possible headwords. Calculate the proportion of the number of being successfully predicted to the number of attempted headwords.*	Time: Time will be recorded from the start of the program to the end. And this includes the time spent on calculating accuracy, precision and recall.These four terms indicate four aspects of performance of the algorithms.  Under different circumstances, the most valued term is different.

##Analysis
####Based on the experimental dataset, I have analyzed the performance of four spelling correction methods. Except Jaro-Winkler method, all three methods could be used under different circumstances. When the output needs to be a single best matched word, then we value accuracy more than other factors. Then Levenshtein method is the best choice. Same when recall ratio is what we concern about. When it comes to speed, Jaro method is a good choice. With respect to 3-Gram method, it can be used when precision is the most important factor.