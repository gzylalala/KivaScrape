# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 20:28:40 2012

@author: Nick

{
    "id": 84,
    "name": "Justine",
    "description": {
      "languages": ["en"],
      "texts": {
        "en": "<i>The following description was written by Moses O., a volunteer with Village Enterprise Fund and partner representative for Kiva in Uganda:<\/i><br><br>Justine O. is among the most successful small-scale business leaders.<br><br>He got a grant of 100 US dollars from VEF.  He started by buying and selling of goats right away. Most butchers have known his business, so a number of them come to him to buy goats.<br><br>He can now buy and sell between 15 and 20 goats in a month -- a great amount.<br><br>The market is very open since most of Ugandans rear goats and cows for raising money whenever needs arise like school fees, sickness, death, journey etc.<br><br>O. has attended business training and he is capable of handling the loan and paying it back.<br><br>Given a loan of 500 US dollars, he is targeting to introduce bulls for slaughter and opening up a butcher shop himself. "
      }
    },
    "status": "paid",
    "funded_amount": 500,
    "basket_amount": null,
    "paid_amount": 500,
    "image": {
      "id": 241,
      "template_id": 1
    },
"""


import glob
import json
import unicodecsv
import os

loan_json_path = r'C:\Users\Nick\Downloads\kiva_ds_json\loans'
output_path = r'c:\users\nick\dropbox\code\jay_kiva\loans.csv'

loan_keys = {'id': lambda x: x['id'],
             'name': lambda x: x['name'],
             'description_en': lambda x: x['description']['texts'].get('en', 'There was no English description for this loan.'),
             'status': lambda x: x['status'],
             'funded_amount': lambda x: x['funded_amount'],
             'basket_amount': lambda x: x['basket_amount'],
             'paid_amount': lambda x: x['paid_amount'],
             'image_id': lambda x: x['image']['id'],
             'image_template_id': lambda x: x['image']['template_id']}

def reformat(loan_list):
    new_list = []
    for loan in loan_list:
        new_loan = dict()
        for new_key, get_key in loan_keys.iteritems():
            new_loan[new_key] = get_key(loan)
        new_list.append(new_loan)
    return new_list             
    
if __name__ == "__main__":
    loan_filenames = glob.glob(os.path.join(loans_path, '*.json'))    
    with open(output_path, 'wb') as outfile:
        writer = unicodecsv.DictWriter(outfile, fieldnames=loan_keys)
        writer.writeheader()
        for file_number, filename in enumerate(loan_filenames):
            print '%d ~ ' % file_number,
            with open(filename, 'rb') as infile:
                loans = reformat(json.load(infile)['loans'])
                writer.writerows(loans)