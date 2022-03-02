#!/home/pi/software/bin/python3
# Name: Farbod Mahdian
# Student ID: 135438190
print("Content-type: text/html\n\n")

import datetime
import urllib.request
import re
import cgi, cgitb

cgitb.enable()

form = cgi.FieldStorage()

minTemp = str(form.getvalue('minTemp'))
maxTemp = str(form.getvalue('maxTemp'))

# Validating the entered inputs
if maxTemp != "None" and minTemp != "None":
	minTemp = float(minTemp)
	maxTemp = float(maxTemp)
else:
	maxTemp = -1
	minTemp = -1


def writeTemp(fn, min_, max_): # Update the text file with the new entered values (if they were valid)
    try:
        f = open(fn, "w")
        f.writelines("%.2f, %.2f" % (min_, max_))
    except IOError:
        print("ERROR... file data could not be loaded")
    else:
        f.close()


data_path = "/home/pi/Desktop/tempsensor/data.txt"

print("<html>\n")
print("<head>\n")
print("<title>Temperatures Checking Result</title>\n")
print('<link rel="stylesheet" href="../result.css" />')
print("</head>\n")
print("<body>\n")
print("<div>\n")

if (maxTemp - minTemp) >= 1:
	writeTemp(data_path, minTemp, maxTemp)
	print("<p>The minimum and maximum temperature are updated!</p>")
	print('<a href="..">Back to the main page</a>')
else:
	print("<p>ERROR: Invalid Input<br />")
	print("The maximum temperature should be at least one degree higher than the minimum temperature. Please try again by clicking on the back button.</p>")
	print('<a href="javascript:javascript:history.go(-1)">Back</a>')
	
print("</div>\n")
print("</body>\n")
print("</html>\n")
