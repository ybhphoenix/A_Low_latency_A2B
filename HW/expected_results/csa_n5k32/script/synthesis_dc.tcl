

source -e -v ../syn_lib/library_setup_dc.tcl
source -e -v ../syn_lib/dont_use.tcl

set_host_options -max_cores 8
set hdlin_check_no_latch true
set verilogout_no_tri true
set_app_var hdlin_reporting_level comprehensive
set hdlin_infer_multibit default_all
set do_operand_isolation true
set enable_keep_signal true
set hdlin_keep_signal_name "user"
set lvt_ratio 2


analyze -define SIM -format verilog ../src/../../lib/lix_define.v
analyze -define SIM -format verilog ../src/../../lib/lix_and.v
analyze -define SIM -format verilog ../src/../../lib/lix_not.v
analyze -define SIM -format verilog ../src/../../lib/lix_or.v
analyze -define SIM -format verilog ../src/../../lib/lix_reg.v
analyze -define SIM -format verilog ../src/../../lib/lix_shr0.v
analyze -define SIM -format verilog ../src/../../lib/lix_shr1.v
analyze -define SIM -format verilog ../src/../../lib/lix_xor.v
analyze -define SIM -format verilog ../src/SecCSATree_n5k32.v
analyze -define SIM -format verilog ../src/SecAnd_PINI1_n5k32_1.v
analyze -define SIM -format verilog ../src/SecCSA_n5k32.v
analyze -define SIM -format verilog ../src/SecCSATree_n4k32.v
analyze -define SIM -format verilog ../src/SecAnd_PINI1_n4k32_1.v
analyze -define SIM -format verilog ../src/SecCSA_n4k32.v
analyze -define SIM -format verilog ../src/SecCSATree_n3k32.v
analyze -define SIM -format verilog ../src/SecAnd_PINI1_n3k32_1.v
analyze -define SIM -format verilog ../src/SecCSA_n3k32.v
analyze -define SIM -format verilog ../src/SecAnd_PINI1_n5k32_0.v
analyze -define SIM -format verilog ../src/SecKSA_1l_n5k32.v
analyze -define SIM -format verilog ../src/SecKSA_n5k32_1.v
analyze -define SIM -format verilog ../src/SecA2B_n5k32_1.v

elaborate SecA2B_n5k32_1
current_design SecA2B_n5k32_1
link
check_design -html check_design.html
set_operating_conditions -lib NangateOpenCellLibrary_typical


change_names -rules verilog -hier -verbose > report/SecA2B_n5k32_1.change_name.before_compile
source -e -v ../sdc/SecA2B_n5k32_1.sdc
change_names -rules verilog -hier -verbose > report/SecA2B_n5k32_1.change_name.after_cons
check_timing
set_dont_touch_network [get_ports clk_i]
compile -exact_map -map_effort medium -area_effort medium
set_dont_touch [get_designs SecAnd_PINI1*]
ungroup -all -flatten
change_names -rules verilog -hierarchy


write -f ddc -hier -o db/SecA2B_n5k32_1.ddc
write -f verilog -hier -o db/SecA2B_n5k32_1.v
write_sdc  report/SecA2B_n5k32_1.sdc
write_sdf  report/SecA2B_n5k32_1.sdf


report_threshold_voltage_group > report/SecA2B_n5k32_1.multi_vt
report_clock_gating -nosplit -ungated > report/SecA2B_n5k32_1.clock_gating.rpt
report_clock -group > report/SecA2B_n5k32_1.clk.rpt
report_clock -skew >> report/SecA2B_n5k32_1.clk.rpt
all_registers -level_sensitive > report/SecA2B_n5k32_1.latch.rpt
report_qor -significant_digits 3 > report/SecA2B_n5k32_1.qor.rpt
report_timing -significant_digits 3 -trans -nets -delay max -max_paths 500 -sort_by group > report/SecA2B_n5k32_1.report_timing
report_constraint -significant_digits 3 -all_violators -verbose > report/SecA2B_n5k32_1.violation
report_area -hier > report/SecA2B_n5k32_1.area.rpt
report_power -nosplit -verbose > report/SecA2B_n5k32_1.power.rpt


exit