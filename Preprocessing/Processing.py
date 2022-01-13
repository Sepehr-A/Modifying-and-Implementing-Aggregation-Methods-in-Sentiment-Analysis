import time
import pandas
from nltk.tokenize import sent_tokenize, word_tokenize
from progress.bar import ChargingBar
from NEW import AggregationMethods as AM
from NEW.PFUNCZ import *

start = time.time()
DatasetName = ["CitySearch", 'TripAdvisor']
LexiconName = ['sentiwordnet3(orderd)', 'SentiSTRLexicon']
LXName = LexiconName[0]
DSName = DatasetName[0]
a = -1
b = 1
c = 1
d = 5
telorance = 0.3
dataSet = pandas.read_excel("Dataset/" + DSName + "(New).xlsx")
Reviewz = list(dataSet["Text"])
Scorez = list(dataSet["Rate"])

Lexiconpath = "Dataset/" + LXName + ".xlsx"
lexiconSheet = pandas.ExcelFile(Lexiconpath)
lexicon_words = []
lexicon_Score = []
print('Initializing...')
for i in lexiconSheet.sheet_names:
    lexicon = pandas.read_excel(Lexiconpath, sheet_name=i)
    lexicon_words.append(list(lexicon[i]))
    lexicon_Score.append(list(lexicon['score']))


# =======================================
def word_finder(words):
    tmp = []
    for w in words:
        sheetNum = lexiconSheet.sheet_names.index(w[0])
        if w in lexicon_words[sheetNum]:
            inDEX = lexicon_words[sheetNum].index(w)
            tmp.append(lexicon_Score[sheetNum][inDEX])
        else:
            matched = word_match(word=w)
            if matched[0] >= 0.75 and matched[1] != w:
                sheetNum = lexiconSheet.sheet_names.index(matched[1][0])
                if matched[1] in lexicon_words[sheetNum]:
                    inDEX = lexicon_words[sheetNum].index(matched[1])
                    tmp.append(lexicon_Score[sheetNum][inDEX])
    # while 0 in tmp:
    # tmp.remove(0)
    if len(tmp) != 0:
        return sum(tmp) / len(tmp)
    else:
        return -100


# ======================================
OWA = []
DempsterShefer = []
sumOfMax = []
maxOfScore = []
IOWA = []
CrossRatio = []
simpleAvg = []
counter = 0
bar = ChargingBar('Processing', max=3000)
for cell in Reviewz:
    Sentences = sent_tokenize(cell, 'english')  # <class 'list'>
    Sentz_Scorez = []
    for sentnce in Sentences:  # <class 'str'>
        QueStion = Question_sent_detect(sentnce, qSign=True)
        NeGative = Negative_sent_detection(sentnce)
        sentnce = remove_special_characters(sentnce)
        WordZset = word_tokenize(sentnce, 'english')  # <class 'list'>
        if not QueStion and len(WordZset) != 0:
            QueStion = Question_sent_detect(WordZset, wh=True)
        WordZset = remove_stopword(WordZset)
        if QueStion:
            Sentz_Scorez.append(0)
        else:
            score_of_sent = word_finder(WordZset)
            if score_of_sent != -100:
                if NeGative:
                    score_of_sent = - score_of_sent
                Sentz_Scorez.append(score_of_sent)
    if len(Sentz_Scorez) != 0:
        OWA.append(AM.OWA(Sentz_Scorez, a, b, c, d))
        IOWA.append(AM.IOWA(Sentz_Scorez, a, b, c, d, telorance))
        DempsterShefer.append(AM.DempsterShefer(Sentz_Scorez, a, b, c, d))
        sumOfMax.append(AM.sumOfMax(Sentz_Scorez, a, b, c, d))
        maxOfScore.append(AM.maxOfScore(Sentz_Scorez, a, b, c, d))
        CrossRatio.append(AM.CrossRatio(Sentz_Scorez, 0.5, a, b, c, d))
        simpleAvg.append(((((sum(Sentz_Scorez) / len(Sentz_Scorez) - a) / (b - a)) * (d - c)) + c))
    else:
        OWA.append('NoN')
        IOWA.append('NoN')
        DempsterShefer.append('NoN')
        sumOfMax.append('NoN')
        maxOfScore.append('NoN')
        CrossRatio.append('NoN')
        simpleAvg.append('NoN')
    bar.next()
    output_file = open('filepath.txt', 'w')
    counter = counter + 1
    output_file.write(str(counter))
    output_file.close()

writer = pandas.ExcelWriter("{0}(Aggr_Result).xlsx".format(DSName), engine='xlsxwriter')

DataSet = pandas.DataFrame(
    {'Reviewz': Reviewz, 'Real Rate': Scorez, 'IOWA': IOWA, 'OWA': OWA,
     'DempsterShefer': DempsterShefer, 'sumOfMax': sumOfMax, 'maxOfScore': maxOfScore, 'CrossRatio': CrossRatio,
     'simpleAvg': simpleAvg})
DataSet.to_excel(writer, sheet_name='Sheet1')
DataSet = pandas.DataFrame([
    'lexicon=' + str(LXName),
    'telorance=' + str(telorance),
    'using word match'
])
DataSet.to_excel(writer, sheet_name='info', index=False, header=False)
writer.save()
bar.finish()
output_file = open('filepath.txt', 'a')
output_file.write('\nDone Sir\n')
end = time.time()
output_file.write(str(end - start))
output_file.close()
