#!/bin/bash

# FILL THESE OUT
PYTHON_SCRIPT=...

# set up venv and talib library paths
source bin/activate
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

# make results folder if it doesn't exist
RESULTS_FOLDER="results"
mkdir $RESULTS_FOLDER

# make a folder for the current time
OUTPUT_FOLDER="$RESULTS_FOLDER/$(date +%d)th-$(date +%T)"
echo "saving output in: $OUTPUT_FOLDER"
mkdir $OUTPUT_FOLDER

OUTPUT_NAME="output.txt"
OUTPUT_PATH="$OUTPUT_FOLDER/$OUTPUT_NAME"

touch $OUTPUT_PATH

# the number of configuations is the sum of the first n triangle numbers
NUM_CONFIGS=... # num total configs here (optional)

NUM_THREADS=... # how many threads in a batch: 1 thread = 1 instance of py3
NUM_BATCHES=$((($NUM_CONFIGS+$NUM_THREADS-1)/$NUM_THREADS)) # ceil(x/y)

echo "$NUM_BATCHES batches and $NUM_CONFIGS configurations to search..."
echo "using $NUM_THREADS threads"
echo ""
echo "SIGKILL the program to quit (don't cntrl+c)"
echo ""
echo "running the program and generating results"

COUNT=1
for PARAM3 in $(seq low high)
do
	for PARAM2 in $(seq low high)
	do
		for PARAM1 in $(seq low high)
		do
			# uses temp files to store intermediate results
			FILENAME=$(printf "%02d-%02d-%02d" $PARAM1 $PARAM2 $PARAM3)
			FILEPATH="$OUTPUT_FOLDER/$FILENAME"

			# ceil(count/6)
			BATCH_COUNT=$((($COUNT+$NUM_THREADS-1)/$NUM_THREADS))

			# run the program and output to a file
			python3 $PYTHON_SCRIPT $PARAM1 $PARAM2 $PARAM3 > $FILEPATH &

			if [[ $(( COUNT % NUM_THREADS )) == 0 ]]; then
				echo -en $(printf "%3d/%3d\r" $BATCH_COUNT $NUM_BATCHES)
				sleep 1
				wait
			fi

			# iterate count
			COUNT=$(($COUNT+1))
		done
	done
done

# do post-processing here

echo "removing temporary files"

rm $OUTPUT_FOLDER/[0-9]*

spd-say "script finished"

# 29 past