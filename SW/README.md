
To get the benchmarks, run the python script run_benchmarks.py

$ python run_benchmarks.py

One should use Python 3.0.
The benchmark results are in the file bench_res.txt

The script allows to pick the number of iterations, the masking orders that are benchmarked and also the type of PRNG used.
When RNG is set to 0, the PRNG is disabled and always returns 0.
When RNG is set to 1, a xorshift PRNG is used to sample 32-bit values.
When RNG is set to 2, the rand() function is used to sample 32-bit values.

The script runs the benchmarks for all the performance results of Section 10. To disable some of them, one can simply comment
the corresponding line in the main function of benchmarks.c.

To replicate the table counting the number of calls to the PRNG: define the macro COUNT in random.h and run the script. Number
of iterations and RNG are irrelevant here. 

The main.c file performs some correctness tests for the benchmarked functions. Those tests can be found in test.c. The benchmark
script does not run those tests.
To manually run them, set the desired masking order in gadget.h and: 
 - make
 - ./main


