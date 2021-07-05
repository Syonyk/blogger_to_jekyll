# Process Blogger links into Jekyll links.
# Relies on blogger_orig_url to create a lookup, then replaces any blog links
# that match with the new link.
# Does NOT rewrite tag links - I changed those manually and so will do them by hand.


import re
import sys
import urllib
import os

links_to_filenames = {}

for filename in sys.argv[1:]:
    with open(filename, 'r') as f:
    	# Loop through and find the blogger_orig_url line.
        for line in f:
	    if line[:17] == 'blogger_orig_url:':
	    	orig_url = line[18:]
	    	print('Orig URL=' + orig_url.rstrip())
	    	print('Filename:' + os.path.splitext(filename)[0])
	    	links_to_filenames[orig_url.rstrip()] = '{% post_url ' + os.path.splitext(filename)[0] + ' %}'
	    	links_to_filenames[orig_url.rstrip().replace('https://', 'http://')] = '{% post_url ' + os.path.splitext(filename)[0] + ' %}'
	    	break

for key in links_to_filenames.keys():
    print(key + " => " + links_to_filenames[key])

# Now, process the files.  For each link, rewrite it with the proper Jekyll string.
# {% post_url 2010-07-21-name-of-post %}

for filename in sys.argv[1:]:
    processed_file = ''
    with open(filename, 'r') as f:
    	# Loop through and find the blogger_orig_url line.
        for line in f:
            # Ignore blogger_orig_url.
	    if line[:17] == 'blogger_orig_url:':
	        processed_file += line
	        continue
	    # Match http and https.
            if "://syonyk.blogspot.com/" in line:
                print("Line matches: " + line)
                for key in links_to_filenames.keys():
                    line = line.replace(key, links_to_filenames[key])
                print("New line: " + line)
            
            processed_file += line


    with open(filename, 'w') as f:
        f.write(processed_file)
        f.close()




