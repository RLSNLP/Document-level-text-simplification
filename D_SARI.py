from __future__ import division

from collections import Counter

import sys

import nltk

import math

def ReadInFile(filename):
    with open(filename) as f:
        lines = f.readlines()

        lines = [x.strip() for x in lines]

    return lines

def D_SARIngram(sgrams, cgrams, rgramslist, numref):
    rgramsall = [rgram for rgrams in rgramslist for rgram in rgrams]

    rgramcounter = Counter(rgramsall)

    sgramcounter = Counter(sgrams)

    sgramcounter_rep = Counter()

    for sgram, scount in sgramcounter.items():
        sgramcounter_rep[sgram] = scount * numref

    cgramcounter = Counter(cgrams)

    cgramcounter_rep = Counter()

    for cgram, ccount in cgramcounter.items():
        cgramcounter_rep[cgram] = ccount * numref

    # KEEP

    keepgramcounter_rep = sgramcounter_rep & cgramcounter_rep

    keepgramcountergood_rep = keepgramcounter_rep & rgramcounter

    keepgramcounterall_rep = sgramcounter_rep & rgramcounter

    keeptmpscore1 = 0

    keeptmpscore2 = 0

    for keepgram in keepgramcountergood_rep:
        keeptmpscore1 += keepgramcountergood_rep[keepgram] / keepgramcounter_rep[keepgram]

        keeptmpscore2 += keepgramcountergood_rep[keepgram] / keepgramcounterall_rep[keepgram]

        # print "KEEP", keepgram, keepscore, cgramcounter[keepgram], sgramcounter[keepgram], rgramcounter[keepgram]

    keepscore_precision = 0

    if len(keepgramcounter_rep) > 0:
        keepscore_precision = keeptmpscore1 / len(keepgramcounter_rep)

    keepscore_recall = 0

    if len(keepgramcounterall_rep) > 0:
        keepscore_recall = keeptmpscore2 / len(keepgramcounterall_rep)

    keepscore = 0

    if keepscore_precision > 0 or keepscore_recall > 0:
        keepscore = 2 * keepscore_precision * keepscore_recall / (keepscore_precision + keepscore_recall)

    # DELETION

    delgramcounter_rep = sgramcounter_rep - cgramcounter_rep

    delgramcountergood_rep = delgramcounter_rep - rgramcounter

    delgramcounterall_rep = sgramcounter_rep - rgramcounter

    deltmpscore1 = 0

    deltmpscore2 = 0

    for delgram in delgramcountergood_rep:
        deltmpscore1 += delgramcountergood_rep[delgram] / delgramcounter_rep[delgram]

        deltmpscore2 += delgramcountergood_rep[delgram] / delgramcounterall_rep[delgram]

    delscore_precision = 0

    if len(delgramcounter_rep) > 0:
        delscore_precision = deltmpscore1 / len(delgramcounter_rep)

    delscore_recall = 0

    if len(delgramcounterall_rep) > 0:
        delscore_recall = deltmpscore1 / len(delgramcounterall_rep)

    delscore = 0

    if delscore_precision > 0 or delscore_recall > 0:
        delscore = 2 * delscore_precision * delscore_recall / (delscore_precision + delscore_recall)

    # ADDITION

    addgramcounter = set(cgramcounter) - set(sgramcounter)

    addgramcountergood = set(addgramcounter) & set(rgramcounter)

    addgramcounterall = set(rgramcounter) - set(sgramcounter)

    addtmpscore = 0

    for addgram in addgramcountergood:
        addtmpscore += 1

    addscore_precision = 0

    addscore_recall = 0

    if len(addgramcounter) > 0:
        addscore_precision = addtmpscore / len(addgramcounter)

    if len(addgramcounterall) > 0:
        addscore_recall = addtmpscore / len(addgramcounterall)

    addscore = 0

    if addscore_precision > 0 or addscore_recall > 0:
        addscore = 2 * addscore_precision * addscore_recall / (addscore_precision + addscore_recall)

    return (keepscore, delscore_precision, addscore)

def count_length(ssent, csent, rsents):

    input_length = len(ssent.split(" "))

    output_length = len(csent.split(" "))

    reference_length = 0

    for rsent in rsents:

        reference_length += len(rsent.split(" "))

    reference_length = int(reference_length / len(rsents))

    return input_length, reference_length, output_length

def sentence_number(csent, rsents):

    output_sentence_number = len(nltk.sent_tokenize(csent))

    reference_sentence_number = 0

    for rsent in rsents:

        reference_sentence_number += len(nltk.sent_tokenize(rsent))

    reference_sentence_number = int(reference_sentence_number / len(rsents))

    return reference_sentence_number, output_sentence_number

