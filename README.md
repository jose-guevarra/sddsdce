# San Diego DSD Code Violations database

The purpose of this project is to create a more accessible source of property records 
for San Diego DSD Code Violations records. The City of San Diego uses a proprietary web
application to submit and provide access to various city violations e.g. barking dogs,
unpermitted structures, loud music. This project will allow you to:

- Download all records from the city's website
- Import/Update them into an SQL database
- Automate webscraping of APN information from the city website
- Allow some tools to export the database into csv format



Installation:

+ Install Selenium
https://tecadmin.net/setup-selenium-chromedriver-on-ubuntu/

# might not need this - sudo apt-get install -y unzip xvfb libxi6 libgconf-2-4
# might not need this - sudo apt-get install default-jdk


pip3 install mysql-connector
pip3 install selenium


Run Import:

Step 1: Download all "complaint" records(csv) from https://aca.accela.com/SANDIEGO/Welcome.aspx

Step 2: Import records into the database.

$>  python3 sddsdce_import.py -f path/to/[CSVFILENAME] -u

Step 3: Now it's time to lookup the citations in the database on the website by scraping pages.

$> python3 sddsdce.py


