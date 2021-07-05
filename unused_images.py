# Looks for unused images in the image directory.
# run as: python _scripts/unused_images.py _posts/* _drafts/*
# Emits unused images.

import re
import sys
import urllib
import os

images = []

for filename in sys.argv[1:]:
    with open(filename, 'r') as f:
    	#contents = f.read()
    	first_image = ''
    	
    	# Loop through and find the first image line.
        for line in f:
	    if line[:5] == '[![](':
	    	image_start = line.find('}}')
	    	image_end = line.find(')]')
	    	first_image = line[image_start + 2:image_end]
	    	print('First Image: ' + first_image)
	    	break

        # Now reprocess the file.
        f.seek(0)
        processed_file = ''
        in_header = False
        for line in f:
            if line == '---\n':
                in_header = not in_header

            # Check for the blogger_orig line and write the redirect_from line as well as the title image.
            if in_header and line[:17] == 'blogger_orig_url:':
                processed_file += 'redirect_from: \n - '
                processed_file += line[18:].replace('https://syonyk.blogspot.com', '')
                processed_file += 'image: ' + first_image + '\n'

            # Rewrite image lines - do NOT copy the original in.
            if line[:5] == '[![](':
	    	image_start = line.find('}}')
	    	image_end = line.find(')]')
	    	image = line[image_start + 2:image_end]
	    	processed_file += '{% picture ' + image + ' %}\n<br/>\n'
	    	continue

            # Otherwise, copy the line to output.
            processed_file += line

    with open(filename, 'w') as f:
        f.write(processed_file)
        f.close()
