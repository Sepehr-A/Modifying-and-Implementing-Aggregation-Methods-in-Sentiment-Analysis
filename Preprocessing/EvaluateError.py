import xlwt, xlrd, datetime

# Set DataSet & Lexicon Name
DatasetName = "CitySearch.xlsx"
DatasetResultName = "CitySearchResult.xls"
ExelEvaluateResultName = 'CitySearchEvaluateResult'

labeledDataSet = xlrd.open_workbook('Data/DAtaset/' + DatasetName)
estimatedDataSet = xlrd.open_workbook('Data/' + DatasetResultName)

bookN = xlwt.Workbook(encoding="utf-8")
sheetN = bookN.add_sheet("Sheet1")

L = labeledDataSet.sheet_by_index(0)
E = estimatedDataSet.sheet_by_index(0)
labeledScoreColumn = L.col_values(2, 1, L.nrows)

FiveStar = False

# Exel Headers
sheetN.write(0, 1, "Precision")
sheetN.write(0, 2, "Recall")
sheetN.write(0, 3, "F-Measure")
sheetN.write(0, 4, "Accuracy")
sheetN.write(0, 5, "MAE")
sheetN.write(1, 0, "simpleAvg")
sheetN.write(2, 0, "DempsterShefer")
sheetN.write(3, 0, "sumOfMax")
sheetN.write(4, 0, "maxOfScore")
sheetN.write(5, 0, "scaledRate")
sheetN.write(6, 0, "OWA")
sheetN.write(7, 0, "CrossRatio")

for j in range(7):
    estimatedScoreColumn = E.col_values(j, 1, E.nrows)
    p = zip(labeledScoreColumn, estimatedScoreColumn)

    truePositive = [0, 0, 0, 0, 0]
    trueNegative = [0, 0, 0, 0, 0]
    falsePositive = [0, 0, 0, 0, 0]
    falseNegative = [0, 0, 0, 0, 0]

    for (labeledScore, estimatedScore) in p:
        estimatedScore = int(round(estimatedScore))
        for i in range(0, 5):
            classScore = i + 1
            if labeledScore == classScore and estimatedScore == classScore:
                truePositive[i] = truePositive[i] + 1
            if labeledScore != classScore and estimatedScore != classScore:
                trueNegative[i] = trueNegative[i] + 1
            if estimatedScore == classScore and labeledScore != classScore:
                falsePositive[i] = falsePositive[i] + 1
            if estimatedScore != classScore and labeledScore == classScore:
                falseNegative[i] = falseNegative[i] + 1
    if FiveStar:
        precision = [0, 0, 0, 0, 0]
        for i in range(0, 5):
            if truePositive[i] + falsePositive[i] == 0:
                precision[i] = "division by zero"
            else:
                precision[i] = truePositive[i] / (truePositive[i] + falsePositive[i])
        print("Precision", j, sum(precision) / 5)
        sheetN.write(j + 1, 1, sum(precision) / 5)

        recall = [0, 0, 0, 0, 0]
        for i in range(0, 5):
            if (truePositive[i] + falseNegative[i]) != 0:
                recall[i] = truePositive[i] / (truePositive[i] + falseNegative[i])
        sheetN.write(j + 1, 2, sum(recall) / 5)
        print("Recall", j, sum(recall) / 5)

        f_Measure = [0, 0, 0, 0, 0]
        for i in range(0, 5):
            if precision[i] + recall[i] != 0:
                f_Measure[i] = (2 * precision[i] * recall[i]) / (precision[i] + recall[i])
        f_Measure = (2 * (sum(precision) / 5) * (sum(recall) / 5)) / ((sum(precision) / 5) + (sum(recall) / 5))
        print("F-Measure", j, sum(f_Measure) / 5)
        sheetN.write(j + 1, 3, sum(f_Measure) / 5)

        accuracy = [0, 0, 0, 0, 0]
        for i in range(0, 5):
            accuracy[i] = (truePositive[i] + trueNegative[i]) / (
                    truePositive[i] + trueNegative[i] + falsePositive[i] + falseNegative[i])
        print("Accuracy", j, sum(accuracy) / 5)
        sheetN.write(j + 1, 4, sum(accuracy) / 5)

    else:
        # print(sum(trueNegative),sum(truePositive),sum(falseNegative),sum(falsePositive))
        # input()
        v = sum(truePositive) + sum(falsePositive)
        if v == 0:
            v = 1
        precision = sum(truePositive) / v
        sheetN.write(j + 1, 1, precision)
        print("Precision", j, precision)

        v = sum(truePositive) + sum(falseNegative)
        if v == 0:
            v = 1
        recall = sum(truePositive) / v
        print("Recall", j, recall)
        sheetN.write(j + 1, 2, recall)

        if precision + recall == 0:
            recall = 1
        f_Measure = (2 * precision * recall) / (precision + recall)
        print("F-Measure", j, f_Measure)
        sheetN.write(j + 1, 3, f_Measure)

        accuracy = (sum(truePositive) + sum(trueNegative)) / (
                sum(truePositive) + sum(trueNegative) + sum(falseNegative) + sum(falsePositive))
        print("Accuracy", j, accuracy)
        sheetN.write(j + 1, 4, accuracy)
    qw = 0
    for i in range(1, E.nrows - 1):
        qw = abs(labeledScoreColumn[i] - estimatedScoreColumn[i]) + qw
    MAE = qw / (E.nrows - 1)
    sheetN.write(j + 1, 5, MAE)
    print("MAE", j, MAE)
if FiveStar:
    bookN.save('Data/{0}(using sum){1}(FiveStar).xls'.format(ExelEvaluateResultName, str(datetime.date.today())))
else:
    bookN.save('Data/{0}(using sum){1}.xls'.format(ExelEvaluateResultName, str(datetime.date.today())))
