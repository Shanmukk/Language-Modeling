"""
Language Modeling Project
Name:
Roll No:
"""

from tkinter.simpledialog import SimpleDialog
from matplotlib.pyplot import title
import language_tests as test
from collections import Counter

project = "Language" # don't edit this

### WEEK 1 ###

'''
loadBook(filename)
#1 [Check6-1]
Parameters: str
Returns: 2D list of strs
'''
def loadBook(filename):
    read = open(filename,"r")
    list = []
    for line in read:
        v = line.split()
        if v:
            list.append(v)
    return list


'''
getCorpusLength(corpus)
#2 [Check6-1]
Parameters: 2D list of strs
Returns: int
'''
def getCorpusLength(corpus):
    count = 0
    for i in corpus:
        count += len(i)
    return count


'''
buildVocabulary(corpus)
#3 [Check6-1]
Parameters: 2D list of strs
Returns: list of strs
'''
def buildVocabulary(corpus):
    l = []
    for i in range(len(corpus)):
        for j in corpus[i]:
            if j not in l:
                l.append(j)
    return l


'''
countUnigrams(corpus)
#4 [Check6-1]
Parameters: 2D list of strs
Returns: dict mapping strs to ints
'''
def countUnigrams(corpus):
    d = {}
    for i in range(len(corpus)):
        for j in corpus[i]:
            if j in d:
                d[j] += 1
            else:
                d[j] = 1
    return d


'''
getStartWords(corpus)
#5 [Check6-1]
Parameters: 2D list of strs
Returns: list of strs
'''
def getStartWords(corpus):
    l = []
    for i in range(len(corpus)):
        if corpus[i][0] not in l:
            l.append(corpus[i][0])
    return l


'''
countStartWords(corpus)
#5 [Check6-1]
Parameters: 2D list of strs
Returns: dict mapping strs to ints
'''
def countStartWords(corpus):
    l = []
    d = {}
    for i in range(len(corpus)):
        l = corpus[i][0]
        if l not in d:
            d[l] = 1
        else:
            d[l] += 1
    return d

'''
countBigrams(corpus)
#6 [Check6-1]
Parameters: 2D list of strs
Returns: dict mapping strs to (dicts mapping strs to ints)
'''
def countBigrams(corpus):
    d = {}
    for i in range(len(corpus)):
        for j in range(len(corpus[i])-1):
            if corpus[i][j] not in d:
                d[corpus[i][j]] = {}
                d[corpus[i][j]][corpus[i][j+1]] = 1
            else:
                if corpus[i][j+1] in d[corpus[i][j]]:
                    d[corpus[i][j]][corpus[i][j+1]] += 1
                else:
                    d[corpus[i][j]][corpus[i][j+1]] = 1
    return d

### WEEK 2 ###

'''
buildUniformProbs(unigrams)
#1 [Check6-2]
Parameters: list of strs
Returns: list of floats
'''
def buildUniformProbs(unigrams):
    l = []
    i = 0
    while i < len(unigrams):
        l.append(1/len(unigrams))
        i += 1
    return l


'''
buildUnigramProbs(unigrams, unigramCounts, totalCount)
#2 [Check6-2]
Parameters: list of strs ; dict mapping strs to ints ; int
Returns: list of floats
'''
def buildUnigramProbs(unigrams, unigramCounts, totalCount):
    l = []
    for index in unigrams:
        if index in unigramCounts:
            l.append(unigramCounts[index]/totalCount)
        else:
            l.append(0)
    return l


'''
buildBigramProbs(unigramCounts, bigramCounts)
#3 [Check6-2]
Parameters: dict mapping strs to ints ; dict mapping strs to (dicts mapping strs to ints)
Returns: dict mapping strs to (dicts mapping strs to (lists of values))
'''
def buildBigramProbs(unigramCounts, bigramCounts):
    d = {}
    for i in bigramCounts:
        keys = []
        probs = []
        for key,value in bigramCounts[i].items():
            temp = {}
            keys.append(key)
            probs.append(value/unigramCounts[i])
            temp["words"] = keys
            temp["probs"] = probs
        d[i] = temp
    return d


