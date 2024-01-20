Introduction
===

This artifact corresponds to the paper entitled "A Low-Latency High-Order Arithmetic to Boolean Masking Conversion".

The artifact includes our proposed CSA-based A2B (Algorithm 7) and, for comparison, RCA-based A2B ([BC22] in Table 1\~3) and KSA-based A2B ([CGTV15] in Table 1\~3). The software implementations are in the ./SW directory, while the hardware implementations are in the ./HW directory.

## Software Implementations

To get the benchmarks, run the python script run_benchmarks.py

$ python3 run_benchmarks.py

One should use Python 3.0.
The benchmark results are in the file bench_res.txt


To get the function tests, run the python script run_test.py

$ python3 run_test.py

One should use Python 3.0.
The test results are in the file test_res.txt


The script allows to pick the number of iterations, the bit width, the gcc compile optimization options, the masking orders that are benchmarked and also the type of PRNG used.\
When RNG is set to 0, the PRNG is disabled and always returns 0.\
When RNG is set to 1, a xorshift PRNG is used to sample 32-bit values.\
When RNG is set to 2, the rand() function is used to sample 32-bit values.

## Hardware Implementations

We provide RTL generation scripts located at ./HW/python that can generate hardware implementations with different security levels for different bit widths. The ./HW/lib contains basic gate implementations for Python to generate RTL. 

We can choose from different hardware platforms.\
If you want to use behavior level for this RTL, please define SIM in lib/lix_define.v.\
If you want to use Xilinx 7 Series Lut6 for this RTL, please define FPGA in lib/lix_define.v.\
If you want to use TSMC 28n lib for this RTL, please define TSMC_28N in lib/lix_define.v.\
By default, to use SIM for RTL.

when generating RTL and TB in the current directory, python3 Main_generator.py type shares width dumpon print_debug.


***Command Descriptions***

Option:\
type   	  = [SecA2B,ConvertAB,ConvertAB_RCA]\
shares 	  = [2:10]\
width 	  = [8:64]				  -- typical value : 8，13，16，24，32，64\
dumpon 	  = [0,1]                 -- fsdb dumpfile switch for test bench\
print_debug = [0,1]                 -- 1: print debug information, 0: keep silence

example1:
generate our CSA-based SecA2B with shares = 3, width = 32 , turn off fsdb dumpfile for Test Bench and turn off debug information\
$ python3 Main_generator.py SecA2B 3 32 0 0

example2:
generate ConvertAB [CGTV15] with shares = 3, width = 32 , turn off fsdb dumpfile for Test Bench and turn off debug information\
$ python3 Main_generator.py ConvertAB 3 32 0 0

example3:
generate ConvertAB_RCA [BC22] with shares = 3, width = 32 , turn off fsdb dumpfile for Test Bench and turn off debug information\
$ python3 Main_generator.py ConvertAB_RCA 3 32 0 0

We place the different 32-bit A2B conversions generated for hardware comparison in Tables 1 and 2 under the ./HW/rtl path.
