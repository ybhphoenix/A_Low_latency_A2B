set CLK_PERIOD 0.180
create_clock -period $CLK_PERIOD [get_ports clk_i] -name clock0
set_clock_uncertainty -setup [expr $CLK_PERIOD*0.100] [get_clocks clock0]

