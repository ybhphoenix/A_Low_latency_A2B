create_clock -period 0.180 [get_ports clk_i] -name clock0
set_clock_uncertainty -setup 0.018 [get_clocks clock0]

