import csv 
import typing
from typing import List, Tuple
import sys
# person is a dict {conc1, conc2, house, academic year}
# data has the same fields, but also has a 'name' field

def match(person1: dict, person2: dict):
    ''' true iff fields match '''
    # doesn't just check person1 == person2 bc person2 has a name field
    matched = person1['Concentration 1'] == person2['Concentration 1'] \
                and person1['Concentration 2'] == person2['Concentration 2'] \
                and person1['House'] == person2['House'] \
                and person1['Year'] == person2['Year']
    return matched


def identifyIndividual(person: dict, data):
    # returns a list of the names of the people who match the person
    # if no one matches, returns an empty list
    matches = [(p['Name'], p['Email']) for p in data if match(person, p)]
    return matches


def uniqueMatches(matches: List[Tuple], k: int=1) -> List[Tuple]:
    # returns a list of the names of the people who match 0 < x <= k person, and the row they match
    # if no one matches, returns an empty list
    uniqueMatches = []
    for match in matches:
        if len(match[1]) <= k and len(match[1]) > 0:
            uniqueMatches.append((match[0], match[1][0][0], match[1][0][1]))
    return uniqueMatches


def main():
    if len(sys.argv) != 3:
        print('Usage: python3 identifier.py facebookFile surveyFile')
        exit()
    facebookFile = sys.argv[1]
    surveyFile = sys.argv[2]
    # read in the data
    f = open(facebookFile, 'r', encoding='utf-8-sig')
    facebookData = list(csv.DictReader(f))
    s = open(surveyFile, 'r', encoding='utf-8-sig')
    surveyData = list(csv.DictReader(s))
    # identify people
    # list of tuples, (personData, [names])
    matches = []
    for person in surveyData:
        matches.append((person, identifyIndividual(person, facebookData)))
    # find unique matches
    unique = uniqueMatches(matches, 1)
    # print out the results
    print(f'Found {len(unique)} unique matches')
    print(f'Out of {len(surveyData)} responses')
    for match in unique:
        print(f'{match[1]}, {match[2]}')
    f.close()
    s.close()

if __name__ == '__main__':
    main()