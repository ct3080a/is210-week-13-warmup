#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Grading restaurants in the boroughs."""

import json
import csv


GSCALE = {'A': float(1.00),
          'B': float(.90),
          'C': float(.80),
          'D': float(.70),
          'F': float(.60)}


def get_score_summary(fname):
    """Loop through file to obtain grades.

    Args:
        fname (string): Filename to be read and interpreted.

    Returns:
        dict: Restaurants per borough with sum of scores.

    Examples:
        >>> get_score_summary('inspection_results.csv')
        {'BRONX': (156, 0.9762820512820514),
        'BROOKLYN': (417, 0.9745803357314141),
        'STATEN ISLAND': (46, 0.9804347826086955),
        'MANHATTAN': (748, 0.9771390374331531),
        'QUEENS': (414, 0.9719806763285017)}
    """
    gradedata = {}
    fhandler = open(fname, 'r')
    rest_data = csv.reader(fhandler)
    for row in rest_data:
        if row[10] not in ['P', '', 'GRADE']:
            gradedata[row[0]] = [row[1], row[10]]
            gradedata.update(gradedata)
    fhandler.close()

    gradereview = {}
    for value in gradedata.itervalues():
        if value[0] not in gradereview.iterkeys():
            count1 = 1
            count2 = GSCALE[value[1]]
        else:
            count1 = gradereview[value[0]][0] + 1
            count2 = gradereview[value[0]][1] + GSCALE[value[1]]
        gradereview[value[0]] = (count1, count2)
        gradereview.update(gradereview)
    graderesults = {}
    for key in gradereview.iterkeys():
        count1 = gradereview[key][0]
        count2 = gradereview[key][1]/gradereview[key][0]
        graderesults[key] = (count1, count2)
    return graderesults


def get_market_density(fname):
    """Count markets per borough.

    Args:
        fname (string): Filename to be read.

    Return:
        dict: Count of markets per borough as dictionary.

    Examples:
        >>> get_market_density('green_markets.json')
        {u'Bronx': 32, u'Brooklyn': 48, u'Staten Island': 2,
        u'Manhattan': 39, u'Queens': 16}
    """
    fhandler = open(fname, 'r')
    jdata = json.load(fhandler)
    datasum = jdata['data']
    datareturn = {}
    fhandler.close()
    for data in datasum:
        data[8] = data[8].strip()
        if data[8] not in datareturn.iterkeys():
            count1 = 1
        else:
            count1 = datareturn[data[8]] + 1
        datareturn[data[8]] = count1
        datareturn.update(datareturn)
    return datareturn


def correlate_data(fname1='inspection_results.csv',
                   fname2='green_markets.json',
                   fname3='dataresults.csv'):
    """Combine score summary and market density.

    Args:
        fname1 (str): Filename of scores data. Default = inspection_results.csv
        fname2 (str): Filename of market data. Default = green_markets.json
        fname3 (str): Build results file. Default = dataresults.csv

    Returns:
        dict: Combined dictionary keyed by borough.
    """
    correlate1 = get_score_summary(fname1)
    correlate2 = get_market_density(fname2)
    datareturn = {}
    for key2 in correlate2.iterkeys():
        for key1 in correlate1.iterkeys():
            if key1 == str(key2).upper():
                keyval1 = correlate1[key1][1]
                keyval2 = float(correlate2[key2])/(correlate1[key1][0])
                datareturn[key2] = (keyval1, keyval2)
                datareturn.update(datareturn)
    jsondata = json.dumps(datareturn)
    fhandler = open(fname3, 'w')
    fhandler.write(jsondata)
    fhandler.close()
