#! /bin/bash


cd ./mjs-issues-78
find . -name "*.bc"  -type f -print | sed "s|^\./||" >> ../address2.txt


while IFS= read -r line; do
    #/home/wu000380/Documents/static_analysis/crix/analyzer/build/lib/kanalyzer -sc ./libxml2_ef709ce2/$line
    /home/kefu/Documents/mlta/build/lib/kanalyzer ./$line &> $line.res
    echo $line.res>>../res_address.txt
done < ../address2.txt

