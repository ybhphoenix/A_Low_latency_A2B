Introduction
===

This artifact corresponds to the paper entitled "A Low-Latency High-Order Arithmetic to Boolean Masking Conversion".

The artifact includes our proposed CSA-based A2B (Algorithm 7) and, for comparison, RCA-based A2B ([BC22] in Table 1\~3) and KSA-based A2B ([CGTV15] in Table 1\~3). The software implementations are in the ./SW directory, while the hardware implementations are in the ./HW directory.

Some key directories are shown below.

```
|--HW/                ## hardware implementations
  |--lib/             ## basic gate implementations for Python script to generate RTL
  |--python/          ## scripts for RTL generation
    |--Main_Generator.py ## Run this script to generate the specified parameter RTL
    |--syn_lib/        ## scripts to setup the path to the standard cell library
  |--expected_results/             ## generated rtl for reference
    |--csa_n3k32/      ## expected generation for CSA-based A2B rtl with 3 shares and 32 bit width
    |--csa_n4k32/      ## expected generation for CSA-based A2B rtl with 4 shares and 32 bit width
    |--csa_n5k32/      ## expected generation for CSA-based A2B rtl with 5 shares and 32 bit width
    |--ksa_n3k32/      ## expected generation for KSA-based A2B rtl with 3 shares and 32 bit width
    |--ksa_n4k32/      ## expected generation for KSA-based A2B rtl with 4 shares and 32 bit width
    |--ksa_n5k32/      ## expected generation for KSA-based A2B rtl with 5 shares and 32 bit width
    |--rca_n3k32/      ## expected generation for RCA-based A2B rtl with 3 shares and 32 bit width
    |--rca_n4k32/      ## expected generation for RCA-based A2B rtl with 4 shares and 32 bit width
    |--rca_n5k32/      ## expected generation for RCA-based A2B rtl with 5 shares and 32 bit width
    |--lib/            ## Same as a /HW/lib, copied here as part of the source code to facilitate direct synthesis
|--SW/                ## software simulation environment
  |--convab.c         ## main source c code of CSA-based A2B, RCA-based A2B ([BC22]) and KSA-based A2B ([CGTV15])
  |--cpucycles.c      ## cpucycles function to access system counter for benchmarking
  |--Masking.c        ## functions to generate arithmetic or Boolean shares
  |--random.c         ## different random function to generate random number
  |--run_benchmarks.py ## python script for benchmarks
  |--run_test.py       ## python script for function tests

|--README.md          ## source code introduction and basic usage
```

## Software Implementations
We provide c source code for different A2B conversion shceme and python scripts for testing.

Using Python 3.

### Function Test
To get the function tests, run the python script run_test.py by commands:
```
$ cd ./SW
$ python3 run_test.py
```

The test results **test_res.txt** will be generated in current directory. \
**test_res_ref.txt** is expected results for reference.

### Benchmarks
To get the benchmarks, run the python script run_benchmarks.py by commands:
```
$ cd ./SW
$ python3 run_benchmarks.py
```
The benchmark results **bench_res.txt** will be generated in current directory. \
**bench_res_ref.txt** is expected results with default gcc compile optimization options -O0 for reference.\
**bench_res_o2_ref.txt** is expected results with gcc compile optimization options -O0 for reference.\
Benchmarking results are cpu run clock cycles and vary per run. This paper uses the average of 1 million runs as the results on an Intel(R) Core(TM) i5-1135G7 @ 2.40GHz CPU platform, but the data still fluctuates within a small range.

### Parameters Setting
The script allows to pick the number of iterations, the bit width, the gcc compile optimization options, the masking orders that are benchmarked and also the type of PRNG used.

run_test.py and run_benchmarks.py can change the number of iterations by setting `ITERATIONS` parameter, and change the bit width by modify `width` range and `i` range as below.
```
for width in range(8, 33, 8): #bit width range and step
for i in range(1, MAX_ORDER+1): #security order range
```

Optimization compilation options can be changed in the **Makefile** file by changing the `-O0` option in the following command.
```
gcc  -Wall -O0 -march=native $(SOURCES) $(SOURCES_BENCH) $(MACROB) -lm -o bench 
```

Different random number patterns can be selected by setting the `RNG` parameter in the **Makefile** file.\
When RNG is set to 0, the PRNG is disabled and always returns 0.\
When RNG is set to 1, a xorshift PRNG is used to sample 32-bit values.\
When RNG is set to 2, the rand() function is used to sample 32-bit values.

## Hardware Implementations

We provide RTL generation scripts Main_generator.py located at ./HW/python that can generate hardware implementations with different security levels for different bit widths. The ./HW/lib contains basic gate implementations for Python to generate RTL. 

