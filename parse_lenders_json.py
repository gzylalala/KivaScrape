# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 20:03:28 2012

@author: Nick

{
    "lender_id": "matt",
    "name": "Matt",
    "image": {
      "id": 12829,
      "template_id": 1
    },
    "whereabouts": "San Francisco CA",
    "country_code": "US",
    "uid": "matt",
    "member_since": "2006-01-01T09:01:01Z",
    "personal_url": "twitter.com\/mattflannery",
    "occupation": "Entrepreneur",
    "loan_because": "I love the stories. ",
    "occupational_info": "I co-founded a startup nonprofit (this one!) and I work with an amazing group of people dreaming up ways to alleviate poverty through personal lending. ",
    "loan_count": 137,
    "invitee_count": 32
  }
"""

import glob
import json
import unicodecsv
import os 

lender_json_path = r'C:\Users\Nick\Downloads\kiva_ds_json\lenders'
output_path = r'c:\users\nick\dropbox\code\jay_kiva\lenders.csv'

lender_keys = {'lender_id': lambda x: x['lender_id'], 
               'name': lambda x: x['name'], 
               'image_id': lambda x: x['image']['id'], 
               'image_template_id': lambda x: x['image']['template_id'], 
               'whereabouts': lambda x: x['whereabouts'], 
               'country_code': lambda x: x['country_code'], 
               'uid': lambda x: x['uid'], 
               'member_since': lambda x: x['member_since'], 
               'personal_url': lambda x: x['personal_url'], 
               'occupation': lambda x: x['occupation'], 
               'loan_because': lambda x: x['loan_because'], 
               'occupational_info': lambda x: x['occupational_info'],
               'loan_count': lambda x: x['loan_count'], 
               'invitee_count': lambda x: x['invitee_count']}

def reformat(lender_list):
    new_list = []
    for lender in lender_list:
        new_lender = dict()
        for new_key, get_key in lender_keys.iteritems():
            new_lender[new_key] = get_key(lender)
        new_list.append(new_lender)
    return new_list

if __name__ == "__main__":
    lender_filenames = glob.glob(os.path.join(lender_json_path, '*.json'))
    with open(output_path, 'wb') as outfile:
        writer = unicodecsv.DictWriter(outfile, fieldnames=lender_keys)
        writer.writeheader()
        for file_number, filename in enumerate(lender_filenames):
            print '%d ~ ' % file_number,
            with open(filename, 'rb') as infile:
                lenders = reformat(json.load(infile)['lenders'])
                writer.writerows(lenders)
            
    