#!/bin/bash
#I should do this in Docer, but ...

PROG=main

export PYTHONPATH='$(pwd)'
export AFL_PYTHON_MODULE=$PROG

AFL_I_DONT_CARE_ABOUT_MISSING_CRASHES=1 AFL_SKIP_CPUFREQ=1 \
    afl-fuzz -t 200 -i $(pwd)/IN -o $(pwd)/OUT -x $(pwd)/dictionaries/json.dict $(pwd)/.jsoncpp_fuzzer

