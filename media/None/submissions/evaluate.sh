#!/bin/bash

cd $1
file = $2
g++ $file -o bashed_executable 2>/dev/null
timeout 5 ./bashed_executable 2>/dev/null 
if (( $? == 8 )); then
    echo $3,$5 >> $4.csv
else
    echo $3,0 >> $4.csv
fi
i = 3
while ((i <= $6))
do
  cd ..
  ((i++))
done