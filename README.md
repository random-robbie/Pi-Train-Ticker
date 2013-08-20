Pi-Train-Ticker
===============

Tells you when the next train is from your chosen station (UK).

This will automatically pull down the data every hour and if the data isnt in the database it will automatically pull it in for you

Requires 1 x Adafruits LCD plate

You will need to install mysql for python

Setup
--------

```
sudo apt-get install python-mysqldb mysql-server mysql-client -y
```
ensure you edit trains.py to put in the mysql connection details once you have set them up.

The file will automatically download a CSV from google docs to get the information.

Currently it is set to my CSV for my local station West Kirby.

Create a new CSV on your google docs account and put this in the first row / col

```
=ImportHtml("http://ojp.nationalrail.co.uk/service/ldbboard/dep/wki?ar=true"& year(now()) & month(now()) & day(now()) & hour(now()),"table",1)
```
change the WKI to your station code and then once you have done this ensure you set the spreadsheet to public and capture the download link.



```
def downloaddue():
```
and change the url in the link there.

Find 
```
lcd.message("The Next Train\nTo Liverpool")
```
Change the station name to your local station.

save the file and then run ./trains.py and it will display on your LCD

If you like this project please donate to my Pi-Camera you can donate via paypal to txt3rob@gmail.com

Also any errors PM me on the raspberry pi forums or email me.


