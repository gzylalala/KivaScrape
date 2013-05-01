# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 14:01:46 2012

@author: Nick
"""

import json
import requests
import datetime

# Kiva requests, but does not require, that developers use
# an app_id parameter in API requests. 
APP_ID = 'edu.northwestern.nick'

def reformat(dict_list, translation_dict):
    '''
    >>> dict_list = [{'a': {'b': 3}}]
    >>> translation_dict = {'c': lambda x: x['a']['b']}
    >>> reformat(dict_list, translation_dict)
    ... [{'c': 3}]
    '''
    new_list = []
    # A single item
    if type(dict_list) != list:
        dict_list = [dict_list]
    for original_dict in dict_list:
        new_dict = dict()
        for new_key, get_key in translation_dict.iteritems():
            new_dict[new_key] = get_key(original_dict)
        new_list.append(new_dict)
    return new_list

def get_json(url):
    r = requests.get(url)
    if r.status_code == 200:
        return json.loads(r.content)
    else:
        return {}


def loan_lenders(loan_id):
    '''
    Typical JSON data structure returned:
    
    {
        lender_id: "alancheuk",
        name: "Alan",
        image: {
            id: 24981,
            template_id: 1
        },
        whereabouts: "Burnaby British Columbia",
        country_code: "CA",
        uid: "alancheuk"
    },

    >>> loan_lenders(84)
    ... [u'michael', '_anonymous', u'ward', '_anonymous', u'brooke']
    '''

    json_translation = {'lender_id':            lambda x: x.get('lender_id', ''),
                        'name':                 lambda x: x.get('name', ''),
                        'image_id':             lambda x: x['image']['id'],
                        'image_template_id':    lambda x: x['image']['template_id'],
                        'whereabouts':          lambda x: x.get('whereabouts', ''),
                        'country_code':         lambda x: x.get('country_code', ''),
                        'uid':                  lambda x: x.get('uid', '')}
    
    # The basic Kiva API query to get the list of lenders
    # for a particular loan, as selected by the loan ID.        
    url = 'http://api.kivaws.org/v1/loans/%s/lenders.json&app_id=%s' % (loan_id, APP_ID)
    content = get_json(url)
    # Use the reformat() function with the json_translation dictionary
    # to go from the nested JSON data structure to a flat Python dict.
    lenders = reformat(content.get('lenders', []), json_translation)
    
    # Each request provides a max of 20 lenders, so we need to iterate
    # through the rest of the pages. 
    if 'paging' in content:
        page_count = int(content['paging']['pages'])
        for page_number in range(2, page_count):
            # Only the query URL changes to add the parameter for page number
            content = get_json(url + '&page=%d' % page_number)
            lenders += reformat(content.get('lenders', []), json_translation)
    return lenders


def lender_loans(lender_id):
    def to_datetime(datetime_string):
        # A blank string should have a nonsensical/invalid value
        if datetime_string == '':
            return datetime.datetime(year=1900, month=1, day=1)
        return datetime.datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%SZ")
        
    json_translation = {\
        'loan_id':                          lambda x: x.get('id', -1),
        'borrower_name':                    lambda x: x.get('name', u''),
        'loan_description':                 lambda x: unicode(x.get('description', u'')),
        'loan_languages':                   lambda x: ','.join(x['description']['languages']),
        'loan_status':                      lambda x: x.get('status', u''),
        'funded_amount':                    lambda x: x.get('funded_amount', -1),
        'image_id':                         lambda x: (x.get('image', {})).get('id', -1),
        'template_id':                      lambda x: (x.get('image', {})).get('template_id', -1),
        'borrower_activity':                lambda x: x.get('activity', u''),
        'borrower_activity_sector':         lambda x: x.get('sector', u''),
        'loan_use':                         lambda x: unicode(x.get('use', u'')),
        'borrower_location_country_code':   lambda x: (x.get('location', {})).get('country_code', u''),
        'borrower_location_country':        lambda x: (x.get('location', {})).get('country', u''),
        'borrower_location_town':           lambda x: (x.get('location', {})).get('town', u''),
        'borrower_location_geo_level':      lambda x: (x.get('geo', {})).get('level', u''),
        'borrower_location_geo_pairs':      lambda x: (x.get('geo', {})).get('pairs', u''),
        'borrower_location_geo_type':       lambda x: (x.get('geo', {})).get('type', u''),
        'partner_id':                       lambda x: x.get('partner_id', -1),
        'posted_date':                      lambda x: to_datetime(x.get('posted_date', u'')),
        'planned_expiration_date':          lambda x: to_datetime(x.get('planned_expiration_date', u'')),
        'loan_amount':                      lambda x: x.get('loan_amount',-1),
        'borrower_count':                   lambda x: x.get('borrower_count', -1)}

    url = 'http://api.kivaws.org/v1/lenders/%s/loans.json&app_id=%s' % (lender_id, APP_ID)
    content = get_json(url)
    loans = reformat(content.get('loans', []), json_translation)
    if 'paging' in content:
        page_count = int(content['paging']['pages'])
        for page_number in range(2, page_count):
            content = get_json(url + '&page=%d'%page_number)
            loans += reformat(content['loans'], json_translation)
    for loan in loans:
        loan['lender_id'] = lender_id
    return loans

