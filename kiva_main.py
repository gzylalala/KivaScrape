# -*- coding: utf-8 -*-
"""
Created on Sun Jul 22 22:27:09 2012

@author: Nick
"""

import kiva_api
import kiva_db

while 1:
    loan_id = kiva_db.next_unprocessed_loan()
    print 'Processing loan_id = %d' % loan_id
    lenders = kiva_api.loan_lenders(loan_id)
    # There are blank lender IDs if the lender is anonymous
    lender_ids = filter(lambda x: x!='', 
                        map(lambda x: x['lender_id'], 
                            lenders))
    for lender_id in lender_ids:
        # We don't want to call the Kiva API again more than
        # once per lender
        if kiva_db.lender_exists(lender_id):
            print '~ Already exists, skipping: lender_id %s' % lender_id
            continue
        else:
            print '~ Processing new lender_id %s.' % lender_id
            loans = kiva_api.lender_loans(lender_id)
            print '~~ Found %d loans.' % len(loans)
            for loan in loans:
                kiva_db.store_loan(loan)
    kiva_db.set_loan_processed(loan_id)
    print 'Finished processing loan_id = %d' % loan_id
    