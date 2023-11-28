import csv 
from matplotlib import pyplot as plt
import numpy as np


quasis  = ['cc_by_ip','city','postalCode','LoE','YoB','gender','nforum_posts','nforum_votes','nforum_endorsed','nforum_threads','nforum_comments','nforum_pinned','nforum_events']
fieldnames  = ['course_id', 'user_id', 'cc_by_ip','city','postalCode','LoE','YoB','gender','nforum_posts','nforum_votes','nforum_endorsed','nforum_threads','nforum_comments','nforum_pinned','nforum_events']


def hasKMatches(data, row, k):
    ''' true iff there are >= k rows in data that match quasis'''
    matches = 0
    for r in data:
        matches += 0 if any([r[quasi] != row[quasi] for quasi in set.intersection(set(quasis), set(r.keys()))]) else 1
        if matches >= k:
            return True
    return False


def matches(data, row):
    '''return the rows that match quasis'''
    matches = []
    quasiSet = set.intersection(set(quasis), set(data[0].keys()))
    for r in data:
        count = 0
        for quasi in quasiSet:
            if r[quasi] != row[quasi]:
                break
            count += 1
        if count == len(quasiSet):
            matches.append(r)
    return matches


def isKAnonymous(data, k):
    ''' true iff each row in data has at least k matches'''
    for row in data:
        if not hasKMatches(data, row, k):
            return False
    return True


def percentUnique(data, column):
    '''return the percent of unique values in a column'''
    unique = set()
    for row in data:
        unique.add(row[column])
    return len(unique) / len(data)


def kAnonRemoveRows(data, k):
    '''make k-anonymous by removing rows that do not fit k-anonymity'''
    newData = []
    # poor time complexity, checking each thing multiple times, but we 
    for i, row in enumerate(data):
        if row in newData:
            continue
        allMatches = matches(data, row)
        if len(allMatches) >= k:
            for r in allMatches:
                newData.append(r) 
        for r in allMatches:
                data.remove(r)
        print(i / len(data))
    print(len(newData) / len(data))
    return newData


