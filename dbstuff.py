from sqlalchemy import create_engine, Table, text
from sqlalchemy.ext.declarative import declarative_base
import datetime

mysql_username = 'kiva'
mysql_password = 'kiva'
mysql_hostname = 'localhost'
mysql_port = 3306
mysql_db = 'kiva'
engine = create_engine('mysql://%s:%s@%s:%d/%s' % \
              (mysql_username, mysql_password, mysql_hostname, mysql_port, mysql_db), 
            echo=False,
            convert_unicode = True)
Base = declarative_base(engine)
metadata = Base.metadata
metadata.bind = engine
# Session = sessionmaker(bind=engine)
# session = Session()
# I love reflection:
Loans = Table('kiva_lending_details', metadata, mysql_engine='MyISAM', autoload=True)
Loan_ids = Table('loan_ids_processed', metadata, mysql_engine='MyISAM', autoload=True)

sample_loan = {\
        'lender_id':                      'matt',
        'loan_id':                        442688,
        'borrower_name':                  'Thandy',
        'loan_description':               {'languages': ["en"]},
        'loan_languages':                 'en',
        'loan_status':                    'funded',
        'funded_amount':                  '2050',
        'image_id':                       1126465,
        'template_id':                    1,
        'borrower_activity':              'Higher education costs',
        'borrower_activity_sector':       'Education',
        'loan_use':                       'to pay for one year of tuition and basic expenses at the Maharishi Institute.',
        'borrower_location_country_code': 'ZA',
        'borrower_location_country':      'South Africa',
        'borrower_location_town':         'Johannesburg',
        'borrower_location_geo_level':    'country',
        'borrower_location_geo_pairs':    '-30 26',
        'borrower_location_geo_type':     'point',
        'partner_id':                     211,
        'posted_date':                    datetime.datetime.strptime("2012-06-28T16:05:04Z", "%Y-%m-%dT%H:%M:%SZ"),
        'planned_expiration_date':        datetime.datetime.strptime("2012-07-28T16:05:04Z", "%Y-%m-%dT%H:%M:%SZ"),
        'loan_amount':                    2050,
        'borrower_count':                 1}

# The following loan is currently tripping the program, because the loan_use
# field is encoded in some vietnamese encoding probably
# It throws this error in store_loan_in_db()
# UnicodeEncodeError: 'charmap' codec can't encode character u'\u1ed1' in position 5: character maps to <undefined>
problematic_loan = {'funded_amount': 875, 'loan_id': 59728, 'posted_date': datetime.datetime(2008, 9, 3, 2, 20, 25), 'borrower_location_geo_level': '', 'borrower_activity': u'Construction', 'borrower_location_geo_pairs': '', 'borrower_location_country': u'Viet Nam', 'planned_expiration_date': datetime.datetime(1900, 1, 1, 0, 0), 'partner_id': 85, 'borrower_count': 5, 'loan_use': u'vay v\u1ed1n ch\u0103n nu\xf4i v\xe0 l\xe0m n\xf4ng ngh\u1ec7p', 'lender_id': u'carl', 'image_id': 189146, 'loan_amount': 875, 'loan_languages': u'vi', 'borrower_location_town': u'Bac Ninh', 'borrower_location_country_code': u'VN', 'borrower_name': u"Thi Man's Group", 'loan_description': {u'languages': [u'vi']}, 'borrower_activity_sector': u'Construction', 'loan_status': u'paid', 'template_id': 1, 'borrower_location_geo_type': ''}

def lender_exists_in_db(lender_id):
  conn = engine.connect()
  s = text("""SELECT COUNT(*) FROM kiva_lending_details WHERE lender_id LIKE :lender_id""")
  num_matched_records = conn.execute(s, lender_id=lender_id).fetchall()[0][0]
  if num_matched_records > 0:
      print 'lender_id ' + lender_id + ' already exists in db!'
  return num_matched_records > 0

def loan_id_processed(loan_id):
    conn = engine.connect()
    s = text("""SELECT COUNT(*) FROM loan_ids_processed WHERE loan_id = :loan_id""")
    num_matched_records = conn.execute(s, loan_id=loan_id).fetchall()[0][0]
    if num_matched_records > 0:
        print 'loan_id ' + loan_id + ' already exists in db!'
    return num_matched_records

def store_loan_in_db(loan):
  try:
    result = Loans.insert().execute(**loan)
  except UnicodeEncodeError:
    print 'Encoding error on ' + str(loan)
    result = -1
  return result
  
  
def store_loan_id_in_db(loan_id):
  return Loan_ids.insert().execute(**loan_id)