We can choose from different hardware platforms.\
If you want to use behavior level for this RTL, please define SIM in ./HW/lib/lix_define.v.\
If you want to use Xilinx 7 Series Lut6 for this RTL, please define FPGA in ./HW/lib/lix_define.v.\
If you want to use TSMC 28nm standard cell for this RTL, please define TSMC_28N in ./HW/lib/lix_define.v.\
If you want to use Nangate 45nm standard cell for this RTL, please define LIB_45NM in lib/lix_define.v.\
By default, use SIM for RTL. SIM is synthesizable under any process library, and the specific implementations under different ifdefs are giving a possible implementation based on primitive for a specific process.\
For fair comparison and generalizability, all results in the paper were generated by using SIM.

### RTL generation command

One should use Python3 and install package imported in ./HW/python/Yaml_Loader.py by command:
```
pip install PyYAML==5.3.1
```
The version of PyYAML package we are using is 5.3.1 as shown in command.

Use the following command to generate an RTL with the specified parameters:
```
$ cd ./HW/python
$ python3 Main_generator.py [type] [shares] [width] [dumpon] [print_debug]
```
The commands `type` `shares` `width` `dumpon` `print_debug` are all adjustable options.

***Option Descriptions***

Option:\
`type`   	  = [SecA2B,ConvertAB,ConvertAB_RCA] \
--SecA2B:CSA-based A2B (Algorithm 7); ConvertAB: KSA-based A2B ([CGTV15] in Table 1\~3); ConvertAB_RCA:RCA-based A2B ([BC22] in Table 1\~3)\
`shares` 	  = [2:10] \
--number of shares\
`width` 	  = [8:64] \
-- Converting Variable Bitwidths, typical value : 8，13，16，24，32，64\
`dumpon` 	  = [0,1]  \
-- fsdb dumpfile switch for test bench\
`print_debug` = [0,1] \
-- For code debugging, set to 0 when used

* command example1:
generate our CSA-based SecA2B with shares = 3, width = 32 , turn off fsdb dumpfile for Test Bench and turn off debug information.
```
$ cd ./HW/python
$ python3 Main_generator.py SecA2B 3 32 0 0
```

* command example2:
generate ConvertAB [CGTV15] with shares = 3, width = 32 , turn off fsdb dumpfile for Test Bench and turn off debug information.
```
$ cd ./HW/python
$ python3 Main_generator.py ConvertAB 3 32 0 0
```

 * command example3:
generate ConvertAB_RCA [BC22] with shares = 3, width = 32 , turn off fsdb dumpfile for Test Bench and turn off debug information.
```
$ cd ./HW/python
$ python3 Main_generator.py ConvertAB_RCA 3 32 0 0
```
### Command results
A successful run of command will generate the following directory in the current directory ./HW/python:
```
|--script/  ##script for DC synthesis
|--sdc/     ##timing constrians for DC synthesis
|--src/     ##rtl code except 
|--syn/     ##folder reserved for synthesis with empty contents
|--tb/      ##testbench for rtl simulation
```
We recommend using the command Example 1 to test whether it runs properly and ./HW/expected_results/csa_n3k32/ provides the full reference output.

We place the different 32-bit A2B conversions generated for hardware comparison in our paper under the ./HW/expected_results path. It can also be used as a expected output.

* expected output rtl of command example1: \
The contents of the output folder ./HW/python/src in example 1 above should be the same as ./HW/expected_results/csa_n3k32/src.

* expected output rtl of command example2: \
The contents of the output folder ./HW/python/src in example 2 above should be the same as ./HW/expected_results/ksa_n3k32/src.

* expected output rtl of command example3: \
The contents of the output folder ./HW/python/src in example 3 above should be the same as ./HW/expected_results/rca_n3k32/src.

### Synthesis flow

One should use Design Compiler Version P-2019.03 for linux64.

***Library setup***\
A standard cell library is required in the liberty (.lib) format. The following Open Libraries can be used:
* Nangate45 - https://github.com/The-OpenROAD-Project/OpenROAD-flow/tree/master/flow/platforms/nangate45

Modify the ./HW/python/syn_lib/library_setup_dc.tcl script to setup the path to the library.

***Synthesis***\
After running RTL generation command, we can run the following command in the current directory ./HW/python for synthesis:
```
$ cd ./syn
$ dc_shell -f ../script/synthesis_dc.tcl
```
We can adjust the `CLK_PERIOD` in the timing constraints file at ./HW/python/sdc to avoid timing violations.

Or you can use our generated rtl code under the expected_results path for direct synthesis. Take CSA-based A2B rtl with 3 shares and 32 bit width as an example. Modify the ./HW/expected_results/csa_n3k32/syn_lib/library_setup_dc.tcl script to setup the path to the library, and use the following command:
```
$ cd ./HW/expected_results/csa_n3k32/syn
$ dc_shell -f ../script/synthesis_dc.tcl
```

***Reference results***\
As shown in Table below, we give the synthesized results under the open source process library Nangate45 as a reference.

![ ](https://github.com/ybhphoenix/A_Low_latency_A2B/blob/main/Nangate_syn_redults.png)
