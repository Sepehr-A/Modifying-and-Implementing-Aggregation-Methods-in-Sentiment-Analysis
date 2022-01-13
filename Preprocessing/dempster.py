import math
from functools import reduce

Score = [ 1.5, 2, 2]


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

    finalScore = (mTotal * 4) + 1
    if finalScore < 3:
        finalScore = math.floor(finalScore)
    else:
        finalScore = math.ceil(finalScore)
    if finalScore == 0:
        finalScore = 1
    elif finalScore == 6:
        finalScore = 5
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
    # print(finalOWA)
    # print(sum(finalOWA) / 3)
    # input()
    print(finalOWA)
    return sum(finalOWA) / 3
    # return max(owa1,owa2,owa3)


def CrossRatio(ScoreArray, e):
    ScoreArray = list(map(lambda t: (t - 1) / 4, ScoreArray))
    if (0 in ScoreArray) and (1 in ScoreArray):
        return 1
    else:
        multipleOfList = reduce((lambda i, j: i * j), ScoreArray)
        minusOne = reduce((lambda k, l: k * l), list(map(lambda x: 1 - x, ScoreArray)))
        Numerator = ((1 - e) ** (len(ScoreArray) - 1)) * multipleOfList
        Denominator = Numerator + ((e ** (len(ScoreArray) - 1)) * minusOne)
        return ((Numerator / Denominator) * 4) + 1


print(DempsterShefer(Score))
print(OWA(Score))
print(CrossRatio(Score, 0.5))
