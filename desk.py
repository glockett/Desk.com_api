import pycurl
import json
import os
from io import BytesIO

# Set conf to environment from config.json (test, android or ios)
with open('config.json') as json_data:
    data = json.load(json_data)

cf_site = data['site']
cf_login = data['login']
cf_password = data['password']


data = BytesIO()


url = "https://guardianuserhelp.desk.com/api/v2/labels"

# url = "https://guardianuserhelp.desk.com/api/v2/cases"

# url = "https://guardianuserhelp.desk.com/api/v2/labelssearch?id=4055243"


c = pycurl.Curl()
c.setopt(pycurl.URL, url)
c.setopt(pycurl.HTTPHEADER, ["Accept: application/json, sort_field=created_at&sort_direction=desc"])

# # c.setopt(pycurl.HTTPHEADER, ["-H 'Accept: application/json' \
#     -H 'Content-Type: application/json' \
#     -H 'X-HTTP-Method-Override: PATCH'"])

c.setopt(pycurl.USERPWD, '%s:%s' % (cf_login, cf_password))
c.setopt(c.WRITEFUNCTION, data.write)
c.perform()

deskData = json.loads(data.getvalue())

print deskData

#Output the data to a jSon file
with open('deskdata.json', 'w') as outfile:
    outfile.write(json.dumps(deskData))
    outfile.close()
    print
    print "Output File: ", os.getcwd()
