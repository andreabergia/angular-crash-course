import httplib
import json
import sys

if len(sys.argv) == 1:
    print "Please give a city as argument"
    sys.exit(1)
city = sys.argv[1]

conn = httplib.HTTPConnection("api.openweathermap.org")
conn.request("GET", "/data/2.5/forecast/daily?mode=json&units=metric&q=" + city)
resp = conn.getresponse()

# It should print 200 OK
# print resp.status, resp.reason

data = json.load(resp)
day = 1
for forecast in data['list']:
    print "In %d days the temperature will be %d, and the wheather %s" % (day, forecast['temp']['day'], forecast['weather'][0]['description'])
    day += 1