def kAnonGeneralize(data):
    '''make k-anonymous by generalizing rows that are rather continuous, or can easily be binned'''
    for row in data:
        # bin years 
        if row['YoB'] != '':
            row['YoB'] = str(int(row['YoB']) // 10 * 10) + '-' + str(int(row['YoB']) // 10 * 10 + 10)
        # bin nforum_posts to 5s
        if row['nforum_posts'] != '':
            row['nforum_posts'] = str(int(row['nforum_posts']) // 5 * 5) + '-' + str(int(row['nforum_posts']) // 5 * 5 + 5)
        # bin nforum_votes to 5s
        if row['nforum_votes'] != '':
            row['nforum_votes'] = str(int(row['nforum_votes']) // 5 * 5) + '-' + str(int(row['nforum_votes']) // 5 * 5 + 5)
        # bin nforum_endorsed to 5s
        if row['nforum_endorsed'] != '':
            row['nforum_endorsed'] = str(int(row['nforum_endorsed']) // 5 * 5) + '-' + str(int(row['nforum_endorsed']) // 5 * 5 + 5)
        # bin nforum_threads to 5s
        if row['nforum_threads'] != '':
            row['nforum_threads'] = str(int(row['nforum_threads']) // 5 * 5) + '-' + str(int(row['nforum_threads']) // 5 * 5 + 5)
        # bin nforum_comments to 5s
        if row['nforum_comments'] != '':
            row['nforum_comments'] = str(int(row['nforum_comments']) // 5 * 5) + '-' + str(int(row['nforum_comments']) // 5 * 5 + 5)
        # bin nforum_pinned to 5s
        if row['nforum_pinned'] != '':
            row['nforum_pinned'] = str(int(row['nforum_pinned']) // 5 * 5) + '-' + str(int(row['nforum_pinned']) // 5 * 5 + 5)
        # bin nforum_events to 5s
        if row['nforum_events'] != '':
            row['nforum_events'] = str(int(row['nforum_events']) // 5 * 5) + '-' + str(int(row['nforum_events']) // 5 * 5 + 5) 
        # remove city and postalCode to generalize location to country code 
        del row['city']
        del row['postalCode']
    return data


def kAnonRemoveColumns(data, k):
    '''make k-anonymous by removing columns that are too specific'''
    while not isKAnonymous(data, k):
        # remove the column with the highest percent unique
        maxUnique = 0
        maxColumn = ''
        for column in data[0].keys():
            if percentUnique(data, column) > maxUnique:
                maxUnique = percentUnique(data, column)
                maxColumn = column
        for row in data:
            del row[maxColumn]
        print(len(data[0].keys()))
    return data


def numValidRows(data):
    '''return the number of rows with valid data'''
    count = 0
    for row in data:
        if any([row[quasi] != '' for quasi in quasis]):
            count += 1
    return count


def graphNumRows():
    '''graph the number of rows in each dataset'''
    # unadulterated data
    file = open('reduced_qi_filled.csv', 'r')
    data = list(csv.DictReader(file))
    file.close()
    file = open('removed_rows.csv', 'r')
    removedRows = list(csv.DictReader(file))
    file.close()
    file = open('removed_columns.csv', 'r')
    removedColumns = list(csv.DictReader(file))
    file.close()
    file = open('generalized_columns.csv', 'r')
    generalizedColumns = list(csv.DictReader(file))
    file.close()
    plt.bar([1, 2, 3, 4],[numValidRows(data), numValidRows(removedRows), numValidRows(removedColumns), numValidRows(generalizedColumns)])
    plt.ylabel('Number of Rows')
    plt.xlabel('Dataset')
    plt.title('Number of Rows Remaining After Anonymization')
    plt.xticks([1, 2, 3, 4], ['OriginalData', 'Removed Rows', 'Removed Columns', 'Generalized Columns'])
    plt.show()


def graphDiffKByRow(data):
    # takes advantage of the fact that if data isn't k-anonymous, then data isn't k+1 anonymous
    numRows = []
    for k in [2, 3, 4]:
        data = kAnonRemoveRows(data, k)
        numRows.append(len(data))
    plt.plot([2, 3, 4], numRows)
    plt.title('Number of Rows vs k')
    plt.ylabel('Number of Rows')
    plt.xlabel('k')
    plt.xticks([2, 3, 4])
    plt.show()


def driver():
    with open('reduced_qi_filled.csv', 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)
        generalized = kAnonGeneralize(data)
        # save as csv
        if not isKAnonymous(generalized, 5):
            generalized = []
        with open('generalized_columns.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(generalized)


def distOfRowRemovedData():
    ''' graph of difference of mean of each column between original data and removed row data '''
    f = open('reduced_qi_filled.csv', 'r')
    data = list(csv.DictReader(f))
    f.close()
    f = open('removed_rows.csv', 'r')
    removedRows = list(csv.DictReader(f))
    f.close()
    # get mean of each column
    means = {}
    count = 0
    colsToGather = ['YoB', 'nforum_posts', 'nforum_votes', 'nforum_endorsed', 'nforum_threads', 'nforum_comments', 'nforum_pinned', 'nforum_events']
    for column in colsToGather:
        means[column] = 0
    YoBCount = 0
    for row in data:
        for column in colsToGather:
            if row[column].isnumeric():
                means[column] += int(row[column])
                count += (1/7)
                if column == 'YoB':
                    YoBCount += 1
                else:
                    count += (1/7)
    for column in colsToGather:
        if column == 'YoB':
            means[column] = means[column] / YoBCount
        else:
            means[column] /= count
    count = 0
    YoBCount = 0
    removedMeans = {}
    for column in colsToGather:
        removedMeans[column] = 0
    for row in removedRows:
        for column in colsToGather:
            if row[column].isnumeric():
                removedMeans[column] += int(row[column])
                if column == 'YoB':
                    YoBCount += 1
                else:
                    count += (1/7)
    for column in colsToGather:
        if column == 'YoB':
            removedMeans[column] /= YoBCount
        else:
            removedMeans[column] /= count
    # don't graph, but print these stats in a table rounded to 5 decimal places
    print('mean')
    print('column, original, removed')
    for column in colsToGather:
        print(column, round(means[column], 5), round(removedMeans[column], 5))



if __name__ == '__main__':
    with open ('reduced_qi_filled.csv', 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)
        print(len(data))
    with open('generalizedAndRemoved.csv', 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)
        print(len(data))
    