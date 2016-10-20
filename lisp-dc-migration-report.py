#Added email reporting support

import requests
from requests.auth import HTTPBasicAuth
from urllib.request import Request, urlopen
import json
import ssl
import smtplib
from email.mime.text import MIMEText
import time

now = time.strftime("%c")

f = open('LISP-MIGRATION-REPORT.txt', 'w')

#The first section of the script does an API call to first CSR retrieve the token
auth1 = HTTPBasicAuth('admin', 'Passw0rd!!')
csr1 = "https://192.168.175.110:55443"
csr1_url = csr1 + '/api/v1/auth/token-services'
post_csr1_response = requests.post(csr1_url, verify=False, auth=auth1)
post_csr1_json = post_csr1_response.json()
my_token1 = post_csr1_json["token-id"]
#print(json.dumps(my_token1, indent=4, separators=('.', ': ')))

#The second section of the script does another API call to get the routing table from the first CSR in JSON format
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req1 = Request('https://192.168.175.110:55443/api/v1/routing-svc/routing-table')
req1.add_header('Authorization', 'Basic YWRtaW46UGFzc3cwcmQhIQ==')
req1.add_header('Accept', 'application/json')
req1.add_header('X-Auth-Token', my_token1)

response1 = urlopen(req1, context=ctx)
responseString1 = response1.read().decode("utf-8")

jsonObject1 = json.loads(responseString1)
total_routes1 = len(jsonObject1["items"])

z = 0

print("Here is the list of Dynamic-EIDs located in DC1:")
f.write("---   DATA CENTER 1   ---" "\n")
f.write("Here is the list of Dynamic-EIDs located in DC1:" "\n")

for x in range(0,total_routes1):
    dest_network1 = jsonObject1["items"][x]["destination-network"]
    protocol1 = jsonObject1["items"][x]["routing-protocol"]
    w = z
    if protocol1 == ("LISP"):
        print(dest_network1)
        f.write(dest_network1)
        f.write("\n")
        z = w + 1
    else:
        pass

o = str(z)
print("\n" "The total number of Dynamic-EIDs located in DC1 is:", z)
f.write("\n")
f.write("The total number of Dynamic-EIDs located in DC1 is: ")
f.write(o)

#The third section of the script does an API call to second CSR retrieve the token
auth2 = HTTPBasicAuth('admin', 'Passw0rd!!')
csr2 = "https://192.168.175.111:55443"
csr2_url = csr2 + '/api/v1/auth/token-services'
post_csr2_response = requests.post(csr2_url, verify=False, auth=auth2)
post_csr2_json = post_csr2_response.json()
my_token2 = post_csr2_json["token-id"]
#print(json.dumps(my_token2, indent=4, separators=('.', ': ')))

#The second section of the script does another API call to get the routing table from the second CSR in JSON format

req2 = Request('https://192.168.175.111:55443/api/v1/routing-svc/routing-table')
req2.add_header('Authorization', 'Basic YWRtaW46UGFzc3cwcmQhIQ==')
req2.add_header('Accept', 'application/json')
req2.add_header('X-Auth-Token', my_token2)

response2 = urlopen(req2, context=ctx)
responseString2 = response2.read().decode("utf-8")

jsonObject2 = json.loads(responseString2)
total_routes2 = len(jsonObject2["items"])

p = 0

print("\n" "Here is the list of Dynamic-EIDs located in DC2:")
f.write("\n" "\n" "\n")
f.write("---   DATA CENTER 2   ---" "\n")
f.write("Here is the list of Dynamic-EIDs located in DC2:")

for r in range(0,total_routes2):
    dest_network2 = jsonObject2["items"][r]["destination-network"]
    protocol2 = jsonObject2["items"][r]["routing-protocol"]
    q = p
    if protocol2 == ("LISP"):
        print(dest_network2)
        f.write(dest_network2)
        f.write("\n")
        p = q + 1
    else:
        pass

m = str(p)
print("\n" "The total number of Dynamic-EIDs located in DC2 is:", p)
f.write("\n")
f.write("The total number of Dynamic-EIDs located in DC2 is: ")
f.write(m)
f.close()

fp = open('LISP-MIGRATION-REPORT.txt', 'r')
msg = MIMEText(fp.read())
fp.close()

now_string = str(now)
email_subject = ("LISP MIGRATION REPORT " + now_string)

me = ("sender@gmail.com")
you = ("receiver@hotmail.com")
msg['Subject'] = email_subject
msg['From'] = me
msg['To'] = you

s = smtplib.SMTP('smtp.gmail.com', 587)
s.ehlo()
s.starttls()
s.login('sender@gmail.com', 'PASSWORD')
s.sendmail(me, [you], msg.as_string())
s.quit()

    
