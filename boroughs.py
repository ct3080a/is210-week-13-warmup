#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tasks 01 - 03: opening files, reading, writing, json, csv, etc."""


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
    """ takes exactly 1 argument, a string which represents the
    filename whose data will be read and interpreted then loops
    and loops again to remove duplicates and create a dictionary"""

    data = {}
    fhandler = open(filename, 'r')
    csv_f = csv.reader(fhandler)

    for row in csv_f:
        if row[10] not in ['P', '', 'GRADE']:
            data[row[0]] = [row[1], row[10]]
            data.update(data)
    fhandler.close()

    summary = {}
    for value in data.itervalues():
        if value[0] not in summary.iterkeys():
            val1 = 1
            val2 = GRADES[value[1]]
        else:
            val1 = summary[value[0]][0] + 1
            val2 = summary[value[0]][1] + GRADES[value[1]]
        summary[value[0]] = (val1, val2)
        summary.update(summary)

    result = {}
    for key in summary.iterkeys():
        val1 = summary[key][0]
        val2 = summary[key][1]/summary[key][0]
        result[key] = (val1, val2)
    return result


def get_market_density(filename):
    """Loads a file and return a dictionary"""

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


def correlate_data(file1='inspection_results.csv',
                   file2='green_markets.json',
                   file3='result.json'):
    """Combining data together and writing into new file."""

    data1 = get_score_summary(file1)
    data2 = get_market_density(file2)
    result = {}
    for key2 in data2.iterkeys():
        for key1 in data1.iterkeys():
            if key1 == str(key2).upper():
                val1 = data1[key1][1]
                val2 = float(data2[key2])/(data1[key1][0])
                result[key2] = (val1, val2)
                result.update(result)
    jdata = json.dumps(result)
    fhandler = open(file3, 'w')
    fhandler.write(jdata)
    fhandler.close()
