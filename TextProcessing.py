import xlwt
from nltk.corpus import stopwords, wordnet
from xlrd import open_workbook
from collections import defaultdict
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer, SnowballStemmer, LancasterStemmer
from nltk.sentiment.util import *
from functools import reduce
import time

start = time.time()

# Set DataSet & Lexicon Name
DatasetName = "YelpDataSet.xlsx"
LexiconName = "SentiSTRLexicon.xlsx"
LexiconName2 = "NRC-v0.92-Nov2017_Score.xlsx"
ExelResultName = "YelpResult.xls"

snowballStem = SnowballStemmer("english")
porterStem = PorterStemmer()
lancasterStem = LancasterStemmer()
lemmatizer = WordNetLemmatizer()

Lexicon = open_workbook('Data/Lexicon/' + LexiconName)
Lexicon2 = open_workbook('Data/Lexicon/' + LexiconName2)
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Sheet1")

# dataset = DataSet.sheet_by_index(0)
LexiconData = Lexicon.sheet_by_index(0)
LexiconData2 = Lexicon2.sheet_by_index(0)

StopWord = set(stopwords.words('english'))

extraStopWord = ["<br>", ':', '#', '<', '>', 'ب┬', '!', ',', "'ve", '$', '┬ب', '...', '^', '@', '^', '*', '=', "?", '"',
                 '`',
                 '+', "'m", '-', ';', ')', '?', '(', "'s", "'ll", '-/', '[', ']', '{', '}', "'", '~', '`', '\\n', '\\t',
                 "."]

wholeWord = ['can', 'hasn', 'again', 'be', 'the', 'yourself', "you're", "couldn't", "didn't", 'our',
             'until', "hasn't", 'didn', 'each', 'it', 'into', 'through', 'below', 'other', 'being', 'both', 'some',
             'hers', 'this', 'in', 'few', 'what', 'most', "doesn't", 'i', "aren't", 'further', 'do', 'doesn',
             'before', 'when', 'too', 'your', 'shouldn', 'mightn', 'her', "mightn't", "don't", 'or', 'from', 'he',
             'but', 'between', 'then', 'theirs', 'has', 'only', 'if', 'whom', 'yours', 'there', 'all', 'such',
             'she', 'we', 'by', 'more', "should've", 'were', 'ma', 'been', 'not', 'hadn', 'couldn', 'is', 'its',
             'of', 'have', 'isn', "weren't", 'own', 'don', "wouldn't", 'needn', 'me', "you'll", 'having',
             'how', "needn't", 'myself', 'these', 'haven', 'than', 'him', 'themselves', 'on', 'as', '', 'same',
             'are', 'them', 'now', 'where', "haven't", 'itself', 'ourselves', 'any', 'at', "it's", 'doing',
             'wouldn', 'was', 'with', 'herself', 'those', 'out', 'to', 'off', "hadn't", 'that', 'about', "you'd",
             'weren', 'nor', 'an', 'himself', 'above', 'very', 'up', 'down', 'during', 'while',
             "mustn't", "that'll", "she's", 'wasn', 'their', 'for', 'had', 'did', 'll', "wasn't", 'will', 'after',
             'no', 'am', 'under', 're', 'because', 'just', 'here', 'yourselves', 'so', 'you', "you've", 'aren',
             'mustn', 'my', 'they', 've', "won't", 'once', 'and', 'does', 'his', 'should', 'ours', 'ain', "shan't",
             'over', "shouldn't", "isn't", 'shan', 's', 'y', 'm', 'd', 'o', 't',
             'a', '.', "br"]

LexiconWords = [word.lower() for word in LexiconData.col_values(0, 0, LexiconData.nrows)]
LexiconRates = LexiconData.col_values(2, 0, LexiconData.nrows)
LexiconWords2 = [word1.lower() for word1 in LexiconData2.col_values(1, 1, LexiconData2.nrows)]
LexiconRates2 = LexiconData2.col_values(2, 1, LexiconData2.nrows)
questionWords = ["who", "what", " when", " where", " why", " how", " is", " can", " does", " do", "which", "wanna",
                 "would", "should", "could", "are", "am", "was", "were"]


# ===========================
def removeStopwords(sentnce):
    sentnce = str(sentnce)
    # if "<br>" in sentnce:
    #     sentnce = sentnce.replace("<br>", " ")
    #     sentnce = sent_tokenize(sentnce, "english")
    # for s in sentnce:
    # print(sentnce)
    NegSentence = False
    QSentence = False
    if sentnce.endswith("?"):
        QSentence = True
    for k in extraStopWord:
        sentnce = sentnce.replace(k, " ")
    print("sentnce:", sentnce)
    s = word_tokenize(sentnce, "english")
    print("s", s)
    y = []
    if len(s) > 0:
        if s[0] in questionWords:
            QSentence = True
        for i in s:
            if NEGATION_RE.search(i):
                NegSentence = True
            if i not in wholeWord:
                y.append(i)
        # e = list(filter(lambda r: r is not '', y))
        y.append(QSentence)
        y.append(NegSentence)
        print("y:", y)
        input()
        return y
    else:
        return [False, False]


