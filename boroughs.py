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

#{3453445: {"GRADE":"A","BORO":"QUEENS"}}

def get_score_summary(filepath):
     fhandler = open(filepath, 'r')
     f_list = fhandler.readlines()

     d = {}
     for line in f_list[1:]:
          part1 = line.split(',')
          if part1[10] in grades:
               d[part1[0]] = {"GRADE":part1[10], "BORO":part1[1]}

     #print "d is: ", d
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

     #print r_count_and_score

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
    filepath = green_markets.json
    fhandler = open(filepath, 'r')

    data = json.load(fhandler)
    for value in data.iterkeys():
        a = data[key]["meta"]
        a["description"] = market_count

    return market_count
        

    fhandler.close()
    
##  to return the data as a dictionary
##Loop through the data found in the 'data' and count the number of markets per borough, saving the result as a dictionary.
##Return a dictionary of the number of green markets per borough. 
        

     
     
