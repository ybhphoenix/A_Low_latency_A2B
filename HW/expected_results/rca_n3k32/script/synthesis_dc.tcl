

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
analyze -define SIM -format verilog ../src/ConvertAB_RCA_n3k32_1.v
analyze -define SIM -format verilog ../src/Expand1_n1o3k32.v
analyze -define SIM -format verilog ../src/Expand2_n2o3k32.v
analyze -define SIM -format verilog ../src/SecRCA_n3k32_1.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n3k32_0.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n3k32_1.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n3k32_2.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n3k32_3.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n3k32_4.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n3k32_5.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n3k32_6.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n3k32_7.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n3k32_8.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n3k32_9.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n3k32_10.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n3k32_11.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n3k32_12.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n3k32_13.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n3k32_14.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n3k32_15.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n3k32_16.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n3k32_17.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n3k32_18.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n3k32_19.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n3k32_20.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n3k32_21.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n3k32_22.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n3k32_23.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n3k32_24.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n3k32_25.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n3k32_26.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n3k32_27.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n3k32_28.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n3k32_29.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n3k32_30.v
analyze -define SIM -format verilog ../src/SecAnd_PINI1_n3k1_1.v
analyze -define SIM -format verilog ../src/ConvertAB_RCA_n2k32_1.v
analyze -define SIM -format verilog ../src/Expand1_n1o2k32.v
analyze -define SIM -format verilog ../src/Expand2_n1o2k32.v
analyze -define SIM -format verilog ../src/SecRCA_n2k32_1.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n2k32_0.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n2k32_1.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n2k32_2.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n2k32_3.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n2k32_4.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n2k32_5.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n2k32_6.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n2k32_7.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n2k32_8.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n2k32_9.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n2k32_10.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n2k32_11.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n2k32_12.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n2k32_13.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n2k32_14.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n2k32_15.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n2k32_16.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n2k32_17.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n2k32_18.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n2k32_19.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n2k32_20.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n2k32_21.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n2k32_22.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n2k32_23.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n2k32_24.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n2k32_25.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n2k32_26.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n2k32_27.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n2k32_28.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n2k32_29.v
analyze -define SIM -format verilog ../src/SecRCA_1b_n2k32_30.v
analyze -define SIM -format verilog ../src/SecAnd_PINI1_n2k1_1.v

elaborate ConvertAB_RCA_n3k32_1
current_design ConvertAB_RCA_n3k32_1
link
check_design -html check_design.html
set_operating_conditions -lib NangateOpenCellLibrary_typical


change_names -rules verilog -hier -verbose > report/ConvertAB_RCA_n3k32_1.change_name.before_compile
source -e -v ../sdc/ConvertAB_RCA_n3k32_1.sdc
change_names -rules verilog -hier -verbose > report/ConvertAB_RCA_n3k32_1.change_name.after_cons
check_timing
set_dont_touch_network [get_ports clk_i]
compile -exact_map -map_effort medium -area_effort medium
set_dont_touch [get_designs SecAnd_PINI1*]
ungroup -all -flatten
change_names -rules verilog -hierarchy


write -f ddc -hier -o db/ConvertAB_RCA_n3k32_1.ddc
write -f verilog -hier -o db/ConvertAB_RCA_n3k32_1.v
write_sdc  report/ConvertAB_RCA_n3k32_1.sdc
write_sdf  report/ConvertAB_RCA_n3k32_1.sdf


report_threshold_voltage_group > report/ConvertAB_RCA_n3k32_1.multi_vt
report_clock_gating -nosplit -ungated > report/ConvertAB_RCA_n3k32_1.clock_gating.rpt
report_clock -group > report/ConvertAB_RCA_n3k32_1.clk.rpt
report_clock -skew >> report/ConvertAB_RCA_n3k32_1.clk.rpt
all_registers -level_sensitive > report/ConvertAB_RCA_n3k32_1.latch.rpt
report_qor -significant_digits 3 > report/ConvertAB_RCA_n3k32_1.qor.rpt
report_timing -significant_digits 3 -trans -nets -delay max -max_paths 500 -sort_by group > report/ConvertAB_RCA_n3k32_1.report_timing
report_constraint -significant_digits 3 -all_violators -verbose > report/ConvertAB_RCA_n3k32_1.violation
report_area -hier > report/ConvertAB_RCA_n3k32_1.area.rpt
report_power -nosplit -verbose > report/ConvertAB_RCA_n3k32_1.power.rpt


exit