# ===============
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ""


# ===============
def CheckStemOrLemmatize(word, SntPosTag):
    """
    check a word stem and lemmatize
    """
    anotherTypeOfWord = [word]
    if word != snowballStem.stem(word):
        anotherTypeOfWord.append(snowballStem.stem(word))
    if word != porterStem.stem(word) and porterStem.stem(word) not in anotherTypeOfWord:
        anotherTypeOfWord.append(porterStem.stem(word))
    if word != lancasterStem.stem(word) and lancasterStem.stem(word) not in anotherTypeOfWord:
        anotherTypeOfWord.append(lancasterStem.stem(word))
    for i, v in SntPosTag:
        if i == word:
            v = get_wordnet_pos(v)
            if v != "":
                if word != lemmatizer.lemmatize(word, pos=v) and lemmatizer.lemmatize(word,
                                                                                      pos=v) not in anotherTypeOfWord:
                    anotherTypeOfWord.append(lemmatizer.lemmatize(word, pos=v))
                break
            else:
                if word != lemmatizer.lemmatize(word) and lemmatizer.lemmatize(word) not in anotherTypeOfWord:
                    anotherTypeOfWord.append(lemmatizer.lemmatize(word))
                break
    return anotherTypeOfWord


def CellAnalyze(cell):
    Sentence = sent_tokenize(cell, "english")
    print("Sentence: ", Sentence)
    input()
    sntcScore = []
    for sntc in Sentence:
        sntc = removeStopwords(sntc)
        NegativeSentence = sntc.pop(-1)
        QuestionSentence = sntc.pop(-1)
        sntcPOStag = nltk.pos_tag(sntc)
        print("sntnc:", sntc)
        score = []
        d = []
        if len(sntc) > 0:
            if not QuestionSentence:
                for wordz in sntc:
                    allTypeWordz = CheckStemOrLemmatize(wordz, sntcPOStag)
                    for w in allTypeWordz:
                        if w in LexiconWords:
                            tmp = LexiconRates[LexiconWords.index(w)]
                            d.append(w)
                            if not NegativeSentence:
                                score.append(tmp)
                            else:
                                score.append(6 - tmp)
                            break
                        elif w in LexiconWords2:
                            d.append(w)
                            tmp = LexiconRates2[LexiconWords2.index(w)]
                            if not NegativeSentence:
                                score.append(tmp)
                            else:
                                score.append(6 - tmp)
                            break
                if len(score) > 0:
                    print("score: ", score)
                    sntcScore.append(sum(score) / len(score))
            else:
                sntcScore.append(3)
        print("d",d)
    print("sntcScore: ", sntcScore)
    input()
    return sntcScore


def normalizer(datasetAddress, sheetIndex, reviewNum=0, possibleMaxReviews=False):
    DataSet = open_workbook(datasetAddress)
    dataset = DataSet.sheet_by_index(sheetIndex)
    datasetDick = defaultdict(list)
    for i in range(1, dataset.nrows - 1):
        if dataset.cell_value(i, 2) == 1:
            datasetDick['one'].append(dataset.cell_value(i, 1))
        elif dataset.cell_value(i, 2) == 2:
            datasetDick['two'].append(dataset.cell_value(i, 1))
        elif dataset.cell_value(i, 2) == 3:
            datasetDick['three'].append(dataset.cell_value(i, 1))
        elif dataset.cell_value(i, 2) == 4:
            datasetDick['four'].append(dataset.cell_value(i, 1))
        elif dataset.cell_value(i, 2) == 5:
            datasetDick['five'].append(dataset.cell_value(i, 1))
    minReviewNum = min(len(datasetDick['one']), len(datasetDick['two']),
                       len(datasetDick['three']), len(datasetDick['four']),
                       len(datasetDick['five']))
    if possibleMaxReviews:
        for rate, reviews in datasetDick.items():
            hhh = datasetDick[rate]
            while len(datasetDick[rate]) > minReviewNum:
                del hhh[-1]
        return datasetDick
    else:
        if reviewNum <= minReviewNum:
            for rate, reviews in datasetDick.items():
                hhh = datasetDick[rate]
                while len(datasetDick[rate]) > reviewNum:
                    del hhh[-1]
            return datasetDick
        else:
            print("cant create that")


# ====== Methods
def DempsterShefer(ScoreArray):
    mTotal = 0
    indexCheck = True
    for score in ScoreArray:
        mScore = (score - 1) / 4
        if mScore == 0:
            mScore = 0.001
        if ScoreArray.index(score) == 0 and indexCheck:
            mTotal = mScore
            indexCheck = False
        elif ((1 - mTotal) * mScore + ((1 - mScore) * mTotal)) != 1:
            mTotal = (mTotal * mScore) / (1 - ((1 - mTotal) * mScore + ((1 - mScore) * mTotal)))
        else:
            mTotal = 0

    finalScore = (mTotal * 4 + 1)
    return finalScore


