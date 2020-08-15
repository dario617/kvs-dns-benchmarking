
if [ $1 == "reduce" ]; then
  head -n $2 dataset.txt > tmp.txt
  mv tmp.txt dataset.txt
else
  grep -P "IN\tA|HINFO|TXT\t" dns-rr.txt > dataset.txt
fi