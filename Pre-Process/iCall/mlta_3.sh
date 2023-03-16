#! /bin/bash


cd ./mjs-issues-78
find . -name "*.res"  -type f -print | sed "s|^\./||" >> ../mlta_res_path.txt