def D_SARIsent(ssent, csent, rsents):
    numref = len(rsents)

    s1grams = ssent.lower().split(" ")

    c1grams = csent.lower().split(" ")

    s2grams = []

    c2grams = []

    s3grams = []

    c3grams = []

    s4grams = []

    c4grams = []

    r1gramslist = []

    r2gramslist = []

    r3gramslist = []

    r4gramslist = []

    for rsent in rsents:

        r1grams = rsent.lower().split(" ")

        r2grams = []

        r3grams = []

        r4grams = []

        r1gramslist.append(r1grams)

        for i in range(0, len(r1grams) - 1):

            if i < len(r1grams) - 1:
                r2gram = r1grams[i] + " " + r1grams[i + 1]

                r2grams.append(r2gram)

            if i < len(r1grams) - 2:
                r3gram = r1grams[i] + " " + r1grams[i + 1] + " " + r1grams[i + 2]

                r3grams.append(r3gram)

            if i < len(r1grams) - 3:
                r4gram = r1grams[i] + " " + r1grams[i + 1] + " " + r1grams[i + 2] + " " + r1grams[i + 3]

                r4grams.append(r4gram)

        r2gramslist.append(r2grams)

        r3gramslist.append(r3grams)

        r4gramslist.append(r4grams)

    for i in range(0, len(s1grams) - 1):

        if i < len(s1grams) - 1:
            s2gram = s1grams[i] + " " + s1grams[i + 1]

            s2grams.append(s2gram)

        if i < len(s1grams) - 2:
            s3gram = s1grams[i] + " " + s1grams[i + 1] + " " + s1grams[i + 2]

            s3grams.append(s3gram)

        if i < len(s1grams) - 3:
            s4gram = s1grams[i] + " " + s1grams[i + 1] + " " + s1grams[i + 2] + " " + s1grams[i + 3]

            s4grams.append(s4gram)

    for i in range(0, len(c1grams) - 1):

        if i < len(c1grams) - 1:
            c2gram = c1grams[i] + " " + c1grams[i + 1]

            c2grams.append(c2gram)

        if i < len(c1grams) - 2:
            c3gram = c1grams[i] + " " + c1grams[i + 1] + " " + c1grams[i + 2]

            c3grams.append(c3gram)

        if i < len(c1grams) - 3:
            c4gram = c1grams[i] + " " + c1grams[i + 1] + " " + c1grams[i + 2] + " " + c1grams[i + 3]

            c4grams.append(c4gram)

    (keep1score, del1score, add1score) = D_SARIngram(s1grams, c1grams, r1gramslist, numref)

    (keep2score, del2score, add2score) = D_SARIngram(s2grams, c2grams, r2gramslist, numref)

    (keep3score, del3score, add3score) = D_SARIngram(s3grams, c3grams, r3gramslist, numref)

    (keep4score, del4score, add4score) = D_SARIngram(s4grams, c4grams, r4gramslist, numref)

    avgkeepscore = sum([keep1score, keep2score, keep3score, keep4score]) / 4

    avgdelscore = sum([del1score, del2score, del3score, del4score]) / 4

    avgaddscore = sum([add1score, add2score, add3score, add4score]) / 4

    input_length, reference_length, output_length = count_length(ssent, csent, rsents)

    reference_sentence_number, output_sentence_number = sentence_number(csent, rsents)
    
    if output_length >= reference_length:

        LP_1 = 1

    else:

        LP_1 = math.exp((output_length - reference_length) / output_length)

    if output_length > reference_length:

        LP_2 = math.exp((reference_length - output_length) / max(input_length - reference_length, 1))

    else:

        LP_2 = 1

    SLP = math.exp(-abs(reference_sentence_number - output_sentence_number) / max(reference_sentence_number,
                                                                                  output_sentence_number))

    avgkeepscore = avgkeepscore * LP_2 * SLP

    avgaddscore = avgaddscore * LP_1

    avgdelscore = avgdelscore * LP_2

    finalscore = (avgkeepscore + avgdelscore + avgaddscore) / 3

    return finalscore, avgkeepscore, avgdelscore, avgaddscore

def main():

    ssent = "marengo is a town in and the county seat of iowa county , iowa , united states . it has served as the county seat since august 1845 , even though it was not incorporated until july 1859 . the population was 2,528 in the 2010 census , a decline from 2,535 in 2000 ."

    csent1 = "in the US . 2,528 in 2010 ."
    csent2 = "marengo is a city in iowa , the US . it has served as the county seat since august 1845 , even though it was not incorporated . the population was 2,528 in the 2010 census , a decline from 2,535 in 2010 ."
    csent3 = "marengo is a town in iowa . marengo is a town in the US . in the US . the population was 2,528 . the population in the 2010 census ."
    csent4 = "marengo is a town in iowa , united states . in 2010 , the population was 2,528 ."
    rsents = ["marengo is a city in iowa in the US . the population was 2,528 in 2010 ."]
    
    print(D_SARIsent(ssent, csent1, rsents))
    print(D_SARIsent(ssent, csent2, rsents))
    print(D_SARIsent(ssent, csent3, rsents))
    print(D_SARIsent(ssent, csent4, rsents))
    
if __name__ == '__main__':
    main()