'''
getTopWords(count, words, probs, ignoreList)
#4 [Check6-2]
Parameters: int ; list of strs ; list of floats ; list of strs
Returns: dict mapping strs to floats
'''
def getTopWords(count, words, probs, ignoreList):
    d = {}
    g = {}
    for i in range(len(words)):
        if words[i] not in ignoreList:
            d[words[i]] = probs[i]
    k = Counter(d)
    k = k.most_common(count)
    for key,value in k:
        g[key] = value
    return g

'''
generateTextFromUnigrams(count, words, probs)
#5 [Check6-2]
Parameters: int ; list of strs ; list of floats
Returns: str
'''
from random import choices
def generateTextFromUnigrams(count, words, probs):
    s = " "
    for i in range(count):
        l = choices(words, weights=probs)
        s = s + " " + l[0]
    return s


'''
generateTextFromBigrams(count, startWords, startWordProbs, bigramProbs)
#6 [Check6-2]
Parameters: int ; list of strs ; list of floats ; dict mapping strs to (dicts mapping strs to (lists of values))
Returns: str
'''
def generateTextFromBigrams(count, startWords, startWordProbs, bigramProbs):
    s = ""
    l = choices(startWords, weights = startWordProbs)
    s += l[0]
    lst = s
    for i in range(count-1):
        if lst != '.':
            if lst in bigramProbs:
                lst = choices(bigramProbs[lst]["words"], weights = bigramProbs[lst]["probs"])[0]
                s = s + ' ' + lst
        #print(sentence)
        else:
            l = choices(startWords, weights = startWordProbs)
            s = s +' '+ l[0]
            lst = l[0]
    return s

### WEEK 3 ###

ignore = [ ",", ".", "?", "'", '"', "-", "!", ":", ";", "by", "around", "over",
           "a", "on", "be", "in", "the", "is", "on", "and", "to", "of", "it",
           "as", "an", "but", "at", "if", "so", "was", "were", "for", "this",
           "that", "onto", "from", "not", "into" ]

'''
graphTop50Words(corpus)
#3 [Hw6]
Parameters: 2D list of strs
Returns: None
'''
def graphTop50Words(corpus):
    cnt = getCorpusLength(corpus)
    voc = buildVocabulary(corpus)
    unigram = countUnigrams(corpus)
    prob = buildUnigramProbs(voc, unigram, cnt)
    g = getTopWords(50, voc, prob, ignore)
    barPlot(g,"Top 50 words")
    return


'''
graphTopStartWords(corpus)
#4 [Hw6]
Parameters: 2D list of strs
Returns: None
'''
def graphTopStartWords(corpus): 
    start_words = getStartWords(corpus)
    count = countStartWords(corpus)
    cnt = count.values()
    cnt = sum(cnt)
    prob = buildUnigramProbs(start_words, count, cnt) 
    g = getTopWords(50, start_words, prob, ignore) 
    barPlot(g,"Top 50 Start words")
    return


'''
graphTopNextWords(corpus, word)
#5 [Hw6]
Parameters: 2D list of strs ; str
Returns: None
'''
def graphTopNextWords(corpus, word):
    Unigrams = countUnigrams(corpus)
    Bigrams = countBigrams(corpus)
    prob = buildBigramProbs(Unigrams, Bigrams)
    g = getTopWords(10, prob[word]['words'], prob[word]["probs"], ignore)
    barPlot(g, "Top 10 next words")
    return


'''
setupChartData(corpus1, corpus2, topWordCount)
#6 [Hw6]
Parameters: 2D list of strs ; 2D list of strs ; int
Returns: dict mapping strs to (lists of values)
'''
def setupChartData(corpus1, corpus2, topWordCount):
    topWords = []
    dict1 = {}
    cnt1, cnt2 = getCorpusLength(corpus1), getCorpusLength(corpus2) 
    one, two = buildVocabulary(corpus1), buildVocabulary(corpus2)
    count1, count2 = countUnigrams(corpus1), countUnigrams(corpus2)
    prob1, prob2 = buildUnigramProbs(one, count1, cnt1), buildUnigramProbs(two, count2, cnt2)
    g, h = getTopWords(topWordCount, one, prob1, ignore), getTopWords(topWordCount, two, prob2, ignore)
    m = {**g, **h}
    for i in m.items():
        topWords.append(i[0])
    corpus1Probs = buildUnigramProbs(topWords, count1, cnt1)
    corpus2Probs = buildUnigramProbs(topWords, count2, cnt2)
    dict1["topWords"] = topWords
    dict1["corpus1Probs"] = corpus1Probs
    dict1["corpus2Probs"] = corpus2Probs
    return dict1
 

