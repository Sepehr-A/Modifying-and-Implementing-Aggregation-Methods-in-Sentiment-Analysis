import math
import operator
from functools import reduce

# MembershipFuncz or linguistic labels
Poor = [0, 0, 0.050, 0.150]
Slight = [0.050, 0.150, 0.250, 0.350]
Moderate = [0.250, 0.350, 0.650, 0.750]
Very = [0.650, 0.750, 0.850, 0.950]
Most = [0.850, 0.950, 1, 1]
G = [Poor, Slight, Moderate, Very, Most]


def DempsterShefer(ScoreArray, a, b, c=1, d=5):
    mTotal = 0
    indexCheck = True
    for score in ScoreArray:
        # change scale to [0-1]
        mScore = ((score - a) / (b - a))
        if mScore == 0:
            mScore = 0.001
        if ScoreArray.index(score) == 0 and indexCheck:
            mTotal = mScore
            indexCheck = False
        elif ((1 - mTotal) * mScore + ((1 - mScore) * mTotal)) != 1:
            mTotal = (mTotal * mScore) / (1 - ((1 - mTotal) * mScore + ((1 - mScore) * mTotal)))
        else:
            mTotal = 0

    finalScore = (mTotal * (d - c)) + c
    if finalScore < 3:
        finalScore = math.floor(finalScore)
    else:
        finalScore = math.ceil(finalScore)
    if finalScore == 0:
        finalScore = 1
    elif finalScore == 6:
        finalScore = 5
    return finalScore


def sumOfMax(ScoreArray, a, b, c=1, d=5):
    minimum = min(ScoreArray)
    maximum = max(ScoreArray)
    # change scale to 0-1
    minimum = ((minimum - a) / (b - a))
    maximum = ((maximum - a) / (b - a))
    finalScore = maximum - minimum
    finalScore = (((finalScore - a) / (b - a)) * (d - c)) + c
    return finalScore


def maxOfScore(ScoreArray, a, b, c=1, d=5):
    minimum = min(ScoreArray)
    maximum = max(ScoreArray)
    # changing scale to -5,5
    minimum = (((minimum - a) / (b - a)) * 10) - 5
    maximum = (((maximum - a) / (b - a)) * 10) - 5
    if abs(maximum) > abs(minimum):
        finalScore = maximum
    elif abs(maximum) < abs(minimum):
        finalScore = minimum
    else:
        finalScore = maximum
    # returning scale to 1-5
    finalScore = (((finalScore + 5) / 10) * (d - c)) + c
    return finalScore


def CrossRatio(ScoreArray, e, a, b, c=1, d=5):
    # change scale to [0,1]
    ScoreAray = list(map(lambda t: (t - a) / (b - a), ScoreArray))
    if (0 in ScoreAray) and (1 in ScoreAray):
        return 1
    elif len(ScoreAray) == 1:
        # change scale to [c,d]
        return (ScoreAray[0] * (d - c)) + c
    else:
        multipleOfList = reduce((lambda i, j: i * j), ScoreAray)
        minusOne = reduce((lambda k, l: k * l), list(map(lambda x: 1 - x, ScoreAray)))
        Numerator = ((1 - e) ** (len(ScoreAray) - 1)) * multipleOfList
        Denominator = Numerator + ((e ** (len(ScoreAray) - 1)) * minusOne)
        if Denominator == 0:
            kasr = 1
        else:
            kasr = Numerator / Denominator
        return (kasr * (d - c)) + c


def Q(r, a, b):
    if r < a or r == 0:
        return 0
    elif r > b or r == 1:
        return 1
    elif a <= r:
        if r <= b:
            return (r - a) / (b - a)


def OWA(ScoreArray, a, b, c=1, d=5):
    n = len(ScoreArray)
    ScoreArray = list(map(lambda t: (t - a) / (b - a), ScoreArray))
    SortedScoreArray = sorted(ScoreArray, reverse=True)
    owa1 = 0
    owa2 = 0
    owa3 = 0
    for i in range(1, n + 1):
        owa1 += (Q(i / n, 0, 0.5) - Q((i - 1) / n, 0, 0.5)) * SortedScoreArray[i - 1]
        owa2 += (Q(i / n, 0.3, 0.8) - Q((i - 1) / n, 0.3, 0.8)) * SortedScoreArray[i - 1]
        owa3 += (Q(i / n, 0.5, 1) - Q((i - 1) / n, 0.5, 1)) * SortedScoreArray[i - 1]
    finalOWA = [owa1, owa2, owa3]
    return ((sum(finalOWA) / 3) * (d - c)) + c


def QI(r):
    if r <= 0.4:
        return 0
    elif r >= 0.9:
        return 1
    elif 0.4 < r:
        if r < 0.9:
            return (2 * r) - 0.8


def IOWA(ScoreArray, a, b, c=1, d=5, tolerance=0.4):
    n = len(ScoreArray)
    ScoreArray = list(map(lambda t: (t - a) / (b - a), ScoreArray))
    supp_list = [[0 for x in range(n)] for y in range(n)]
    u_l = [0 for x in range(n)]
    Q_sum = 0
    w_l = [0 for x in range(n)]
    iowa = 0
    for l in range(0, n):
        for h in range(0, n):
            supp_list[l][h] = abs(ScoreArray[l] - ScoreArray[h])
    mux = max(max(x) if isinstance(x, list) else x for x in supp_list)
    for l in range(0, n):
        for h in range(0, n):
            if mux != 0:
                supp_list[l][h] = (supp_list[l][h]) / mux
            else:
                supp_list[l][h] = tolerance - 0.1
            if supp_list[l][h] < tolerance:
                supp_list[l][h] = 1
            else:
                supp_list[l][h] = 0
            u_l[l] = u_l[l] + supp_list[l][h]
    U_l = sorted(u_l)
    for l in range(0, n):
        Q_sum = Q_sum + QI(U_l[l] / n)
    for l in range(0, n):
        if Q_sum != 0:
            w_l[l] = (QI(U_l[l] / n)) / Q_sum
        # else:   ????????????????????????
    iowa_list = list(zip(u_l, ScoreArray))
    iowa_list = sorted(iowa_list, key=operator.itemgetter(0))
    score = list(zip(*iowa_list))[1]
    for i in range(0, n):
        iowa = iowa + (w_l[i] * score[i])
    return (iowa * (d - c)) + c


def MU(x, MF):
    # MF is abbr for MembershipFuncz
    a, b, c, d = MF
    if x <= a:
        return 0
    elif a < x < b:
        return (x - a) / (b - a)
    elif b <= x <= c:
        return 1
    elif c < x < d:
        return (d - x) / (d - c)
    elif d <= x:
        return 0


def OWA_new(ScoreArray, a, b, c=1, d=5):
    Scorez = list(map(lambda t: (t - a) / (b - a), ScoreArray))
    minScore = max(Scorez)
    choosenMF, tmp = 0, 0
    Weiights = []
    OWAScore = 0
    for i in range(5):
        t = MU(minScore, G[i])
        if t >= tmp:
            tmp = t
            choosenMF = i
    Scorez = sorted(Scorez)
    for i in Scorez:
        Weiights.append(MU(i, G[choosenMF]))
    r = zip(Scorez, Weiights)
    # print(Weiights)
    for S, W in r:
        OWAScore += S * W
    OWAScore = OWAScore / len(Scorez)
    return (OWAScore * (d - c)) + c
