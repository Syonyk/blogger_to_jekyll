# Process comments (one per HTML file) into something that can flow into Discourse.

import re
import sys
import urllib
import os
from HTMLParser import HTMLParser

reload(sys)
sys.setdefaultencoding("utf-8")

htmlparser = HTMLParser()


for filename in sys.argv[1:]:
    with open(filename, 'r') as f:
      author = ''
      date = filename[:10]
      output_path = ''
      file = ''
      print("File: " + filename)

      in_header = False
      for line in f:

        if line == '---\n':
          in_header = not in_header
          continue;

        # Check for the blogger_orig line and write the redirect_from line as well as the title image.
        if in_header and line[:8] == 'author: ':
          author = line[8:].rstrip()
          #print("Found author: " , author);

        if in_header and line[:18] == 'blogger_orig_url: ':
          # Trim off to end of the first URL.
          output_path = line[45:]
          output_path = output_path[:output_path.find('?')]
          
          #print("Output path:" + output_path)
          file = open(output_path, "a")
          file.write(date)
          file.write(' by ')
          file.write(author)
          file.write('\n');
          
        if not in_header:
          file.write(htmlparser.unescape(line))

      # Out of for loop.
      file.write("\n\n----\n\n")
      file.close()

          # Otherwise, copy the line to output.
          #processed_file += line




