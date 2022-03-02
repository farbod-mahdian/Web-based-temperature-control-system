# Web-based temperature control system

Python, HTML, and CSS Project

Using Python to make a program which reads the current temperature from temperature sensor connected to the Raspberry Pi, and it processes the temperature to turn on/off the heating/cooling system and updates the webpage to show the most recent data. The circuit is designed by me as well as every single program that has been used in this project. The current temperature can be seen through the webpage and the LCD which is connected to the Raspberry Pi. User can set her/his desired minimum and maximum temperature for the place, and the system will make sure to control the temperature between those two values. The webpage is designed by HTML, CSS, and JavaScript; this webpage was running on an APACHE web server.

Demonstration Video:
https://drive.google.com/file/d/1195KgmoA2EVOSE7n4CqwMx2s0c1JQ1XL/view?usp=sharing

Details:
Author: Farbod Mahdian

Description:
Explaination of the files of this folder.

---

The web folder contains all of the files whcih are for the web part of the project.
Since this project was done on a raspberry pi, the addresses of the files in the
source codes are not valid in a windows machine. In fact, all of the addresses in
this folder is invalid because they are copied from different locations of a raspberry pi
machine.

The CGI script will run ONLY if CGI feature has been installed on the system.

---

Web files:

index.html is the main web page of the project which contains the current temperature,
the minimum, and the maximum temperature which has been configured. Also, indicates
the status of the heating/cooling system.

app.js is the JavaScript script which is running on the main web page and making it
possible to navigate the configuring webpage.

setTemp.html is the configuring webpage that asks for new maximum and minimum temperature.
And, it calls the setTemp2.py program by CGI feature.

stylesV3.css is the CSS file for index.html.

setTemp.css is the CSS file for setTemp.html.

result.css is the CSS file for the result page of the setTemp2.py program which can be either
a confirmation or an error page.

index_backup.html is a backup source code from the index.html to keep the templates of the webpage.

---

Continuously running program:

reloadV3.py is the main pythoin program which starts to run after boot up automatically
by using the crontab on the background. It responssible for interacting with the circuit and
different hardware component of it. It is in a endless loop with a 2 seconds delay each time.
It also updates the data of the webpage with the new processed data.

---

Others:

The images folder contains the images that were used in the webpages.

data.txt is the text file which contains the most recent maximum and minimum temperatures
which the user has been entered. It is a bridge between the two python program.

---

END
