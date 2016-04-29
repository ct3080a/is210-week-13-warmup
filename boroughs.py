#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This model creates data as a string and extracts info from it. """

import json
grades = {
	"A" : 1.00,
	"B" : .9000,
	"C" : .8000,
	"D" : .7000,
	"F" : .6000,
}

filepath = "inspection_results.csv"

def get_score_summary(filepath):
    """This function returns restaurant inspectction data.
    Args:
        filename (str): The data that will be read and interpreted

    Returns:
        (mixed): a dictionary

    Examples:
        >>> get_score_summary('inspection_results.csv')
        >>> {'BRONX': (156, 0.9762820512820514), 'BROOKLYN':
        (417, 0.9745803357314141), 'STATEN ISLAND': (46, 0.9804347826086955),
        'MANHATTAN': (748, 0.9771390374331531), 'QUEENS':
        (414, 0.9719806763285017)}
    """
    fhandler = open(filepath, 'r')
    f_list = fhandler.readlines()
    d = {}
    for line in f_list[1:]: 
        part1 = line.split(',')
        if part1[10] in grades:
            d[part1[0]] = {"GRADE":part1[10], "BORO":part1[1]}
                     
    fhandler.close()
    r_count_and_score = {
        "QUEENS": {'num_restaurants':0, 'total_score': 0},
        "BROOKLYN": {'num_restaurants':0, 'total_score': 0},
        "MANHATTAN": {'num_restaurants':0, 'total_score': 0},
        "STATEN ISLAND": {'num_restaurants':0, 'total_score': 0},
        "BRONX": {'num_restaurants':0, 'total_score': 0},
    }
    for key in d.iterkeys():
        boro = d[key]['BORO']
        r_count_and_score[boro]['num_restaurants'] +=1
        grade = d[key]['GRADE']
        r_count_and_score[boro]['total_score'] += grades[grade]
    res_info = {}
    for key in r_count_and_score.iterkeys():
        avg = r_count_and_score[key]['total_score'] / \
                 r_count_and_score[key]['num_restaurants']
        res_info[key] = (r_count_and_score[key]['num_restaurants'], avg)
        return res_info

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
    data = market_info['data']
    
    market_count = {
         "QUEENS": 0,
         "BROOKLYN": 0,
         "MANHATTAN": 0,
         "STATEN ISLAND": 0,
         "BRONX": 0
         }
    for l in data:
         market_count[l[8].upper().strip()] += 1
              
    fhandler.close()

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
        >>>>>> correlate_data('inspection_results.csv', 'green_markets.json'
            , 'data_output')
            {"BRONX": [0.9762820512820514, 0.20512820512820512]}
    """
    market_density = get_market_density(market_file)
    score_summary = get_score_summary(res_file)
    new_market = {}
    for key in market_density.iterkeys():
         for key1 in score_summary.iterkeys():
              if key1 ==str(key).upper():
                   val1 = score_summary[key1][1]
                   val2 = float(market_density[key]) / (score_summary[key1][0])
                   new_market[key] = (val1, val2)
                   new_market.update(new_market)                 
    finaldata = json.dumps(new_market)
    fhandler = open(data_output, 'w')
    fhandler.write(finaldata)
    fhandler.close
