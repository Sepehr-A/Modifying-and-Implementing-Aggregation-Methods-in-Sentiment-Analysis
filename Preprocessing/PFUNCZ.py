import spacy
from nltk import word_tokenize
from spellchecker import SpellChecker
from NEW.WordSetz import *
from nltk.sentiment.util import *

spell = SpellChecker()
nlp = spacy.load('en_core_web_md')
rEgEx = re.compile('[^a-z A-Z]')


def remove_special_characters(text):  # only use it after sentence tokinization
    text = rEgEx.sub('', text)
    return text


def Question_sent_detect(text, wh=False, qSign=False):
    Q = False
    if qSign:
        text = str(text)
        if text.endswith("?") or text.endswith("?", len(text) - 2, len(text) - 1):
            Q = True
    elif wh:
        if text[0] in questionWords and nlp(str(text))[1].pos_ == 'VERB':
            Q = True
    return Q


def Negative_sent_detection(text):
    Negetive = False
    text = text.split()
    text = mark_negation(text)
    for i in text:
        if str(i).endswith('_NEG'):
            Negetive = True
    return Negetive


def remove_stopword(sent_wordz):
    for i in sent_wordz:
        if i in (questionWords or stopWordZ):
            sent_wordz.remove(i)
    return sent_wordz


def word_match(word):
    wordset = []
    Candidated = []
    SimilaritY = [0, word]
    # lemmatize
    if word != nlp(word)[0].lemma_:
        wordset.append(nlp(word)[0].lemma_)
    # omit alphabet with more than 2 repeat
    tmp = re.sub(r'(.)\1\1+', r'\1', word)
    if (word != tmp) and (tmp not in wordset):
        wordset.append(tmp)
    if len(wordset) != 0:
        for i in wordset:
            Candidated.append(spell.correction(i))
        w = nlp(word)
        if len(Candidated) != 0:
            for j in Candidated:
                w1 = nlp(j)
                if SimilaritY[0] < w[0].similarity(w1[0]):
                    SimilaritY[0] = w[0].similarity(w1[0])
                    SimilaritY[1] = j
    return SimilaritY


def Neg_detect(sentence):
    # this one can be used inside sentence
    # for detecting negetivity and posetivity of each words
    # currently its not used
    # for using this func gotta make some change in rest of code
    wordzzz = word_tokenize(sentence, 'english')
    wordzzz = mark_negation(wordzzz)
    Negetivity = []
    for i in range(len(wordzzz)):
        if '_NEG' in wordzzz[i]:
            wordzzz[i] = wordzzz[i].replace('_NEG', '')
            Negetivity.append(-1)
        else:
            Negetivity.append(1)
    return wordzzz, Negetivity
