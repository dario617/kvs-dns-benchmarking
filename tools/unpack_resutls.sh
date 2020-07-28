#!/usr/bin/env bash

#
# Unpack all the results tar files to folders
# 
results_folder=$1
cd $results_folder
echo "Working on $( pwd ) ..."
for sub_test in $(ls); do
  cd $sub_test
  # Ignore mem profile and times
  echo $sub_test > tmp.log
  grep -E "mem-|times-" tmp.log
  skip=$?
  if [ $skip -eq "0" ]; then
    echo "Skipping test"
    rm tmp.log
    cd ..
    continue
  fi
    
  for test in $(ls); do
    echo $test > tmp.log
    grep -e ".log" tmp.log
    skip=$?
    [[ $skip -eq "0" ]] && echo "Skipping file" && continue
    # Create name for folder
    extracted_folder=$( sed 's/.tar.gz//' tmp.log )
    # Create folder
    mkdir -p $extracted_folder
    # Unpack
    tar -xf $test --strip 1 -C $extracted_folder
    # Clear folder
    rm $test
  done
  rm tmp.log
  cd ..
done
echo "Extracted tar files"