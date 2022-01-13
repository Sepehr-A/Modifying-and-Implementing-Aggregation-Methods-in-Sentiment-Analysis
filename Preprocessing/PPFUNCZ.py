import datetime
import pandas
import re
import unicodedata
from bs4 import BeautifulSoup
from NEW.contractions import CONTRACTION_MAP


def strip_html_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    stripped_text = soup.get_text()
    return stripped_text


def remove_accented_chars(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text


def expand_contractions(text, contraction_mapping=CONTRACTION_MAP):
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())),
                                      flags=re.IGNORECASE | re.DOTALL)

    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match) \
            if contraction_mapping.get(match) \
            else contraction_mapping.get(match.lower())
        expanded_contraction = first_char + expanded_contraction[1:]
        return expanded_contraction

    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text


def normalizer(dataset, reviewNum=0, possibleMaxReviews=True, wantExcel=False):
    Reviewz = list(dataset["Text"])
    Scorez = list(dataset["Rate"])
    ScorezCount = [0, 0, 0, 0, 0]
    for i in Scorez:
        for j in range(5):
            if i == j + 1:
                ScorezCount[j] += 1
                # break
    print(ScorezCount, sum(ScorezCount), len(Scorez), sep='\t')
    minReviewNum = min(ScorezCount)
    if possibleMaxReviews:
        for i in range(5):
            while ScorezCount[i] > minReviewNum:
                ScorezCount[i] -= 1
                indeX = Scorez.index(i + 1)
                del Reviewz[indeX]
                del Scorez[indeX]
    else:
        if reviewNum <= minReviewNum:
            for i in range(5):
                while ScorezCount[i] > reviewNum:
                    ScorezCount[i] -= 1
                    indeX = Scorez.index(i + 1)
                    del Reviewz[indeX]
                    del Scorez[indeX]
        else:
            return "cant create that"
    if wantExcel:
        dataSet = pandas.DataFrame({'Text': Reviewz, 'Rate': Scorez})
        dataSet.to_excel("NormalizedDataSet-{0}.xlsx".format(str(datetime.date.today())))
        return "Done, Check out the Directory"
    else:
        return [Reviewz, Scorez]


def seriesOfFunctions(teXt):
    teXt = strip_html_tags(teXt)
    teXt = remove_accented_chars(teXt)
    teXt = expand_contractions(teXt)
    return teXt.lower()
