#!/bin/bash

mkdir ./retile
for i in *.jp2; do
no_ext=${i%.*};
output_dir="$PWD/retile/$no_ext/";
echo "$output_dir"

if [ -d $output_dir ]
then
  echo "$output_dir exists";
else
  echo "working on $i";
  mkdir $output_dir;
  gdal_retile.py -of JPEG -ps 1000 1000 -overlap 200 -csv $i.csv -targetDir $output_dir $i;
  echo "completed $i";
fi

done
