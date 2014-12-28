#
# USAGE: python checkLinksInWayback.py <inputFile> 
#
# inputFile: CSV file, 1st item descriptor, 2nd URl (both wrapped in quotation marks) 
# 
# Output items (comma separated):
#
# * item description (from input file)
# * True/False field that indicates availability in WayBack 
# * URL of most recent capture in Wayback
#
# Output is written to stdout
#
# Tested with Python 2.7.6
#
# Based on: https://github.com/bitsgalore/iawayback
# Author: Johan van der Knijff
#
# Published as open source software under the Apache license:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#

import sys
import codecs
import urllib2
import json
import csv

def checkURL(url):

    # API url (see: http://archive.org/help/wayback_api.php)
    urlAPI="http://archive.org/wayback/available?url="

    # URL we want to search for
    urlSearch = url

    req = urllib2.Request(urlAPI + urlSearch)
    response = urllib2.urlopen(req)
    the_page = response.read()

    # Decode json object
    data = json.loads(the_page)
    snapshots = data['archived_snapshots']
    if len(snapshots) == 0:
        # No snapshots available, so not available in Wayback
        available = False
        urlWayback = ""
        status = ""
        timestamp = ""

    else:
        # Snapshot(s) available
        # For now API only returns 1 snaphot, which is the most recent one.
        # May change in future API versions.
        closest = snapshots['closest']
        available = closest['available']
        urlWayback = closest['url']
        status = closest['status']
        timestamp = closest['timestamp']
    
    return(available, urlWayback, status, timestamp)

def main():
    
    if len(sys.argv) == 1:
        sys.stderr.write("USAGE: python checkLinksInWayback.py <inputFile> \n")
        sys.exit()
    inputFile = sys.argv[1]

    # Set encoding of the terminal to UTF-8 (Py 2.7.x; may not work under 3.x)
    out = codecs.getwriter("UTF-8")(sys.stdout)

    # Process input file
    with open(inputFile) as csvfile:
        reader = csv.reader(csvfile,quotechar='"')
        for row in reader:
            desc = row[0].decode("UTF-8", "strict")            
            url = row[1]

            # Check in wayback
            available, urlWayback, status, timestamp = checkURL(url)
            stringOut = '"' + desc + '"' + "," + unicode(available) + "," + urlWayback + "," + status + "," + timestamp

            # Output to stdout
            out.write(stringOut + "\n")


main()

