

# this is the manual for generating the RTL by python3

# Note:
#      1. If you want to use behavior level for this RTL, please define SIM in lib/lix_define.v
#      2. If you want to use Xilinx 7 Series Lut6 for this RTL, please define FPGA in lib/lix_define.v
#      3. If you want to use TSMC 28n lib for this RTL, please define TSMC_28N in lib/lix_define.v
#      By default, to use SIM for RTL

# generate RTL and TB in the current directory
python3 Main_generator.py type shares width dumpon print_debug


# description
# type   	  = [SecA2B,ConvertAB,ConvertAB_RCA]
# shares 	  = [2:10]
# width 	  = [8:64]				  -- typical value : 8，13，16，24，32，64
# dumpon 	  = [0,1]                 -- fsdb dumpfile switch for test bench
# print_debug = [0,1]                 -- 1: print debug information, 0: keep silence


# example1
# generate SecA2B with shares = 3, width = 32 , turn off fsdb dumpfile for Test Bench and turn off debug information
python3 Main_generator.py SecA2B 3 32 0 0

# example2
# generate ConvertAB with shares = 3, width = 32 , turn off fsdb dumpfile for Test Bench and turn off debug information
python3 Main_generator.py ConvertAB 3 32 0 0

# example3
# generate ConvertAB_RCA with shares = 3, width = 32 , turn off fsdb dumpfile for Test Bench and turn off debug information
python3 Main_generator.py ConvertAB_RCA 3 32 0 0

