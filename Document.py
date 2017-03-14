#!/usr/bin/python
import sys
import argparse
#from stop_words import get_stop_words



#disclaimer : I hope this program is working fine in terms of functionality, but it is taking an awful lot of time,
#as I am new to python and is in transition period of fully converting from java to python, I am still not aware of
#full potential and availability of various data structures of python, but I think that I can do better, so I would
#try tommarow to make it more time efficient.
#Thank You

class learning(object):
    #list of common stop words picked up from source from google (also used stop_words library which is currently commented out
    stop = ['a',
                    'about',
                    'above',
                    'after',
                    'again',
                    'against',
                    'all',
                    'am',
                    'an',
                    'and',
                    'any',
                    'are',
                    'arent',
                    'as',
                    'at',
                    'be',
                    'because',
                    'been',
                    'before',
                    'being',
                    'below',
                    'between',
                    'both',
                    'but',
                    'by',
                    'cant',
                    'cannot',
                    'could',
                    'couldnt',
                    'did',
                    'didnt',
                    'do',
                    'does',
                    'doesnt',
                    'doing',
                    'dont',
                    'down',
                    'during',
                    'each',
                    'few',
                    'for',
                    'from',
                    'further',
                    'had',
                    'hadnt',
                    'has',
                    'hasnt',
                    'have',
                    'havent',
                    'having',
                    'he',
                    'hed',
                    'hell',
                    'hes',
                    'her',
                    'here',
                    'heres',
                    'hers',
                    'herself',
                    'him',
                    'himself',
                    'his',
                    'how',
                    'hows',
                    'i',
                    'id',
                    'ill',
                    'im',
                    'ive',
                    'if',
                    'in',
                    'into',
                    'is',
                    'isnt',
                    'it',
                    'its',
                    'its',
                    'itself',
                    'lets',
                    'me',
                    'more',
                    'most',
                    'mustnt',
                    'my',
                    'myself',
                    'no',
                    'nor',
                    'not',
                    'of',
                    'off',
                    'on',
                    'once',
                    'only',
                    'or',
                    'other',
                    'ought',
                    'our',
                    'ours',
                    'ourselves',
                    'out',
                    'over',
                    'own',
                    'same',
                    'shant',
                    'she',
                    'shed',
                    'shell',
                    'shes',
                    'should',
                    'shouldnt',
                    'so',
                    'some',
                    'such',
                    'than',
                    'that',
                    'thats',
                    'the',
                    'their',
                    'theirs',
                    'them',
                    'themselves',
                    'then',
                    'there',
                    'theres',
                    'these',
                    'they',
                    'theyd',
                    'theyll',
                    'theyre',
                    'theyve',
                    'this',
                    'those',
                    'through',
                    'to',
                    'too',
                    'under',
                    'until',
                    'up',
                    'very',
                    'was',
                    'wasnt',
                    'we',
                    'wed',
                    'well',
                    'were',
                    'weve',
                    'were',
                    'werent',
                    'what',
                    'whats',
                    'when',
                    'whens',
                    'where',
                    'wheres',
                    'which',
                    'while',
                    'who',
                    'whos',
                    'whom',
                    'why',
                    'whys',
                    'with',
                    'wont',
                    'would',
                    'wouldnt',
                    'you',
                    'youd',
                    'youll',
                    'youre',
                    'youve',
                    'your',
                    'yours',
                    'yourself',
                    'yourselves']

    wordProb = dict() #to store the word probabilities
    classProb = dict() #to store class probabilites
    wordGivenClassProb = dict() #to store probability of a word given a class, key would be in format of word+class, for example
                                # word = "book" , mapped to class 4, then unique key of this dictionary would be "book4"


    def __init__(self,fileName):
        self.fileName = fileName


    def readFile(self):
        with open(self.fileName) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        return (content)


    def training(self):
        #print("started")
        lines = self.readFile()
        lines = lines[1:len(lines)]
        wordCount=0
        clsCount = len(lines)

        wordFreq=dict() #for storing the frequency of each word
        classFreq=dict() #storing frequency of each class 1-8
        wordGivenClass=dict() #storing all words occuring in a class
        #print(lines[0])

        for i in range (1,9):
            wordGivenClass[str(i)]=[]

        #print(wordGivenClass)
        for line in lines:
            words = line.split();
            cls = words[0]
            words = words[1:len(words)]
            if cls in classFreq:
                classFreq[cls] = classFreq[cls]+1
            else:
                classFreq[cls] = 1

            for word in words:
                if word in self.stop or len(word)<3:
                    continue
                wordCount = wordCount + 1
                word = word.lower()
                if word in wordFreq:

                    wordFreq[word] = wordFreq[word]+1
                else:
                    wordFreq[word]=1
                l = wordGivenClass[cls]
                l.append(word)
                wordGivenClass[cls] = l

        #now finding out probabilities of each word


        for i in range (1,9):
            self.classProb[i] = float(classFreq[str(i)])/clsCount

        #print(self.classProb)
        #print(sum(classProb))

        for word,freq in wordFreq.iteritems():
            self.wordProb[word] = float(freq)/wordCount
            for i in range (1,9):
                l = wordGivenClass[str(i)]
                count =  l.count(word)
                newKey = word + str(i)
                self.wordGivenClassProb[newKey] = float(count)/len(l)



        #print(self.wordProb)
        #print("done")




   #function to classify the test case
    def test(self,case):


        words = case.split()
        maxProb = 0.0
        maxclass = 1
        #checking for each class
        for i in range(1,9):
            currentprob=1
            for word in words:
                word = word.lower()
                if word in self.stop or len(word)<3:
                    continue
                if word not in self.wordProb:
                    continue

                key = str(word) + str(i)       #using bayes theorem to find the probability
                currentprob = currentprob*(self.wordGivenClassProb[key] / self.wordProb[word])
            currentprob = currentprob*self.classProb[(i)]
            if maxProb < currentprob:
                maxProb = currentprob
                maxclass = i
        print(maxclass)



# stop = get_stop_words('english')
# for word in stop:
#     print (word)



n = int(input())
inputList = []
for i in range(0,n):
    inp = (raw_input())
    inputList.append(inp)
#print(inputList)
check = learning("trainingdata.txt")
check.training()

for i in inputList:
    check.test(i)


