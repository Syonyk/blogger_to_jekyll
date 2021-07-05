#!/bin/bash

git pull
JEKYLL_ENV=production bundle exec jekyll build -V
#cd _site
#gsutil -m rsync -r generated gs://your-bucket-here/generated
#gsutil -m rsync -r images gs://your-bucket-here/images
#gsutil -m rsync -r -d -j html . gs://your-bucket-here/

rsync -avrz --progress _site/generated yourserver:yourblog/
rsync -avrz --progress _site/images yourserver:yourblog/
rsync -avrz --progress _site/* yourserver:yourblog

