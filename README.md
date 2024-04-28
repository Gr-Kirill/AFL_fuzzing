### Task:
#### - Need from the fuzzbench project https://github.com/google/fuzzbench take the benchmark jsoncpp_jsoncpp_fuzzer and get it (target).
The collected binary (target), which needs to be profiled, accepts data of a certain json format as input.

#### - It is necessary to train a neural network that will generate a high-quality corpus of input data in this format.
I.e., the input files must match the format that the target accepts as input.

#### - Write and apply a custom mutation that will use a neural network to generate input data.
#### - This target needs to be profiled with an AFL++ fuzzer.
You need to run 2+ afl-fuzz processes and ensure synchronization between them.

### Solution:

#### - Start fuzzing using mutation
* export PYTHONPATH='./src'
* export AFL_PYTHON_MODULE=main


#### - Start fuzzing using a neural network

* export PYTHONPATH='./src'
* export AFL_PYTHON_MODULE=main_model

### - Fuzzing start:
### afl-fuzz -t 200 -i ./IN -o ./OUT -x ./dictionaries/json.dict ./build/.jsoncpp_fuzzer

###### If necessary: AFL_I_DONT_CARE_ABOUT_MISSING_CRASHES=1 AFL_SKIP_CPUFREQ=1