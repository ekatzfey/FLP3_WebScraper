#
# This is a script to collect the weekly rental rates from all properties at www.southernresorts.com
#
import requests
import time
import datetime

# Function to format the date appropriatelly for the HTTP POST
def datestr( d ):
    return str(d.month).zfill(2) + '/' + \
        str(d.day).zfill(2) + '/' + \
        str(d.year)

# Set per-page to some realy big number. If there are less than that it will return all of them.
payload = {'per-page': '5000', 'sort-order': 'bedrooms-lh', 'listpage': '1', 'viewtype': 'page'}

# This gets the top level website populated with all of the properties
r = requests.post('http://www.southernresorts.com/bre/listproperties/', payload )

links = []
if r.status_code != 200:
    print "Got bad status #1: " + str(r.status_code)
else:
    lines = r.text.splitlines()
    for line in lines:
        # Collect all of the links to the individual properties
        if (line.find('<a href=\"http://www.southernresorts.com/bre/properties/') != -1) and \
            (line.find('<div') == -1) and \
            (line.find('</a') != -1):
            links.append( line.split('\"')[1] )

looper = len(links)
print "There are " + str(looper) + " properties listed"

# Loop through each property
for x in range(0, looper):
    
    # Request the property page
    r = requests.get(links[x])

    tag = ""

    if r.status_code != 200:
        print "Got bad status #2: " + str(r.status_code)
    else:
        lines = r.text.splitlines()
        for line in lines:
            # Find the special property ID that can be used to query the rate
            if line.find('var realPropId') != -1:
                tag = line.split('\"')[1]
                print str(x+1) + ". Property ID: " + tag

                # Set the start date to be the next Saturday
                # TODO: Make this an input parameter
                d = datetime.date(2016, 2, 13)

                # We have to loop through each week until we find one that is available
                # because if it isn't available it won't give us the rental rate
                for y in range (0,52):
                    start_date = datestr(d)
                    end_date = datestr(d + datetime.timedelta(days=7))

                    r = requests.post('http://www.southernresorts.com/bre/jax/PropAvail2.php', \
                                         {'pid': tag, 'ci': start_date, 'co': end_date, \
                                            'ti': 'false', 'tid': 'false'})

                    if r.status_code == 200:
                        # Grab the rate if it is available, otherwise we'll try the next week
                        chunks = r.text.splitlines()
                        flds = chunks[0].split('\"')
                        available = flds[2][1:-1]
                        #print "Available: " + available
                        if available == 'true':
                            print "From " + start_date + " to " + end_date + " Rate is $" \
                                + flds[5]
                            break
                    #else:
                        #print "Got bad status #3: " + str(r.status_code)

                    d = d + datetime.timedelta(days=7)


