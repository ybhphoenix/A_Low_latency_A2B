import datetime
import os
import sys



#################################################################################
 # class name       : LintTclWriter
 # description      : generate spyglass Lint TCL file
 #    
 # function         : @add_rtl_flist      : add rtl file list
 # function         : @add_vhdl_file      : add vhdl file
 # function         : @add_verilog_file   : add verilog file
 # function         : @add_sv_file        : add system verilog file
 # function         : @add_rules          : add rules
 # function         : @add_swl_waiver     : add swl waiver file
 # function         : @add_awl_waiver     : add awl waiver file
 # function         : @add_sdc_file       : add SDC constraint file
 # function         : @write              : wirte file
 #                
 # input            : @module_name        : the module name
 # input            : @root_path          : the root path
 # input            : @name               : the tcl file name
 # returns          : no
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
class LintTclWriter:
    def __init__(self, module_name = "", root_path = "", name = "spyglass_lint"):
        self.module_name        = module_name
        self.root_path          = root_path
        self.name               = name
        self.rtl_flist          = []
        self.vhdl_list          = []
        self.verilog_list       = []
        self.sv_list            = []    
        self.rules_flist        = []
        self.swl_waiver_flist   = []
        self.awl_waiver_flist   = []
        self.sdc_flist          = []

    def add_rtl_flist(self, file_list):
        self.rtl_flist.append(file_list)

    def add_vhdl_file(self, file):
        self.vhdl_list.append(file)

    def add_verilog_file(self, file):
        self.verilog_list.append(file)

    def add_sv_file(self, file):
        self.sv_list.append(file)

    def add_rules(self, file_name):
        self.rules_flist.append(file_name)

    def add_swl_waiver(self, file_name):
        self.swl_waiver_flist.append(file_name)

    def add_awl_waiver(self, file_name):
        self.awl_waiver_flist.append(file_name)

    def add_sdc_file(self, file_name):
        self.sdc_flist.append(file_name)

    def write(self, file=None):
        file = "{}.tcl".format(self.name)
        s = "\n\n"
        s += "new_project spyglass_lint -force\n"
        for i in range(0, len(self.rtl_flist)):
            if self.root_path == "":
                s += "read_file -type sourcelist ./{}\n".format(self.rtl_flist[i])
            else:
                s += "read_file -type sourcelist $env({})/{}\n".format(self.root_path, self.rtl_flist[i])
        for i in range(0, len(self.vhdl_list)):
            if self.root_path == "":
                s += "read_file -type vhdl ./{}\n".format(self.vhdl_list[i])
            else:
                s += "read_file -type vhdl $env({})/{}\n".format(self.root_path, self.vhdl_list[i])
        for i in range(0, len(self.verilog_list)):
            if self.root_path == "":
                s += "read_file -type verilog ./{}\n".format(self.verilog_list[i])
            else:
                s += "read_file -type verilog $env({})/{}\n".format(self.root_path, self.verilog_list[i])
        for i in range(0, len(self.sv_list)):
            if self.root_path == "":
                s += "read_file -type systemverilog ./{}\n".format(self.sv_list[i])
            else:
                s += "read_file -type systemverilog $env({})/{}\n".format(self.root_path, self.sv_list[i])
        for i in range(0, len(self.rules_flist)):
            if self.root_path == "":
                s += "source ./{}\n".format(self.rules_flist[i])
            else:
                s += "source $env({})/{}\n".format(self.root_path, self.rules_flist[i])
        for i in range(0, len(self.swl_waiver_flist)):
            if self.root_path == "":
                s += "read_file -type waiver ./{}\n".format(self.swl_waiver_flist[i])
            else:
                s += "read_file -type waiver $env({})/{}\n".format(self.root_path, self.swl_waiver_flist[i])
        for i in range(0, len(self.awl_waiver_flist)):
            if self.root_path == "":
                s += "read_file -type awl ./{}\n".format(self.awl_waiver_flist[i])
            else:
                s += "read_file -type awl $env({})/{}\n".format(self.root_path, self.awl_waiver_flist[i])

        s += "set_option enableSV yes\n"
        s += """set_option nosavepolicies {txv lowpower power_est dft dft_dsm}\n"""
        s += "set_option language_mode mixed\n"
        s += "set_option sort yes\n"
        s += "set_option auto_save yes\n"
        s += "set_option sdc2sgdc yes\n"
        s += "\n\n"
        s += "current_methodology  $env(SPYGLASS_HOME)/GuideWare/latest/block/rtl_handoff\n"
        s += "current_goal Group_Run -goal "+"""{lint/lint_rtl lint/lint_turbo_rtl lint/lint_functional_rtl lint/lint_abstract}"""+" -top {}\n".format(self.module_name)
        s += "current_design {}\n".format(self.module_name)
        for i in range(0, len(self.sdc_flist)):
            if self.root_path == "":
                s += "sdc_data -file ./{}\n".format(self.sdc_flist[i])
            else:
                s += "sdc_data -file $env({})/{}\n".format(self.root_path, self.sdc_flist[i])

        s += "\n"
        s += "set_goal_option addrule SignedUnsignedExpr-ML\n"
        s += "set_goal_option addrule Av_width_mismatch_function\n"
        s += "set_goal_option addrule Av_width_mismatch_expr\n"
        s += "set_goal_option addrule Av_signed_unsigned_mismatch\n"
        s += "set_goal_option addrule Av_width_mismatch_port\n"
        s += "set_goal_option addrule Av_width_mismatch_expr02\n"
        s += "set_goal_option addrule Av_width_mismatch_assign\n"
        s += "set_goal_option addrule Av_width_mismatch_case\n"
        s += "set_goal_option addrule Av_width_mismatch_expr03\n"
        s += "set_goal_option addrule Av_dontcare_mismatch\n"
        s += "set_goal_option addrule Av_case_default_missing\n"
        s += """set_goal_option addrule { W164a W164b W164c }\n"""
        # check truncation of bits in constant integer conversion
        s += """set_goal_option addrule { W163  }\n"""
        # check truncation in constant conversion, without loss of data
        s += """set_goal_option addrule { W328  }\n"""    
        # check duplicate design unit
        s += """set_goal_option addrule { W546  }\n"""    

        s += """set_goal_option addrule { W182g }\n"""
        s += """set_goal_option addrule { W182h }\n"""
        s += """set_goal_option addrule { InferLatch }\n"""
        #s += """set_goal_option addrule { UndrivenIn }\n"""
        s += """set_goal_option addrule { W110  }\n"""
        s += """set_goal_option addrule { W116 W486 }\n"""
        s += """set_goal_option addrule { W123 }\n"""
        s += """set_goal_option addrule { W528 }\n"""

        s += """set_parameter check_static_value yes\n"""
        s += "\n"


        s += "run_goal\n"
        s += "save_project\n"
        s += "close_project\n"
        s += "exit\n"


        if file is None:
            return s
        else:
            fname = os.getcwd()
            fname += "/script/" + file
            if not os.path.exists('script'):
                os.mkdir('script')
            f = open(fname,'w')
            f.write(s)

if __name__ == "__main__":
    if len(sys.argv) < 6:
        raise Exception("Invalid parameters!\n example: python LintTclwriter.py module_name rootpath linttclname rtl_flist sdc_file ...")

    module_name = sys.argv[1]
    rootpath = sys.argv[2]
    linttcl_name = sys.argv[3]
    rtl_flist = sys.argv[4]
    sdc_file = sys.argv[5]

    g = LintTclWriter(module_name, rootpath, linttcl_name)
    g.add_rtl_flist(rtl_flist)
    g.add_sdc_file(sdc_file)

    g.write()
