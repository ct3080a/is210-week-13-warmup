#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Rating the Buroughs"""


import csv
import json

GRADES = {
    'A': float(1.00),
    'B': float(0.90),
    'C': float(0.80),
    'D': float(0.70),
    'F': float(0.60),
}


def get_score_summary(filename):
    """Looks through data and returns a dict

    Arguments:
        filename(file): a comma seperated value(csv) file.

    Returns:
        a dict

    Examples:
        >>> get_score_summary('inspection_results.csv')
        {'BRONX': (156, 0.9762820512820514),
        'BROOKLYN': (417, 0.9745803357314141),
        'STATEN ISLAND': (46, 0.9804347826086955),
        'MANHATTAN': (748, 0.9771390374331531),
        'QUEENS': (414, 0.9719806763285017)}
    """
    data = {}
    fhandler = open(filename, 'r')
    csv_f = csv.reader(fhandler)

    for row in csv_f:
        if row[10] not in ['P', '', 'GRADE']:
            data[row[0]] = [row[1], row[10]]
            data.update(data)
    fhandler.close()

    summary = {}
    for value in data.itervalues(): #.itervalues/iterkeys has been replaced by
        if value[0] not in summary.iterkeys(): # values/keys, but will not pass
            value1 = 1              # runtests.sh with the new values
            value2 = GRADES[value[1]]
        else:
            value1 = summary[value[0]][0] + 1
            value2 = summary[value[0]][1] + GRADES[value[1]]
        summary[value[0]] = (value1, value2)
        summary.update(summary)

    result = {}
    for key in summary.iterkeys():
        value1 = summary[key][0]
        value2 = summary[key][1]/summary[key][0]
        result[key] = (value1, value2)
    return result


def get_market_density(filename):
    """Opens a file and then returns a dict.

    Arguments:
        filename(file): a file

    Return:
        A dictionary

    Examples:
        >>>get_market_density('green_markets.json')
        {u'Staten Island': 2,
        u'Brooklyn': 48, u'Bronx': 32,
        u'Manhattan': 39,
        u'Queens': 16}
    """

    fhandler = open(filename, 'r')
    all_data = json.load(fhandler)
    summary = all_data["data"]
    result = {}
    fhandler.close()
    for data in summary:
        data[8] = data[8].strip()
        if data[8] not in result.iterkeys():
            val = 1
        else:
            val = result[data[8]] + 1
        result[data[8]] = val
        result.update(result)
    return result


def correlate_data(doc1='inspection_results.csv',
                   doc2='green_markets.json',
                   doc3='result.json'):
    """Correlating the data into one file.

        Arguments:
            doc1(file): a file that defaults to the file inspection_results.csv
            doc2(file): a file that defaults to the file green_markets.json
            doc3(file): a file that defaults to the file result.json

        Returns: A fourth file with new data

        Example:
            {'BRONX': (0.9762820512820514, 0.1987179487179487)}
    """
    average_score = get_score_summary(doc1)
    average_data = get_market_density(doc2)
    out = {}
    for key2 in average_data.iterkeys():
        for key1 in average_score.iterkeys():
            if key1 == str(key2).upper():
                value1 = average_score[key1][1]
                value2 = float(average_data[key2])/(average_score[key1][0])
                out[key2] = (value1, value2)
                out.update(out)
    jdata = json.dumps(out)
    fhandler = open(doc3, 'w')
    fhandler.write(jdata)
    fhandler.close()
