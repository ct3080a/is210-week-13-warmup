#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This model creates data as a string and extracts info from it. """

grades = {
	"A" : 100.00,
	"B" : 90.00,
	"C" : 80.00,
	"D" : 70.00,
	"F" : 60.00,
}

filepath = "inspection_results.csv"
fhandler = open(filepath, 'r')
f_list = fhandler.readlines()
f_unique = []

for line in f_list:
    if line not in f_unique:
        f_unique.append(line)
    else:
        pass
for x in f_unique:
    print(x)

def get_score_summary(fhandler):
    """This function generates scores.

	   Argumentsm:
            mixed: results of inspection
        Returns:
            A summary of scores
        Examples:
            >>> get_score_summary('inspection_results.csv')
            >>> {'BRONX': (156, 0.9762820512820514), 'BROOKLYN':
                (417, 0.9745803357314141), 'STATEN ISLAND': (46, 0.9804347826086955),
                'MANHATTAN': (748, 0.9771390374331531), 'QUEENS':
                (414, 0.9719806763285017)}
    """
my_file = []
with open(fhandler) as f:
    for line in f.read().split():
        my_file.append(line)
    print(my_file)

fhandler.close()
 
