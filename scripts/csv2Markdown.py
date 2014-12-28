#
# USAGE: python csv2Markdown.py <inputFile> 
#
#
# Published as open source software under the Apache license:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#

import sys
import codecs
import csv


def main():
    
    if len(sys.argv) == 1:
        sys.stderr.write("USAGE: python csv2Markdown.py <inputFile> \n")
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
            urlWayback = row[3]

            if urlWayback != "":
                urlWaybackLink = '<' + urlWayback + '>'
            else:
                urlWaybackLink = ''

            stringOut = '|[' + desc + '](' + url + ')|' + urlWaybackLink + '|'

            # Output to stdout
            out.write(stringOut + "\n")


main()

