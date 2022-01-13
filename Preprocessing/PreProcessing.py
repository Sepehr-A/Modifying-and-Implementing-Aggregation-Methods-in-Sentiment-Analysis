from NEW.PPFUNCZ import *
from progress.bar import ChargingBar

DatasetName = ["CitySearch", "TripAdvisor", 'reviews_Amazon_Instant_Video_5', 'reviews_Musical_Instruments_5']

name = DatasetName[3]

dataSet = pandas.read_excel("Excel/Dataset/" + name + ".xlsx")

# Reviewz = list(dataSet["Text"])
# Scorez = list(dataSet["Rate"])

Normalized = normalizer(dataSet, reviewNum=800, possibleMaxReviews=True)
Reviewz = Normalized[0]
Scorez = Normalized[1]
a = [0, 0, 0, 0, 0]

for i in Scorez:
    for j in range(5):
        if i == j + 1:
            a[j] += 1
            break
print(a)
input()
bar = ChargingBar('Processing', max=2000)
for i in range(len(Reviewz)):
    Reviewz[i] = seriesOfFunctions(Reviewz[i])
    bar.next()

dataSet = pandas.DataFrame({'Text': Reviewz, 'Rate': Scorez})
dataSet.to_excel("Excel/Dataset/{0}(New1).xlsx".format(name))
bar.finish()
