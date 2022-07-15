"""
Contains functions used to handle requests to postgress db.
"""

import configparser
import logging
import os
import psycopg2

PWD = os.environ.get('db_pass')

logging.basicConfig(
        filename = 'logs/postgres_handler.log',
        level = logging.INFO,
        format = '%(levelname)s:%(asctime)s:%(message)s')

def get_cidr_list():
    """Returns a list of previous used CIDR blocks"""
    try:
        cur,conn = postgres_connect()
        sql_query = "SELECT cidr FROM used_cidr"
        cur.execute(sql_query)
        raw_records = cur.fetchall()
        clean_records = []
        for record in raw_records:
            clean_records.append(record[0])
        cur.close()
        conn.close()
        return clean_records
    except Exception as error:
        logging.error(error)
        return []

def check_if_cidr_used(cidr):
    """Checks if CIDR exist in DB"""
    cidr_list = get_cidr_list()
    if cidr in cidr_list:
        return True
    return False

def push_cidr_to_db(cidr):
    """Insert Data to USED CIDR DB"""
    try:
        cur,conn = postgres_connect()
        if check_if_cidr_used(cidr) is not True:
            sql_query = "INSERT INTO USED_CIDR (cidr) VALUES ('{}')".format(cidr)
            cur.execute(sql_query)
            conn.commit()
            logging.info("Commiting to database...")
        cur.close()
        conn.close()
    except Exception as error:
        logging.error(error)

def postgres_connect():
    """Connect's to DB and inserting new data"""
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        dbname = config['db_config']['DATABASE']
        conn = psycopg2.connect(
            host = config['db_config']['HOSTNAME'],
            dbname = dbname,
            user = config['db_config']['USERNAME'],
            password = PWD,
            port = config['db_config']['PORT_ID'])
        logging.info("Connecting to database...")
        cur = conn.cursor()
        create_table =  "CREATE TABLE IF NOT EXISTS USED_CIDR (cidr text);"
        cur.execute(create_table)
        conn.commit()
        return cur,conn
    except Exception as error:
        logging.error(error)
        return 0


if __name__ == '__main__':
    conf = configparser.ConfigParser()
    conf.read('config.ini')
    mylist = get_cidr_list()
    print(mylist)
  
