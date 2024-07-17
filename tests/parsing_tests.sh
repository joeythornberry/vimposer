#/bin/bash
echo
echo TESTING QUANTIZED DELTA TIMES
python -m tests.quantized_delta_times
echo DONE WITH QUANTIZED DELTA TIMES
echo 
echo TESTING UNQUANTIZED DELTA TIMES
python -m tests.unquantized_delta_times
echo DONE WITH UNQUANTIZED DELTA TIMES
echo
echo TESTING QUANTIZED TRIPLETS 
python -m tests.quantized_triplets
echo DONE WITH QUANTIZED TRIPLETS
echo
echo TESTING UNQUANTIZED TRIPLETS 
python -m tests.unquantized_triplets
echo DONE WITH UNQUANTIZED TRIPLETS
echo
