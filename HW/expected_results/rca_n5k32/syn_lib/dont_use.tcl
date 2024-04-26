
foreach lib_i $target_std_lib_name {
   set_dont_use [get_lib_cells -quiet $lib_i/CLK*]
   set_dont_use [get_lib_cells -quiet $lib_i/S*]
   set_dont_use [get_lib_cells -quiet $lib_i/DL*]
}

remove_attribute [get_lib_cells -quiet $lib_i/CLKG*] dont_use