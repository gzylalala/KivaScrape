Create table kiva_Lending_details
(
Lender_id  varchar(50) CHARACTER SET utf8 NOT NULL,
Loan_id int(11) NOT NULL,
borrower_name varchar(50) CHARACTER SET utf8 NOT NULL,
loan_description blob,
loan_languages  varchar(10) CHARACTER SET utf8 DEFAULT NULL,
loan_status  varchar(50) CHARACTER SET utf8 DEFAULT NULL,
funded_amount int(11),
paid_amount int(11),
image_id int(11),
template_id int(11),
borrower_activity varchar(500) CHARACTER SET utf8 DEFAULT NULL,
borrower_activity_sector varchar(500) CHARACTER SET utf8 DEFAULT NULL,
loan_use blob,
borrower_location_country_code varchar(10) CHARACTER SET utf8 DEFAULT NULL,
borrower_location_country varchar(50) CHARACTER SET utf8 DEFAULT NULL,
borrower_location_town varchar(100) CHARACTER SET utf8 DEFAULT NULL,
borrower_location_geo_level varchar(50) CHARACTER SET utf8 DEFAULT NULL,
borrower_location_geo_pairs varchar(50) CHARACTER SET utf8 DEFAULT NULL,
borrower_location_geo_type varchar(50) CHARACTER SET utf8 DEFAULT NULL,
partner_id int(11),
posted_date  datetime DEFAULT NULL,
planned_expiration_date datetime DEFAULT NULL,
loan_amount int(11),
borrower_count int(11)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;



