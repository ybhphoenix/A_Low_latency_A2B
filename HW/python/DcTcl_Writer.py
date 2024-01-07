import datetime
import os
import sys

from FileList_Generator import File 



#################################################################################
 # class name       : DcTclWriter
 # description      : generate Design Compiler TCL file
 #    
 # function         : @add_tcl  : add tcl file to lib setup tcl file
 # function         : @add_sdc  : add SDC file to sdclist
 # function         : @add_vf   : add verilog file to list
 # function         : @set_list : set verilog file list to list
 # function         : @write    : wirte file
 #                
 # input            : @top      : the top name
 # input            : @root_path: the root path
 # input            : @name     : the tcl file name
 # returns          : no
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
class DcTclWriter:
    def __init__(self, top, root_path = "", name = "synthesis_dc", ):
        self.top                = top
        self.root_path          = root_path   
        self.name               = name             
        self.list               = []
        self.sdclist            = []
        self.lib_setup_tcl_file = []



    def add_tcl(self, file):
        self.lib_setup_tcl_file.append(file)



    def add_sdc(self, file):
        self.sdclist.append(file) 
    


    def add_vf(self, obj):
        if isinstance(obj, File):
            is_exist = 0
            for i in range(0,len(self.list)):
                if self.list[i].name == obj.name:
                    is_exist = 1
                    break
            if is_exist == int(0):
                self.list.append(obj)
        else:
            raise Exception("Invalid type!" + str(obj))



    def set_list(self, list):
        self.list = list



    def write(self, file=None):
        file = "{}.tcl".format(self.name)
        s = "\n\n"
        for i in range(0, len(self.lib_setup_tcl_file)):
            if self.root_path == "":
                s += "source -e -v ../script/{}\n".format(self.lib_setup_tcl_file[i])
            else:
                s += "source -e -v {}/work/script/{}\n".format(self.root_path, self.lib_setup_tcl_file[i])

        s += "\n"
        s += "set_host_options -max_cores 8\n"
        s += "set hdlin_check_no_latch true\n"
        s += "set verilogout_no_tri true\n"
        s += "set_app_var hdlin_reporting_level comprehensive\n"
        s += "set hdlin_infer_multibit default_all\n"
        s += "set do_operand_isolation true\n"
        s += "set enable_keep_signal true\n"
        s += "set hdlin_keep_signal_name \"user\"\n"
        s += "set lvt_ratio 2\n"
        s += "\n\n"
        for i in range(0, len(self.list)):
            if self.root_path == "":
                # s += "analyze -define TSMC_28N -format verilog ../src/{}.v\n".format(self.list[i].name)
                s += "analyze -define SIM -format verilog ../src/{}.v\n".format(self.list[i].name)
            else:
                # s += "analyze -define TSMC_28N -format verilog {}/work/src/{}.v\n".format(self.root_path, self.list[i].name)
                s += "analyze -define SIM -format verilog {}/work/src/{}.v\n".format(self.root_path, self.list[i].name)
        s += "\n"
        s += "elaborate {}\n".format(self.top)
        s += "current_design {}\n".format(self.top)
        #s += "set_max_area 0\n"
        s += "link\n"


        s += "check_design -html check_design.html\n"
        s += "uniquify"

        s += "set_operating_conditions -max sg0p81v125c -max_library tcbn28hpcplusbwpl2t30p140hvtssg0p8lv125c_CCs -analysis type_on_chip_variation\n"

        s += "\n\n"

        s += "change_names -rules verilog -hier -verbose > report/{}.change_name.before_compile\n".format(self.top)
        for i in range(0, len(self.sdclist)):
            if self.root_path == "":
                s += "source -e -v ../sdc/{}\n".format(self.sdclist[i])
            else:
                s += "source -e -v {}/work/sdc/{}\n".format(self.root_path, self.sdclist[i])
        s += "change_names -rules verilog -hier -verbose > report/{}.change_name.after_cons\n".format(self.top)
        s += "check_timing\n"
        s += "set_dont_touch_network [get_ports clk_i]\n"
        # s += "compile -exact_map -map_effort medium -area_effort medium -gate_clock\n"
        s += "compile -exact_map -map_effort medium -area_effort medium\n"
        # s += "compile -exact_map\n"

        s += "set_dont_touch [get_designs SecAnd_PINI1*]\n" 
        #s += "set_dont_touch [get_nets -hierarchical DONT_TOUCH_R_*]\n"  
        #s += "set_boundary_optimization [get_designs SecAnd_PINI1*] false\n"
        
        #s += "compile_ultra -no_autoungroup -gate_clock -retime\n"
        s += "ungroup -all -flatten\n"
        s += "change_names -rules verilog -hierarchy\n"
        s += "\n\n"

        s += "write -f ddc -hier -o db/{}.ddc\n".format(self.top)
        s += "write -f verilog -hier -o db/{}.v\n".format(self.top)
        s += "write_sdc  report/{}.sdc\n".format(self.top)
        s += "write_sdf  report/{}.sdf\n".format(self.top)
        s += "\n\n"
        s += "sizeof_collection [get_lib_cells */ND2D*]\n" 
        s += "get_lib_cells */ND2D*\n"       
        s += "get_attribute [get_lib_cells */ND2D*] area\n"
        s += "\n\n"
        s += "report_threshold_voltage_group > report/{}.multi_vt\n".format(self.top)
        s += "report_clock_gating -nosplit -ungated > report/{}.clock_gating.rpt\n".format(self.top)
        s += "report_clock -group > report/{}.clk.rpt\n".format(self.top)
        s += "report_clock -skew >> report/{}.clk.rpt\n".format(self.top)
        s += "all_registers -level_sensitive > report/{}.latch.rpt\n".format(self.top)                
        s += "report_qor -significant_digits 3 > report/{}.qor.rpt\n".format(self.top)
        s += "report_timing -significant_digits 3 -trans -nets -delay max -max_paths 500 -sort_by group > report/{}.report_timing\n".format(self.top)        
        s += "report_constraint -significant_digits 3 -all_violators -verbose > report/{}.violation\n".format(self.top)
        s += "report_area -hier > report/{}.area.rpt\n".format(self.top)
        s += "report_power -nosplit -verbose > report/{}.power.rpt\n".format(self.top)

        s += "\n\n"

        s += "exit"

        if file is None:
            return s
        else:
            fname = os.getcwd()
            fname += "/script/" + file
            if not os.path.exists('script'):
                os.mkdir('script')
            if not os.path.exists('syn'):
                os.mkdir('syn')
            if not os.path.exists('syn/report'):
                os.makedirs('syn/report')
            if not os.path.exists('syn/db'):
                os.makedirs('syn/db')
            f = open(fname,'w')
            f.write(s)