'''
graphTopWordsSideBySide(corpus1, name1, corpus2, name2, numWords, title)
#6 [Hw6]
Parameters: 2D list of strs ; str ; 2D list of strs ; str ; int ; str
Returns: None
'''
def graphTopWordsSideBySide(corpus1, name1, corpus2, name2, numWords, title):
    top = setupChartData(corpus1,corpus2, numWords)
    sideBySideBarPlots(top['topWords'], top["corpus1Probs"], top["corpus2Probs"], name1, name2, title)
    return


'''
graphTopWordsInScatterplot(corpus1, corpus2, numWords, title)
#6 [Hw6]
Parameters: 2D list of strs ; 2D list of strs ; int ; str
Returns: None
'''
def graphTopWordsInScatterplot(corpus1, corpus2, numWords, title):
    top = setupChartData(corpus1,corpus2, numWords)
    scatterPlot(top["corpus1Probs"], top["corpus2Probs"], top['topWords'], title)
    return


### WEEK 3 PROVIDED CODE ###

"""
Expects a dictionary of words as keys with probabilities as values, and a title
Plots the words on the x axis, probabilities as the y axis and puts a title on top.
"""
def barPlot(dict, title):
    import matplotlib.pyplot as plt

    names = []
    values = []
    for k in dict:
        names.append(k)
        values.append(dict[k])

    plt.bar(names, values)

    plt.xticks(rotation='vertical')
    plt.title(title)

    plt.show()

"""
Expects 3 lists - one of x values, and two of values such that the index of a name
corresponds to a value at the same index in both lists. Category1 and Category2
are the labels for the different colors in the graph. For example, you may use
it to graph two categories of probabilities side by side to look at the differences.
"""
def sideBySideBarPlots(xValues, values1, values2, category1, category2, title):
    import matplotlib.pyplot as plt

    w = 0.35  # the width of the bars

    plt.bar(xValues, values1, width=-w, align='edge', label=category1)
    plt.bar(xValues, values2, width= w, align='edge', label=category2)

    plt.xticks(rotation="vertical")
    plt.legend()
    plt.title(title)

    plt.show()

"""
Expects two lists of probabilities and a list of labels (words) all the same length
and plots the probabilities of x and y, labels each point, and puts a title on top.
Note that this limits the graph to go from 0x0 to 0.02 x 0.02.
"""
def scatterPlot(xs, ys, labels, title):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    plt.scatter(xs, ys)

    # make labels for the points
    for i in range(len(labels)):
        plt.annotate(labels[i], # this is the text
                    (xs[i], ys[i]), # this is the point to label
                    textcoords="offset points", # how to position the text
                    xytext=(0, 10), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center

    plt.title(title)
    plt.xlim(0, 0.02)
    plt.ylim(0, 0.02)

    # a bit of advanced code to draw a y=x line
    ax.plot([0, 1], [0, 1], color='black', transform=ax.transAxes)

    plt.show()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    '''print("\n" + "#"*15 + " WEEK 1 TESTS " +  "#" * 16 + "\n")
    test.week1Tests()
    print("\n" + "#"*15 + " WEEK 1 OUTPUT " + "#" * 15 + "\n")
    test.runWeek1()'''

    ## Uncomment these for Week 2 ##
    
    '''print("\n" + "#"*15 + " WEEK 2 TESTS " +  "#" * 16 + "\n")
    test.week2Tests()
    print("\n" + "#"*15 + " WEEK 2 OUTPUT " + "#" * 15 + "\n")
    test.runWeek2()'''
    

    ## Uncomment these for Week 3 ##
    
    print("\n" + "#"*15 + " WEEK 3 OUTPUT " + "#" * 15 + "\n")
    test.runWeek3()
    