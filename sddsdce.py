#!/usr/bin/python3


"""
 @todo - wait for page/element to load
 @todo - create report
 @todo - get headless to work
"""


import time
import yaml
from datetime import datetime
import mysql.connector
from mysql.connector import Error
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def config():
  with open("config.yml", "r") as f:
    return yaml.load(f)


def main():
  cfg = config()

  driver = webdriver.Chrome('/usr/bin/chromedriver')
  dsdurl = cfg["dsdurl"]

  try:
    connection = mysql.connector.connect(user=cfg["mysql"]["user"],
                                         password=cfg["mysql"]["password"],
                                         host=cfg["mysql"]["host"],
                                         database=cfg["mysql"]["db"])

    cursor = connection.cursor()

    q = """SELECT * FROM `sddsdce` WHERE apn IS NULL ORDER BY FIELD(`Status`, 'New', 'Active Investigation', 'Active Enforcement') DESC, Date DESC"""
    cursor.execute(q)
    records = cursor.fetchall()
    numrecords = totalrecords = cursor.rowcount
    print("Total # of Records: ", totalrecords)

    for row in records:
        print("Records Left: ", numrecords)
        print("Date    = ", row[0], )
        print("Number  = ", row[1])
        print("AppName = ", row[3])
        print("Status  = ", row[4], "\n")
        apn = ""
        worklocation = ""
        cnumber = row[1]
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")

        driver.get(dsdurl);
        search_box = driver.find_element_by_id('ctl00_PlaceHolderMain_generalSearchForm_txtGSPermitNumber')
        search_box.clear()
        search_box.send_keys(cnumber)
        search_box.send_keys(Keys.RETURN)

        time.sleep(7)

        #if successful, now on complaint page. GET Work Location data

        # You have to click down these elements to reveal apn info
        if driver.find_elements_by_css_selector('#lnkMoreDetail'):
            driver.find_element_by_css_selector('#lnkMoreDetail').click()

            if driver.find_elements_by_css_selector('#lnkParcelList'):
              driver.find_element_by_css_selector('#lnkParcelList').click()
              apn = driver.find_element_by_css_selector('#ctl00_PlaceHolderMain_PermitDetailList1_palParceList > div:nth-child(1) > div').text
            else:
              apn = "NOAPN"
        else:
            apn = "NOAPN"

        worklocation = driver.find_element_by_css_selector('#tbl_worklocation > tbody > tr > td.NotBreakWord').text

        print("APN: ", apn.replace('-',""))
        print("Work Location: ", worklocation.replace("\n"," "))
        print("\n---------------\n")

        if apn != "" or worklocation != "" :
          q = """UPDATE sddsdce SET `Apn` = '%s', `Work Location` = '%s' WHERE `Record Number` = '%s'""" % (apn.replace('-',""), worklocation.replace("\n"," ").replace("'","").replace("\\",""), cnumber)
          cursor.execute(q)
          connection.commit()
        numrecords -= 1

    #time.sleep(5) # Let the user actually see something!
    driver.quit()


  except Error as e:
      print("Error reading data from MySQL table", e)
  finally:
      if (connection.is_connected()):
          connection.close()
          cursor.close()
          print("MySQL connection is closed")


if __name__ == "__main__":
    main()

# end