def sumOfMax(ScoreArray):
    minimum = min(ScoreArray)
    maximum = max(ScoreArray)
    finalScore = maximum - minimum
    return finalScore


def maxOfScore(ScoreArray):
    minimum = min(ScoreArray)
    maximum = max(ScoreArray)
    # changing scale to -5,5
    minimum = (((minimum - 1) / 4) * 10) - 5
    maximum = (((maximum - 1) / 4) * 10) - 5
    if abs(maximum) > abs(minimum):
        finalScore = maximum
    elif abs(maximum) < abs(minimum):
        finalScore = minimum
    else:
        finalScore = maximum
    # returning scale to 1-5
    finalScore = (((finalScore + 5) / 10) * 4) + 1
    return finalScore


def scaledRate(ScoreArray):
    positive = 0
    negetive = 0
    for score in ScoreArray:
        if score > 3:
            positive = positive + 1
        if score < 3:
            negetive = negetive + 1
    if positive + negetive != 0:
        finalScore = ((positive * 4) / (positive + negetive)) + 1
    else:
        finalScore = 0
    return finalScore


def Q(r, a, b):
    if r < a or r == 0:
        return 0
    elif r > b or r == 1:
        return 1
    elif a <= r:
        if r <= b:
            return (r - a) / (b - a)


def OWA(ScoreArray):
    lengthArray = len(ScoreArray)
    ScoreArray = sorted(ScoreArray, reverse=True)
    owa1 = 0
    owa2 = 0
    owa3 = 0
    for i in range(1, lengthArray + 1):
        owa1 += (Q(i / lengthArray, 0, 0.5) - Q((i - 1) / lengthArray, 0, 0.5)) * ScoreArray[i - 1]
        owa2 += (Q(i / lengthArray, 0.3, 0.8) - Q((i - 1) / lengthArray, 0.3, 0.8)) * ScoreArray[i - 1]
        owa3 += (Q(i / lengthArray, 0.5, 1) - Q((i - 1) / lengthArray, 0.5, 1)) * ScoreArray[i - 1]
    finalOWA = [owa1, owa2, owa3]
    return sum(finalOWA) / 3


def CrossRatio(ScoreArray, e):
    if (0 in ScoreArray) and (1 in ScoreArray):
        return 0
    else:
        multipleOfList = reduce((lambda i, j: i * j), ScoreArray)
        minusOne = reduce((lambda k, l: k * l), list(map(lambda x: x - 1, ScoreArray)))
        Numerator = ((1 - e) ** (len(ScoreArray) - 1)) * multipleOfList
        Denominator = Numerator + ((e ** (len(ScoreArray) - 1)) * minusOne)
        return Numerator / Denominator


# ===========================

datasetDick = normalizer('Data/Dataset/' + DatasetName, 0, 0, True)

sheet1.write(0, 0, "simpleAvg")
sheet1.write(0, 1, "DempsterShefer")
sheet1.write(0, 2, "sumOfMax")
sheet1.write(0, 3, "maxOfScore")
sheet1.write(0, 4, "scaledRate")
sheet1.write(0, 5, "OWA")
sheet1.write(0, 6, "CrossRatio")
sheet1.write(0, 7, "REVIEWS")

j = 0
for rate, reviews in datasetDick.items():
    normalizedReview = datasetDick[rate]

    for i in normalizedReview:
        j = j + 1
        SenteceScores = CellAnalyze(i.lower())
        if len(SenteceScores) == 0:
            simpleAvgScore = 0
            DempsterSheferScore = 0
            sumOfMaxScore = 0
            scaledRateScore = 0
            maxOfScor = 0
            owaScore = 0
            CrossRatioScore = 0
        else:
            simpleAvgScore = sum(SenteceScores) / len(SenteceScores)
            DempsterSheferScore = DempsterShefer(SenteceScores)
            sumOfMaxScore = sumOfMax(SenteceScores)
            maxOfScor = maxOfScore(SenteceScores)
            scaledRateScore = scaledRate(SenteceScores)
            owaScore = OWA(SenteceScores)
            CrossRatioScore = CrossRatio(SenteceScores, 0.5)

        sheet1.write(j, 0, simpleAvgScore)
        sheet1.write(j, 1, DempsterSheferScore)
        sheet1.write(j, 2, sumOfMaxScore)
        sheet1.write(j, 3, maxOfScor)
        sheet1.write(j, 4, scaledRateScore)
        sheet1.write(j, 5, owaScore)
        sheet1.write(j, 6, CrossRatioScore)
        sheet1.write(j, 7, i)
book.save('Data/' + ExelResultName)

print(time.time() - start)
