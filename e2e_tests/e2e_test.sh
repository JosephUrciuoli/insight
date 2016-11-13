#!/usr/bin/env bash

# Run an end to end test on two example text files checking their outputs for verification
python ./temp/src/antifraud.py ./tests/test-1-paymo-trans/paymo_input/batch_payment_test.txt ./tests/test-1-paymo-trans/paymo_input/stream_payment_test.txt ./tests/test-1-paymo-trans/paymo_output/output1.txt ./tests/test-1-paymo-trans/paymo_output/output2.txt ./tests/test-1-paymo-trans/paymo_output/output3.txt ./tests/test-1-paymo-trans/paymo_output/added_feature.txt
python ./verify_output.py
