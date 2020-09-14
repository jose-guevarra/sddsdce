#!/usr/bin/python3

"""

"""


import sys
import datetime
import csv
import yaml
import mysql.connector
from mysql.connector import Error
from argparse import ArgumentParser


def config():
    with open("config.yml", "r") as f:
        return yaml.load(f)


# Function to covert string to datetime
def convert(date_time):
  format = '%m/%d/%Y' # The format
  return datetime.datetime.strptime(date_time, format)


def _printcitation(date,number,type,appname,status,desc):
    print("-------")
    print("Citation   :",number)
    print("Date       :",date)
    print("Type       :",type)
    print("App Name   :",appname)
    print("Status     :",status)
    print("Description:",desc, "\n")


def getopts():
  parser = ArgumentParser()
  parser.add_argument("-f", "--file", required=True, help="CSV file to process.")
  parser.add_argument("-u", "--update", action="store_true", help="Update database.")
  args = parser.parse_args()
  file = args.file;
  return args.update, file


def main():
  update_records, datafile = getopts()
  NEWRECORDS = 0
  cfg = config()

  try:
    connection = mysql.connector.connect(user=cfg["mysql"]["user"],
                                         password=cfg["mysql"]["password"],
                                         host=cfg["mysql"]["host"],
                                         database=cfg["mysql"]["db"])

    cursor = connection.cursor()

    with open(datafile) as csvfile:
      cits = csv.reader(csvfile, delimiter=',')

      itercits = iter(cits) # skip header
      next(itercits)

      for cit in itercits:
        cdate = cit[0];
        cnumber = cit[1];
        ctype = cit[2];
        cappname = cit[3];
        cstatus = cit[4];
        cdesc = cit[5];

        q = """SELECT * FROM sddsdce WHERE `Record Number` = '%s'""" % cnumber
        cursor.execute(q, cnumber)
        record = cursor.fetchone()

        if cursor.rowcount == -1:
          print ("New Record.")
          _printcitation(cdate,cnumber,ctype,cappname,cstatus,cdesc)

          if update_records:
            q = """INSERT INTO sddsdce
            (`Date`, `Record Number`, `Record Type`, `Application Name`, `Status`, `Description`, `Code`)
            VALUES
            ('%s','%s','%s','%s','%s','%s', '%s')""" % (convert(cdate),cnumber,ctype,cappname,cstatus,cdesc.replace('"','_').replace('\'',""), 'NEW')
            print ("Creating Citation Record!", "\n========\n")
            cursor.execute(q)
            connection.commit()
            NEWRECORDS += 1
        else:

          RECORDCHANGE = False
          if ctype != record[2]: RECORDCHANGE = True
          if cappname != record[3]: RECORDCHANGE = True
          if cstatus != record[4]: RECORDCHANGE = True

          if RECORDCHANGE:
            _printcitation(cdate,cnumber,ctype,cappname,cstatus,cdesc)
            _printcitation(record[0],record[1],record[2],record[3],record[4],record[5])
            if args.update:
              q = """UPDATE sddsdce SET
              `Date` = '%s', `Record Type` = '%s', `Application Name` = '%s', `Status` = '%s',
              `Description` = '%s', `Code` = '%s' WHERE `Record Number` = '%s'""" % (convert(cdate),ctype,cappname,cstatus,cdesc.replace('"','_').replace('\'',""), 'CITUPDATED',cnumber)

              print ("Updating Citation Record!", "\n========\n")
              cursor.execute(q)
              connection.commit()

    print ("Records Inserted: ", NEWRECORDS)
  except Error as e:
      print("Error reading data from MySQL table", e)
  finally:
      if connection is not None and connection.is_connected():
        connection.close()
        cursor.close()


if __name__ == "__main__":
    main()

#END

