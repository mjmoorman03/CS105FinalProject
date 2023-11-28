import csv 
import typing
from typing import List, OrderedDict, Tuple
import sys
# person is a dict {conc1, conc2, house, academic year}
# data has the same fields, but also has a 'name' field

def match(person1: dict, person2: dict):
    ''' true iff fields match '''
    # doesn't just check person1 == person2 bc person2 has a name field
    matched = person1['conc1'] == person2['conc1'] \
                and person1['conc2'] == person2['conc2'] \
                and person1['house'] == person2['house'] \
                and person1['academic year'] == person2['academic year']
    return matched


def identifyIndividual(person: dict, data: List[OrderedDict]):
    # returns a list of the names of the people who match the person
    # if no one matches, returns an empty list
    matches = [p['name'] for p in data if match(person, p)]
    return matches


def uniqueMatches(matches: List[Tuple]) -> List[Tuple]:
    # returns a list of the names of the people who match exactly one person, and the row they match
    # if no one matches, returns an empty list
    uniqueMatches = []
    for match in matches:
        if len(match[1]) == 1:
            uniqueMatches.append((match[0], match[1][0]))
    return uniqueMatches


def main():
    if len(sys.argv) != 3:
        print('Usage: python3 identifier.py facebookFile surveyFile')
        exit()
    facebookFile = sys.argv[1]
    surveyFile = sys.argv[2]
    # read in the data
    f = open(facebookFile, 'r')
    facebookData = list(csv.DictReader(f))
    s = open(surveyFile, 'r')
    surveyData = list(csv.DictReader(s))
    # identify people
    # list of tuples, (personData, [names])
    matches = []
    for person in surveyData:
        matches.append((person, identifyIndividual(person, facebookData)))
    # find unique matches
    unique = uniqueMatches(matches)
    # print out the results
    print(f'Found {len(unique)} unique matches')
    print(f'Out of {len(surveyData)} responses')
    f.close()
    s.close()