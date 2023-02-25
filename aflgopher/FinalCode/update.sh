mkdir $IP_DIR/update

counter= 0

for file in `ls out/ef709ce2/queue`
do
        let counter = counter +1
        cat /dev/null>$AFLGO_PROFILER_FILE
        $AFLGO/xmllint --valid --recover out/ef709ce2/queue/$file
        cp $AFLGO_PROFILER_FILE $IP_DIR/update/$counter
done



#python3 CG_phase/prediction.py -increment=True #incremental learning to update
#$AFLGO/scripts/gen_distance_fast.py $SUBJECT $TMP_DIR xmllint
#rm -rf BB_result.txt
#python3 assign_feasibility.py #get the distance table (the inputs are 'BBtable.txt' and 'distance.cfg.txt')
