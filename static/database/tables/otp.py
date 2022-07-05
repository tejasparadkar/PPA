import os
import sqlite3
import csv
from static.database.tables import csvparam as csvparameter

# account table details:
# USERID        : user id
# USERUSERNAME  : username
# USEROTP       : otp
# USERTIME      : otp creation timestamp

CONTENT_PATH = './static/database/content/'
CSV_USER = 'otp.csv'
OTP_FULLPATH = CONTENT_PATH + CSV_USER

SCRIPT_CREATE = 'CREATE TABLE OTPTABLE (USERID integer PRIMARY KEY'
SCRIPT_CREATE += ', USERUSERNAME VARCHAR(32)'
SCRIPT_CREATE += ', USEROTP VARCHAR(6)'
SCRIPT_CREATE += ', USERTIME VARCHAR(32)'
SCRIPT_CREATE += ')'

def otp_init(db):
    # Creates the table
    otp_create(db)

    with open(OTP_FULLPATH) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=csvparameter.CSV_DELIMITER, quotechar=csvparameter.CSV_QUOTE, quoting=csv.QUOTE_MINIMAL, skipinitialspace=True)
        id = 0
        for row in csv_reader:
            if len(row) == 3:
                id += 1
                otp_insert(db, id, row[0], row[1], row[2])

def otp_create(db):
    c = db.cursor()
    c.execute(SCRIPT_CREATE)
    db.commit()

def otp_insert(db,id,username,otp,timestamp):
    c = db.cursor()
    c.execute('INSERT INTO OTPTABLE (USERID, USERUSERNAME, USEROTP, USERTIME) VALUES (?,?,?,?)', (id,username,otp,timestamp))
    db.commit()

def otp_newAccount(db,id,username,otp,timestamp):
    with open(OTP_FULLPATH, 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=csvparameter.CSV_DELIMITER, quotechar=csvparameter.CSV_QUOTE, quoting=csv.QUOTE_MINIMAL)
        writer.writerows([[username,otp,timestamp]])
    id = otp_generateid(db)
    otp_insert(db,id,username,otp,timestamp)

def otp_generateid(db):
    c = db.cursor()
    c.execute('SELECT MAX(USERID)+1 FROM OTPTABLE')
    return c.fetchall()[0][0]

def otp_getUserIdByUsername(db, username):
    c = db.cursor()
    c.execute('SELECT USERID FROM OTPTABLE WHERE USERUSERNAME = (?)', (username,))
    userId = c.fetchall()[0][0]
    return userId

def otp_getUsernameByUserId(db, userId):
    c = db.cursor()
    c.execute('SELECT USERUSERNAME FROM OTPTABLE WHERE USERID = (?)', (userId,))
    username = c.fetchall()[0][0]
    return username

def otp_getOtpByUserId(db, userId):
    c = db.cursor()
    c.execute('SELECT USEROTP FROM OTPTABLE WHERE USERID = (?)', (userId,))
    otp = c.fetchall()[0][0]
    return otp

def otp_getTimestampByUserId(db, userId):
    c = db.cursor()
    c.execute('SELECT USERTIME FROM OTPTABLE WHERE USERID = (?)', (userId,))
    timestamp = c.fetchall()[0][0]
    return timestamp

def otp_updateOtpAndTimestampOfUsername(db, username, otp, timestamp):
    c = db.cursor()
    c.execute('UPDATE OTPTABLE SET USEROTP = (?), USERTIME = (?) WHERE USERUSERNAME = (?)', (otp, timestamp, username))
    db.commit()