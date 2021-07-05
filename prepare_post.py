# Process ![blah](../images/2020-10-10/2020-10-10-blogger_one_image.png)
# into {% picture /images/2020-10-10/2020-10-10-blogger_one_image.png %}
# Create thumbnail and header image at 600px and 90% quality with header material.
# You'll want to call this from the root of the blog directory...

import re
import sys
import urllib
import os

quality = "80"
geometry = "800x800"
size = "800"

for filename in sys.argv[1:]:
    with open(filename, 'r') as f:
        processed_file = ''
        in_header = False
        for line in f:
            if line == '---\n':
                in_header = not in_header

            # Read the image line.  Create a thumbnail.  Add the front matter.
            if in_header and line[:7] == 'image: ':
                image_path = line[7:].rstrip()
                image_prefix = image_path[:image_path.rfind('.')]
                image_suffix = image_path[image_path.rfind('.'):]
                image_thumbnail = image_prefix + "-" + size + image_suffix
                print("Path: " + image_path + "  Prefix: " + image_prefix + "  Suffix: " + image_suffix)
                os.system("convert -geometry " + geometry + " -quality " + quality + " ./" + image_path + " ./" + image_thumbnail)
                processed_file += line
                processed_file += 'image-thumbnail: ' + image_thumbnail + "\n"
                continue
            
            # Ignore any previous image-thumbnail headers.
            if in_header and line[:17] == 'image-thumbnail: ':
                continue

            # Rewrite image lines - and remove any ../ prefix.
            if line[:2] == '![':
	    	image_start = line.find('images')
	    	image_end = line.find(')')
	    	image = line[image_start:image_end]
	    	processed_file += '{% picture ' + image + ' %}\n<br/>\n'
	    	continue

            # Otherwise, copy the line to output.
            processed_file += line

    with open(filename, 'w') as f:
        f.write(processed_file)
        f.close()




