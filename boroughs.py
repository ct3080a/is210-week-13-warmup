#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""almost forgot docstring here"""

import csv
import json

GRADES = {
    'A': float(1.0),
    'B': float(0.9),
    'C': float(0.8),
    'D': float(0.7),
    'F': float(0.6),
}


def get_score_summary(filename):
    """Looks through info; returns a dict
    Arguments:
        filename(file): (csv) file.
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
    info = {}
    fhandler = open(filename, 'r')
    r_csv = csv.reader(fhandler)

    for line in r_csv:
        if line[10] not in ['P', '', 'GRADE']:
            info[line[0]] = [line[1], line[10]]
            info.update(info)
    fhandler.close()

    data = {}
    for value in info.itervalues():
        if value[0] not in data.iterkeys():
            val1 = 1
            val2 = GRADES[value[1]]
        else:
            val1 = data[value[0]][0] + 1
            val2 = data[value[0]][1] + GRADES[value[1]]
        data[value[0]] = (val1, val2)
        data.update(data)

    end = {}
    for item in data.iterkeys():
        val1 = data[item][0]
        val2 = data[item][1]/data[item][0]
        end[item] = (val1, val2)
    return end


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
    my_info = json.load(fhandler)
    data = my_info["info"]
    end = {}
    fhandler.close()
    for info in data:
        info[8] = info[8].strip()
        if info[8] not in end.iterkeys():
            val = 1
        else:
            val = end[info[8]] + 1
        end[info[8]] = val
        end.update(end)
    return end


def correlate_data(doc1='inspection_results.csv',
                   doc2='green_markets.json',
                   doc3='end.json'):
    """Correlating the info into one file.
        Arguments:
            doc1(file): a file that defaults to the file inspection_results.csv
            doc2(file): a file that defaults to the file green_markets.json
            doc3(file): a file that defaults to the file end.json
        Returns: A fourth file with new info
        Example:
            {'BRONX': (0.9762820512820514, 0.1987179487179487)}
    """
    avg_score = get_score_summary(doc1)
    avg_data = get_market_density(doc2)
    out = {}
    for tet in avg_data.iterkeys():
        for tobi in avg_score.iterkeys():
            if tobi == str(tet).upper():
                val1 = avg_score[tobi][1]
                val2 = float(avg_data[tet])/(avg_score[tobi][0])
                out[tet] = (val1, val2)
                out.update(out)
    jdata = json.dumps(out)
    fhandler = open(doc3, 'w')
    fhandler.write(jdata)
    fhandler.close()