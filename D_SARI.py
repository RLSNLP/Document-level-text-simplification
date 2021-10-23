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
