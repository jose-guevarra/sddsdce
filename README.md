# San Diego DSD Code Violations database

The purpose of this project is to create a more accessible source of property records 
for San Diego DSD Code Violations records. The City of San Diego uses a proprietary web
application to submit and provide access to various city violations e.g. barking dogs,
unpermitted structures, loud music. This project will allow you to:

- Import/Update them into an SQL database
- Automate webscraping of APN information from the city website
- Allow some tools to export the database into csv format



Installation:

+ Install Selenium
hint: https://tecadmin.net/setup-selenium-chromedriver-on-ubuntu/

pip3 install mysql-connector
pip3 install selenium


Run Import:

Step 1: Download all "complaint" records(csv) from https://aca.accela.com/SANDIEGO/Welcome.aspx

Step 2: Import records into the database. Records status will be updated if they already exist.

$>  python3 sddsdce_import.py -f path/to/[CSVFILENAME] -u

Step 3: Now it's time to lookup the citations in the database on the website by scraping pages.

$> python3 sddsdce.py


Now that you have a local copy of citations, you can do some analysis with SQL queries. 
For Example, find all active noise complaints:

mysql $> SELECT * FROM `sddsdce` WHERE `Application Name` LIKE "Noise%" AND `Status` IN ('New','Active Enforcement', 'Active Investigation') ORDER BY `Date` DESC

@TODO: Create script that exports a nicely formatted csv file to upload to Google Maps.

For Example:
https://www.google.com/maps/d/edit?mid=1SQYMWcEzAaNwBHTkds08-RitDERTLalz&usp=sharing




