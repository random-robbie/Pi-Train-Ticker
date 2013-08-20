#!/usr/bin/python
####################################################################
#																   #
#																   #
#	Raspberry Pi Train Times Ticker								   #
#																   #
#	Made By Robert Wiggins										   #
#																   #
#	txt3rob@gmail.com											   #
#																   #
#																   #
####################################################################
# import the MySQLdb and sys modules and Adafruits LCD Plate
from Adafruit_I2C import Adafruit_I2C
from Adafruit_MCP230xx import Adafruit_MCP230XX
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from time import sleep
import time
import datetime
import MySQLdb
import os
import sys
import urllib2
from os.path import exists
lcd = Adafruit_CharLCDPlate(busnum = 1)

##################################################################
# open a database connection
# be sure to change the host IP address, username, password and database name to match your own
connection = MySQLdb.connect (host = "localhost", user = "root", passwd = "toor", db = "trains")
# prepare a cursor object using cursor() method
cursor = connection.cursor ()

#Download the CSV file from Google Docs	
def downloaddue():
	web_file = urllib2.urlopen("https://docs.google.com/spreadsheet/pub?key=0AuC2xjBKqlYadDJ2TzJkdFh5Wi03Wlh5NmMtdDNOdHc&single=true&gid=0&output=csv")
	out_file = open('/tmp/trains.csv', 'w')
	out_file.write(web_file.read())
	out_file.close()
	
# Create the MySql Table for the due to be imported to.
def table():
	cursor.execute ("CREATE TABLE IF NOT EXISTS `trains`.`Trains` (`Due` varchar(8), `Destination` varchar(27), `Status` varchar(7), `Platform` varchar(10), `Details` varchar(21)) ENGINE=MyISAM DEFAULT CHARACTER SET utf8 COLLATE latin1_sweedish_ci")
# Empty Current Data
def empty():
	cursor.execute("TRUNCATE TABLE  `Trains`")

# Import train due from google docs download
def importdue():
	cursor.execute ("LOAD DATA INFILE '/tmp/trains.csv' INTO TABLE Trains FIELDS TERMINATED BY ',' IGNORE 1 LINES;")



#Delete older due that have passed
def oldtrains():
	cursor.execute ("DELETE  FROM `Trains` WHERE `due` < CURRENT_TIME")



def display():
	#Delete older due that have passed
	cursor.execute ("DELETE  FROM `Trains` WHERE `due` < CURRENT_TIME")
	# display col 0 which contains the due
	cursor.execute ("SELECT * FROM `Trains` WHERE `due` > CURRENT_TIME LIMIT 0 , 1 ")
	# fetch all of the rows from the query
	data = cursor.fetchall ()
	
	for row in data :
		lcd.clear()
		lcd.message("The Next Train\nTo Liverpool")
		lcd.backlight(lcd.GREEN)
		sleep(3)
		lcd.clear()
		lcd.message(row[0])
		lcd.message("\n" + row[2])
		lcd.backlight(lcd.GREEN)
		sleep(15)
		lcd.clear()
		lcd.backlight(lcd.OFF)

def updatecsv():
	path = ("/tmp/trains.csv")
	ftime = os.path.getmtime(path)
	curtime = time.time()
	difftime = curtime - ftime
	if difftime > 3600:
		downloaddue()
		lcd.clear()
		lcd.backlight(lcd.RED)
		lcd.message("Downloading DATA")
		empty()
		lcd.clear()
		lcd.message("Removing Old DATA")
		importdue()
		lcd.clear()
		lcd.message("Import Suscessful")
		sleep (10)
		display()



################## Check for train times CSV file ###############


if exists("/tmp/trains.csv") == True:

	updatecsv()
	display()
	sleep (2)
	display()
	sleep (2)
	display()
	sleep (2)
elif exists("/tmp/trains.csv") == False:
		lcd.clear()
		lcd.backlight(lcd.RED)
		lcd.message("Downloading DATA")
		downloaddue()
		sleep(10)
		lcd.message("Importing DATA")
		empty()
		importdue()
		display()



	
# close the cursor object
cursor.close ()

# close the connection
connection.close ()

# exit the program
sys.exit()
