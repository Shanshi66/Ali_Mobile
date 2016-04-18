#! /bin/bash
echo "************************"
echo "Generate Training Set"
echo "************************"
python feature_extract.py 7
python merge_training_set.py
python sampling.py 7 10
python sampling.py 7 20
