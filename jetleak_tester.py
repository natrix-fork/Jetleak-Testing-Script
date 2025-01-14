import http.client, urllib, ssl, string, sys, getopt
from urllib.parse import urlparse

'''

Author: Gotham Digital Science

Purpose: This tool is intended to provide a quick-and-dirty way for organizations to test whether
                 their Jetty web server versions are vulnerable to JetLeak. Currently, this script does
                 not handle sites with invalid SSL certs. This will be fixed in a future iteration.

'''

if len(sys.argv) < 3:
    print("Usage: jetleak.py [url] [port]")
    sys.exit(1)

url = urlparse(sys.argv[1])
if url.scheme == '' and url.netloc == '':
    print("Error: Invalid URL Entered.")
    sys.exit(1)

port = sys.argv[2]

conn = None

if url.scheme == "https":
    conn = http.client.HTTPSConnection(url.netloc + ":" + port, context=ssl._create_unverified_context())
elif url.scheme == "http":
    conn = http.client.HTTPConnection(url.netloc + ":" + port)
else:
    print("Error: Only 'http' or 'https' URL Schemes Supported")
    sys.exit(1)

x = "\x00"
headers = {"Referer": x}
conn.request("POST", "/", "", headers)
r1 = conn.getresponse()
print("\n")
print(r1.reason)

if (r1.status == 400 and ("Illegal character 0x0 in state" in r1.reason)):
    print("\r\nThis version of Jetty is VULNERABLE to JetLeak!")
else:
    print("\r\nThis version of Jetty is NOT vulnerable to JetLeak.")
