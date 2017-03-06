# You provide the tool with 2 lists. List A contains the webpages 
# that might have a link back to web pages in List B. The tool iterates
# through items in List A and checks if each item in List A contains 
# a link to any web page from List B.


import urllib
import http.client
import urllib.parse
import urllib.request
from urllib.error import URLError, HTTPError
import socket
from socket import timeout
import re
import time
import sys
import codecs
import string
from threading import Thread



# utf-8 safe

#if sys.stdout.encoding != 'utf-8':
#    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
#if sys.stderr.encoding != 'utf-8':
#    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# end of utf-8 safe

opener = urllib.request.FancyURLopener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

#socket.setdefaulttimeout(5)



# opening the files and reading data into varables


# links pointing from
f1 = open('/Users/slava.rybalka/Documents/Pyscripts/list-of-referring-pages.txt')
list_of_their_sites = f1.read().splitlines()
f1.close()

# links pointing to
f2 = open('/Users/slava.rybalka/Documents/Pyscripts/list-of-our-sites.txt')
list_of_our_sites = f2.read().splitlines()
f2.close()

total_entries = len(list_of_their_sites)

# build a dictionary were the referring pages are value[0]s and destination pages are value[1]s
backlinks = {}

elem_id = 0

while elem_id < total_entries:

    for entry in list_of_their_sites:
        #print(elem_id)
        #print(list_elem_counter)
        #backlinks[list_elem_counter] = [list_of_their_sites[list_elem_counter], list_of_our_sites[list_elem_counter]]
        backlinks[elem_id] = [list_of_their_sites[elem_id], list_of_our_sites[elem_id]]
        elem_id += 1
        #print(list_elem_counter)

#print(backlinks)

# setting the counters and lists
counter = 0
pages_with_links =[]
error_pages = []

###########
# Request #
###########

# getting the contents of the URL
def query_url(url): 
    url = "http://" + url.replace("http://",'').replace("https://",'') # sanitizing the URI

    request = opener.open(url)
    try:
        results = request.read()
        print(results)

    except ValueError as e:
        print('Error:', e)
        results = None
        pass
    
    return results



#############
# Execution #
#############



#print(list_of_our_sites)
#print(list_of_their_sites)


#print(len(list_of_our_sites))
number_of_referring_pages = len(list_of_their_sites)


for key, value in backlinks.items(): # iterate through all the sites that might contain a link back to us
    #sys.stdout.flush() # clean the buffer to allow terminal to update in real time
    counter += 1
    print("Processing", counter, 'out of', number_of_referring_pages)
    print(value[0])
    #print(list_limit)
    try:
        req = opener.open(value[0]) # open each website in the list, one by one
        results = req.read().decode('utf-8')
    
    
    
        if value[1] in results:
            print('!!! >>>>>>>>>>>>>>>>>>>           Found a link back from ' + value[0] + ' to our site: ', value[1])
            pages_with_links.append(value[0]) # if our website is found on their page, add their page to the list of pages linking back to us

    # error handling    
    except HTTPError as e:
        print('HTTP error:', e.code)
        error_pages.append(value[0])
        pass
    except URLError as e:
        print('We failed to reach a server:', e.reason)
        error_pages.append(value[0])
        pass
    except socket.timeout:
        print('socket timeout')
        error_pages.append(value[0])
        pass
    except http.client.BadStatusLine as e:
        print('HTTP error not recognized, error code not given')
        error_pages.append(value[0])
        pass
    except ValueError as e:
        print('Error:', e)
        error_pages.append(value[0])
        pass
    except AttributeError:
        print("AttributeError found, skipping")
        error_pages.append(value[0])
        pass
    except OSError as e:
        print("OSerror, skipping")
        error_pages.append(value[0])
        pass
    except urllib.error.URLError as e:
        error_pages.append(value[0])
        pass
    except http.client.IncompleteRead as e:
        error_pages.append(value[0])
        pass

for linking_page in pages_with_links: # iterate through the list of websites that have links back to us
    try:
        list_of_their_sites.remove(linking_page) # remove each linking page from the original list
    except:
        pass


print("\nTotal pages: ", len(backlinks))

print("\nPages with links: ", len(pages_with_links), "\n")
#print(pages_with_links)

print("\nPages with errors: ", len(error_pages), "\n")
#print(error_pages)  

print("\nPages without links: ", len(list_of_their_sites), "\n")
#print(list_of_their_sites)

