##TODO: get address.txt (get the C files)
#python3 if_extraction.py
#TODO: get the 'data.xls' from FU
# Step1: Get the three categories data (global, function, argument)
python3 extract_data.py
# Step2: Convert the text version of each categories (global, function, argument) to vector (word2vec)
python3 word2vec.py -category='function'
python3 word2vec.py -category='argument'
python3 word2vec.py -category='global'
# Step3: Get the clusters for each categories
python3 DBSCAN.py -category='function'
python3 DBSCAN.py -category='argument'
python3 DBSCAN.py -category='global'
# Step4: Assign the group into 'data.xls'
python3 cluster2xls.py
# Step5: Extract the IF with clusters of categories form 'data.xls'
python3 extract_if.py
# Step6: Convert IF data to vector (need parameter: number of cluster of each categories)
#        Have to get the result from Step3
python3 if2vec.py -global_number=96 -function_number=197 -argument_number=614
# Step7: Get the clusters for IF statement
python3 if_grouping.py
# Step8: Assign the probability to the 'Final IF.xls' file
python3 assgn_prob.py