
# Jekyll will import posts from Blogger, but they still contain image
# references to Blogger's CDN. This script:
# - Finds all image references in an imported blogger page
# - Downloads the images into the assets/ directory
# - Rewrites the page with the appropriate image link

import re
import sys
import urllib
import os

IMG_RE = re.compile('<img[^>]+src="(?P<src>[^"]+)"')
DATE_RE = re.compile('(?P<date>[0-9]+\-[0-9]+\-[0-9]+)')

try:
    os.mkdir('./processed/')
except:
    # Don't care.
    pass


for filename in sys.argv[1:]:
    date_prefix = DATE_RE.search(filename).group('date')
    with open(filename, 'r') as f:
        file_index = 0
        contents = f.read()
        for match in IMG_RE.finditer(contents):
            sourceurl = match.group('src')
            print('sourceurl: ' + sourceurl)
            if "rover.ebay" in sourceurl:
            	print('Ignoring eBay tracking pixel')
            	continue
            extstart = sourceurl.rfind('.')
            extension = sourceurl[extstart:]
            if "blogspot.com" in sourceurl:
                # This is blogger.  Download the /full/ size image.
                size_end = sourceurl.rfind('/')
                size_start = sourceurl.rfind('/', 0, size_end - 1)
                # Trim out the size, replace with 's0' for the full size image.
                imagename = sourceurl[size_end + 1:]
                sourceurl_full = sourceurl[:size_start] + '/s0' + sourceurl[size_end:]
    	    else:
    	        # Not blogger, just get the image name.
    	        size_end = sourceurl.rfind('/')
                imagename = sourceurl[size_end + 1:]
                sourceurl_full = sourceurl

            newfile = date_prefix + '-' + imagename

            file_index += 1
            print('{} => {}'.format(sourceurl_full, newfile))
            try:
                os.mkdir('../images/' + date_prefix)
            except:
                # Don't care.
                pass
            
            urllib.FancyURLopener().retrieve(sourceurl_full, '../images/' + date_prefix + '/' + newfile)
            contents = contents.replace(sourceurl, '{{ site.url }}/images/' + date_prefix + '/' + newfile)

    with open(filename, 'w') as f:
        f.write(contents)
        f.close()
        os.rename(filename, './processed/' + filename)
