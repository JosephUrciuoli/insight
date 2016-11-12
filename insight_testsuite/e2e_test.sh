#!/usr/bin/env bash

# Run an end to end test on two example text files checking their outputs for verification
python ./temp/src/antifraud.py ./tests/test-2-paymo-trans/paymo_input/batch_payment.txt ./tests/test-2-paymo-trans/paymo_input/stream_payment.txt ./tests/test-2-paymo-trans/paymo_output/output1.txt ./tests/test-2-paymo-trans/paymo_output/output2.txt ./tests/test-2-paymo-trans/paymo_output/output3.txt ./tests/test-2-paymo-trans/paymo_output/added_feature.txt
