#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Week 13 Task 01 - boroughs health violations module."""

import csv
import json

GRADES = {'A': 1.00, 'B': 0.90, 'C': 0.80, 'D': 0.70, 'F': 0.60}


def get_score_summary(filename):
    """ Processes the csv file identified by the file name and summarize the
        data.

    Args:
        filename (string): name of the csv file to be processed.

    Returns:
        dictionary: summarized list keyed by BORO with a tuple (containing the
        number of restaurateurs per boro with scores and the average score for
        that boro) as a value.

    Examples:
        >>> get_score_summary('inspection_results.csv')
        >>> {'BRONX': (156, 0.9762820512820514), 'BROOKLYN':
        (417, 0.9745803357314141), 'STATEN ISLAND': (46, 0.9804347826086955),
        'MANHATTAN': (748, 0.9771390374331531), 'QUEENS':
        (414, 0.9719806763285017)}
    """
    restlist = {}
    borolist = {}
    borosumm = {}

    try:
        cs_file = open(filename, 'rb')

    except IOError as ioe:
        print 'Failed to open CSV file {0}, error code {1}'.format(filename,
                                                                   ioe.errno)
        raise ioe

    try:
        csd_read = csv.DictReader(cs_file)

        for datarow in csd_read:

            camkey = datarow['CAMIS']
            igrade = GRADES.get(datarow['GRADE'], None)

            if igrade is not None and camkey not in restlist:
                restlist[camkey] = {'BORO': datarow['BORO'], 'GRADE': igrade}

    except IOError as ioe:
        print 'I/O Error reading CSV file: {0}:{1}'.format(ioe.errno,
                                                           ioe.strerror)
        raise ioe

    for restinfo in restlist.values():

        borokey = restinfo['BORO']

        if borokey in borolist:
            borolist[borokey]['COUNT'] += 1
            borolist[borokey]['GRADE'] += restinfo['GRADE']

        else:
            borolist[borokey] = {}
            borolist[borokey]['COUNT'] = 1
            borolist[borokey]['GRADE'] = restinfo['GRADE']

    for borokey in borolist.keys():

        gradecnt = borolist[borokey]['COUNT']
        gradeave = borolist[borokey]['GRADE'] / gradecnt
        borosumm[borokey] = (gradecnt, gradeave)

    return borosumm


def get_market_density(filename):
    """ Processes the JSON file identified by the file name and summarize the
        data.

    Args:
        filename (string): name of the JSON file to be processed.

    Returns:
        dictionary: summarized list keyed by BORO with an integer value of the
                    number of markets in the borough.

    Examples:
        >>> get_market_density('green_markets.json')
        {u'STATEN ISLAND': 2, u'BROOKLYN': 48, u'BRONX': 32,
        u'MANHATTAN': 39, u'QUEENS': 16}
    """
    markets = {}

    try:
        jfile = open(filename, 'r')

    except IOError as ioe:
        print 'Failed to open JSON file {0}, error code {1}'.format(filename,
                                                                    ioe.errno)
        raise ioe

    try:
        jdata = json.load(jfile)

    except IOError as ioe:
        print 'I/O Error reading CSV file: {0}:{1}'.format(ioe.errno,
                                                           ioe.strerror)
        raise ioe

    for dataline in jdata['data']:

        borokey = str(dataline[8].upper().rstrip())

        if borokey in markets:
            markets[borokey] += 1

        else:
            markets[borokey] = 1

    return markets


def correlate_data(csvfname, jsnfname, outfname):
    """ Processes the CSV and JSON files identified and merge the data, then
        write the JSON data to the output file.

    Args:
        csvfname (string): name of the CSV file to be processed.
        jsnfname (string): name of the JSON file to be processed.
        outfname (string): name of the JSON file to be written to.

    Returns:
        None.

    Examples:
        >>> correlate_data('inspection_results.csv', 'green_markets.json',
                            'summary_data.json')
    """
    mrgdata = {}

    rdata = get_score_summary(csvfname)
    mdata = get_market_density(jsnfname)

    for borokey in rdata.keys() + mdata.keys():

        if borokey not in mrgdata:

            rscore = rdata.get(borokey, (None, None))[1]
            mcount = mdata.get(borokey, None)
            mpct = None if rscore is None or mcount is None else \
                float(mcount) / rdata[borokey][0]

            mrgdata[borokey] = (rscore, mpct)

    try:
        joutfile = open(outfname, 'w')

    except IOError as ioe:
        openemsg = 'Failed to open JSON output file {0}, error code {1}'
        print openemsg.format(outfname, ioe.errno)
        raise ioe

    try:
        json.dump(mrgdata, joutfile)

    except IOError as ioe:
        print 'I/O Error writing JSON file: {0}:{1}'.format(ioe.errno,
                                                            ioe.strerror)
        raise ioe
