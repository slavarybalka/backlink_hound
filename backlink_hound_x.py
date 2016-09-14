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

if sys.stdout.encoding != 'utf-8':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


opener = urllib.request.FancyURLopener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

socket.setdefaulttimeout(5)

f = open('/Users/slava.rybalka/Documents/Pyscripts/list_of_our_sites.txt')
list_of_our_sites = f.read().splitlines()
f.close()

f2 = open('/Users/slava.rybalka/Documents/Pyscripts/list_of_referring_sites_1000plus.txt')
#f2 = open('/Users/slava.rybalka/Documents/Pyscripts/sample_set.txt')

list_of_their_sites = f2.read().splitlines()
f2.close()

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


for webpage in list_of_their_sites: # iterate through all the sites that might contain a link back to us
    sys.stdout.flush() # clean the buffer to allow terminal to update in real time
    counter +=1
    print("Processing", counter, 'out of', number_of_referring_pages)
    print(webpage)

    try:
        req = opener.open(webpage) # open each website in the list, one by one
        results = req.read().decode('utf-8')
    
        
        for our_site in list_of_our_sites: # with their website retrieved, iterate through a list of our sites
            if our_site in results:
                print('>>>             Found a link back to our site: ', our_site)
                pages_with_links.append(webpage) # if our website is found on their page, add their page to the list of pages linking back to us

    # error handling    
    except HTTPError as e:
        print('HTTP error:', e.code)
        error_pages.append(webpage)
        pass
    except URLError as e:
        print('We failed to reach a server:', e.reason)
        error_pages.append(webpage)
        pass
    except socket.timeout:
        print('socket timeout')
        error_pages.append(webpage)
        pass
    except http.client.BadStatusLine as e:
        print('HTTP error not recognized, error code not given')
        error_pages.append(webpage)
        pass
    except ValueError as e:
        print('Error:', e)
        error_pages.append(webpage)
        pass
    except AttributeError:
        print("AttributeError found, skipping")
        error_pages.append(webpage)
        pass
    except OSError as e:
        print("OSerror, skipping")
        error_pages.append(webpage)
        pass
    except urllib.error.URLError as e:
        error_pages.append(webpage)
        pass
    except http.client.IncompleteRead as e:
        error_pages.append(webpage)
        pass

for linking_page in pages_with_links: # iterate through the list of websites that have links back to us
    try:
        list_of_their_sites.remove(linking_page) # remove each linking page from the original list
    except:
        pass
print(len(pages_with_links))
print(len(list_of_their_sites))

print("\nPages with errors: ", len(error_pages), "\n")

print(error_pages)  

print("\nPages without links: ", len(list_of_their_sites), "\n")

print(list_of_their_sites) 