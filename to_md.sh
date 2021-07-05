#!/bin/bash

dir=`pwd`
cd /tmp
for var in "$@"
do
  split_num=`grep -n '\-\-\-' $dir/$var | tail -n 1 | cut -d':' -f1`
  let split_num+=1;
  csplit "$dir/$var" $split_num
  html2md -i xx01 -o out.md
  new_filename=${var/.html/.md}
  cat xx00 out.md > "$dir/$new_filename"
  rm "$dir/$var"
done
