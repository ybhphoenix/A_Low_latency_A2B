To get the benchmarks, run the python script run_benchmarks.py

$ python3 run_benchmarks.py

One should use Python 3.0.
The benchmark results are in the file bench_res.txt


To get the function tests, run the python script run_test.py

$ python3 run_test.py

One should use Python 3.0.
The test results are in the file test_res.txt


The script allows to pick the number of iterations, the bit width, the gcc compile optimization options, the masking orders that are benchmarked and also the type of PRNG used.
When RNG is set to 0, the PRNG is disabled and always returns 0.
When RNG is set to 1, a xorshift PRNG is used to sample 32-bit values.
When RNG is set to 2, the rand() function is used to sample 32-bit values.
