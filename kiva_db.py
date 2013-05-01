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
conn = engine.connect()

# sqlalchemy will use a feature called reflection to automatically
# detect the structure of the tables below, saving us from having to
# painstakingly reproduce the table details in the code. 
Loans = Table('kiva_lending_details', metadata, mysql_engine='MyISAM', autoload=True)
Loan_ids = Table('loan_ids', metadata, mysql_engine='MyISAM', autoload=True)

def populate_loan_ids(file_path):
    with open(file_path, 'r') as f:
#        pdb.set_trace()
        for line_number, line in enumerate(f.readlines()):
            if line == '':
                continue
            loan_id = int(line.strip())
            result = conn.execute(Loan_ids.insert().\
                                            values(loan_id=loan_id, processed='N'))
            if line_number % 1000 == 0: 
                print '%d ... '%line_number, 

def lender_exists(lender_id):
  s = text("""SELECT 
                COUNT(*) 
              FROM 
                kiva_lending_details 
              WHERE 
                lender_id LIKE :lender_id""")
  # We want the COUNT(*) value, which is the first field of the first record returned
  records_count = conn.execute(s, lender_id=lender_id).fetchall()[0][0]
  # We return a boolean value, whether there exist one or more records in the db
  # for lender_id
  return (records_count > 0)

def loan_processed(loan_id):
    s = text("""SELECT 
                  *
                FROM 
                  loan_ids 
                WHERE 
                  loan_id = :loan_id
                LIMIT 
                    1""")
    loan_record = conn.execute(s, loan_id=loan_id).fetchone()
    # the processed field defaults to 'N', until that loan has been processed
    return (loan_record['processed'] == 'Y')


def store_loan(loan):
  result = conn.execute(Loans.insert().values(**loan))
  # except UnicodeEncodeError:
  #   print 'Encoding error on ' + str(loan)
  #   result = -1
  return result
  
  
def set_loan_processed(loan_id):
  result = conn.execute(Loan_ids.\
                          update().\
                          where(Loan_ids.c.loan_id==loan_id).\
                          values(processed='Y'))
  return result

def next_unprocessed_loan():
  # Finds the first loan_id record in the Loan_ids table where
  # the processed field is 'N'
  s = text("""SELECT
                  loan_id
              FROM
                  loan_ids
              WHERE
                  processed = 'N'
              LIMIT 
                  1""")
  loan_id = conn.execute(s).fetchone()['loan_id']
  return loan_id