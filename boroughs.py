#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This model creates data as a string and extracts info from it. """

import json
import csv
GRADES = {
    'A': float(1),
    'B': float(.9),
    'C': float(.8),
    'D': float(.7),
    'F': float(.6),
}


def get_score_summary(filepath):
    """This function returns restaurant inspectction data.
    Args:
        filename (str): The data that will be read and interpreted

    Returns:
        (mixed): a dictionary

    Examples:
        >>> get_score_summary('inspection_results.csv')
        {'BRONX': (156, 0.9762820512820514),
        'BROOKLYN': (417, 0.9745803357314141),
        'STATEN ISLAND': (46, 0.9804347826086955),
        'MANHATTAN': (748, 0.9771390374331531),
        'QUEENS': (414, 0.9719806763285017)}
    """
    data = {}
    fhandler = open(filepath, 'r')
    f_list = csv.reader(fhandler)
    for line in f_list:
        if line[10] not in ['P', '', 'GRADE']:
            data[line[0]] = [line[1], line[10]]
            data.update(data)
    fhandler.close()
    res_info = {}
    for value in data.itervalues():
        if value[0] not in res_info.iterkeys():
            total1 = 1
            total2 = GRADES[value[1]]
        else:
            total1 = res_info[value[0]][0] + 1
            total2 = res_info[value[0]][1] + GRADES[value[1]]
        res_info[value[0]] = (total1, total2)
        res_info.update(res_info)
    r_count_and_score = {}
    for key in res_info.iterkeys():
        total1 = res_info[key][0]
        total2 = res_info[key][1]/res_info[key][0]
        r_count_and_score[key] = (total1, total2)
    return r_count_and_score


def get_market_density(filepath):
    """This function gets a count of markets per borough.

    Args:
        filename (str): A file containing data.

    Returns:
        (mixed): A dictionary of the number of green markets per borough.

    Examples:
        >>> get_market_density('green_markets.json')
        {u'STATEN ISLAND': 2, u'BROOKLYN': 48, u'BRONX': 32,
        u'MANHATTAN': 39, u'QUEENS': 16}
    """
    fhandler = open(filepath, 'r')
    market_info = json.load(fhandler)
    market_data = market_info['data']
    market_count = {}
    fhandler.close()
    for info in market_data:
        info[8] = info[8].strip()
        if info[8] not in market_count.iterkeys():
            total1 = 1
        else:
            total1 = market_count[info[8]] + 1
        market_count[info[8]] = total1
        market_count.update(market_count)
    return market_count


def correlate_data(res_file, market_file, data_output):
    """This function correlates data.

    Args:
        file with restaurant scores data(mixed): dictionary
        JSON file with green_market data(mixed): dictionary
        file that will contain the output of this function(mixed); dictionary

    Returns:
        (mixed): A combined dictionary with correlated data

    Examples:
        >>>>>> correlate_data('inspection_results.csv', 'green_markets.json',
               'data_output')
               {"BRONX": [0.9762820512820514, 0.20512820512820512]}
    """
    market_density = get_market_density(market_file)
    score_summary = get_score_summary(res_file)
    new_market = {}
    for key in market_density.iterkeys():
        for key1 in score_summary.iterkeys():
            if key1 == str(key).upper():
                val1 = score_summary[key1][1]
                val2 = float(market_density[key]) / (score_summary[key1][0])
                new_market[key] = (val1, val2)
                new_market.update(new_market)
    finaldata = json.dumps(new_market)
    fhandler = open(data_output, 'w')
    fhandler.write(finaldata)
    fhandler.close()
