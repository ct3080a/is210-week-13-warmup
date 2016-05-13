#!/usr/env/bin/python
# -*- coding: utf-8 -*-
"""Task 1 docstring."""


import json
import csv


GRADES = {'A': float(1.0),
          'B': float(.90),
          'C': float(.80),
          'D': float(.70),
          'F': float(.60)}


def get_score_summary(filename):
    """Return the average score of a boro.

    Args:
        filename (str): Represents the filename whose data will be read and
                        interpreted.

    Returns:
        filedict (dict): A dictionary, keyed by boro, whose value is a tuple
                         with the number of restauranteurs per boro (who have
                         scores), and the average score for that boro.

    Examples:

        >>> get_score_summary('inspection_results.csv')
        >>> {'BRONX': (156, 0.9762820512820514), 'BROOKLYN':
        (417, 0.9745803357314141), 'STATEN ISLAND': (46, 0.9804347826086955),
        'MANHATTAN': (748, 0.9771390374331531), 'QUEENS':
        (414, 0.9719806763285017)}
    """
    filedata = {}
    fhandler = open(filename, 'r')
    csvfile = csv.reader(fhandler)

    for row in csvfile:
        if row[10] not in ['P', '', 'GRADE']:
            filedata[row[0]] = [row[1], row[10]]
            filedata.update(filedata)
    fhandler.close()

    filegrade = {}
    for value in filedata.itervalues():
        if value[0] not in filegrade.iterkeys():
            count = 1
            total = GRADES[value[1]]
        else:
            count = filegrade[value[0]][0] + 1
            total = filegrade[value[0]][1] + GRADES[value[1]]
        filegrade[value[0]] = (count, total)
        filegrade.update(filegrade)

    filedict = {}
    for key in filegrade.iterkeys():
        count = filegrade[key][0]
        total = filegrade[key][1]/filegrade[key][0]
        filedict[key] = (count, total)
    return filedict


def get_market_density(filename):
    """Count of markets per borough.

    Args:
        filename (str): Name of file.

    Returns:
        datadict (dict): Returns a dictionary of number of green markets per
                         borough.

    Examples:

        >>> get_market_density('green_markets.json')
        {u'STATEN ISLAND': 2, u'BROOKLYN': 48, u'BRONX': 32,
        u'MANHATTAN': 39, u'QUEENS': 16}
    """
    fhandler = open(filename, 'r')
    jfile = json.load(fhandler)
    jdata = jfile['data']
    datadict = {}
    fhandler.close()
    for data in jdata:
        data[8] = data[8].strip()
        if data[8] not in datadict.iterkeys():
            count = 1
        else:
            count = datadict[data[8]] + 1
        datadict[data[8]] = count
        datadict.update(datadict)
    return datadict


def correlate_data(fname='inspection_results.csv',
                   jsonfile='green_markets.json',
                   fileoutput='correlatedfile.json'):
    """Combines two pieces of data.

    Args:
        fname = first file
        jsonfile = seconda file
        fileoutput = combined file

    Returns:
        dictionary = a single dictionary of combined data
    """
    correlatefile = get_score_summary(fname)
    correlatefile2 = get_market_density(jsonfile)
    correlatedict = {}
    for key2 in correlatefile2.iterkeys():
        for key1 in correlatefile.iterkeys():
            if key1 == str(key2).upper():
                value1 = correlatefile[key1][1]
                value2 = float(correlatefile2[key2])/(correlatefile[key1][0])
                correlatedict[key2] = (value1, value2)
                correlatedict.update(correlatedict)
    jsonfile = json.dumps(correlatedict)
    fhandler = open(fileoutput, 'w')
    fhandler.write(jsonfile)
    fhandler.close()
