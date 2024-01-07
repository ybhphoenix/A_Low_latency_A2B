#!/usr/bin/env python3
import math
import sys

from InstFun_Container import *
from Yaml_Loader import *
from Verilog_Writer import *



#################################################################################
 # class name       : ConvertAB_RCA_tb
 # description      : generate ConvertAB_RCA test bench system verilog file
 #                    
 # returns          : this class
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
class ConvertAB_RCA_tb:
    def __init__(self, name, shares, width, list_instname, dumpon):
        self.verilog_writer = VerilogWriter(name, False)
        self.name           = name
        self.shares         = shares
        self.width          = width
        self.output_file    = "{}.sv".format(name)
        self.list_instname  = list_instname
        self.dut_name       = "{}_{}".format(list_instname.name, list_instname.exist_odvld)
        self.wrand          = get_num_of_rand(shares)*width
        self.wxy            = shares*width
        self.wxxy           = self.wxy*shares
        self.n_start        = 0
        self.n_width        = 0
        self.dumpon         = dumpon
        self.inst_cnt       = int(0)



    def my_signals(self, share, width):
        signals = [
            ("clk_i"    , 0),
            ("rst_ni"   , 0),
            ("i_dvld"   , 0),
            ("i_rvld"   , 0),
            ("i_n"      , self.list_instname.r_len*1),
            ("i_a"      , self.shares*self.width),
            ("o_z"      , self.shares*self.width),
            ("o_dvld"   , 0),
            ("a"        , self.shares*self.width),
            ("dvld"     , 0),
            ("A"        , self.width),
            ("B"        , self.width),
            ("A_d"      , self.width),
            ("pass"     , 0),
            ("rvld"     , 0),
        ]
        return signals



    def module_logics(self, share, width):
        logics = []
        for (n, w) in self.my_signals(share, width):
            logics.append(Logic("{}".format(n), w))
        return logics
    


    def instance_ConvertAB_ports(self):
        ports = [Port('clk_i'   , 'clk_i'),
                 Port('rst_ni'  , 'rst_ni'),
                 Port('i_dvld'  , 'i_dvld'),
                 Port('i_rvld'  , 'i_rvld'),
                 Port('i_n'     , "i_n"),
                 Port('i_a'     , "i_a"),
                 Port('o_z'     , "o_z"),
                 Port('o_dvld'  , 'o_dvld'),
        ]
        return ports



    def write(self):

        file = self.output_file



        logics = self.module_logics(self.shares, self.width)
        for logic in logics:
            self.verilog_writer.add(logic)


        #################################################################################
        raw  = gen_clock(logics[0].get_name(), 10)
        raw += gen_reset(logics[1].get_name(), 100)
        raw += gen_rand(logics[0].get_name(), 15, logics[4].get_name(), self.list_instname.r_len, 1, True)
        raw += gen_rand(logics[0].get_name(), 15, logics[8].get_name(), self.shares, self.width, True)
        raw += gen_vld(logics[0].get_name(), 16, logics[9].get_name(), 500)
        raw += gen_vld(logics[0].get_name(), 16, logics[14].get_name(), 500+self.list_instname.latency)
        raw += "assign {}[{}+:{}] = {}[{}+:{}] ".format(logics[5].get_name(), 0, self.width, logics[8].get_name(), 0, self.width, self.width)
        for i in range (1, self.shares):
            raw += "- {}[{}+:{}] ".format(logics[8].get_name(), i*self.width,self.width)
        raw += ";\n"
        for i in range (1, self.shares):
            raw += "assign {}[{}+:{}] = {}[{}+:{}];\n".format(logics[5].get_name(), i*self.width,self.width, logics[8].get_name(), i*self.width,self.width)

        raw += "assign {} = {};\n".format(logics[2].get_name(),logics[9].get_name())
        raw += "assign {} = {};\n".format(logics[3].get_name(),logics[14].get_name())
        self.verilog_writer.add(Raw(raw))



        #################################################################################
        inst_module_name    = self.dut_name
        inst_name           = "dut_{}".format(self.dut_name)
        self.inst_cnt       = self.inst_cnt + int(1)
        inst_parameters     = []
        inst_ports          = self.instance_ConvertAB_ports()
        inst_fraw           = "";
        inst_praw           = "";
        
        self.verilog_writer.add(Instance(inst_module_name,
                                         inst_name,
                                         inst_parameters,
                                         inst_ports,
                                         inst_fraw,
                                         inst_praw))        



        #################################################################################
        raw = "\n"
        raw += "assign {}[{}+:{}] = {}[{}+:{}] ".format(logics[10].get_name(), 0, self.width, logics[5].get_name(), 0, self.width, self.width)
        for i in range (1, self.shares):
            raw += "+ {}[{}+:{}] ".format(logics[5].get_name(), i*self.width,self.width)
        raw += ";\n"
        raw += "\n"
        raw += "assign {}[{}+:{}] = {}[{}+:{}] ".format(logics[11].get_name(), 0, self.width, logics[6].get_name(), 0, self.width, self.width)
        for i in range (1, self.shares):
            raw += "^ {}[{}+:{}] ".format(logics[6].get_name(), i*self.width,self.width)
        raw += ";\n"
        raw += inst_sh(logics[12].get_name(), logics[10].get_name(), "", self.list_instname.latency, self.width)
        raw += assigns_2o1(logics[13].get_name(), logics[11].get_name() , " == ", logics[12].get_name(), 0, 1, self.width)
        raw += disp_result(logics[0].get_name(),logics[13].get_name(),logics[7].get_name(), 7000)
        self.verilog_writer.add(Raw(raw))



        #################################################################################        
        raw = "// dumpon = {}\n".format(self.dumpon)
        if self.dumpon == int(1):
            raw += gen_fsdb(self.name)
            self.verilog_writer.add(Raw(raw))   



        #################################################################################
        raw = gen_finish(8000)     
        self.verilog_writer.add(Raw(raw))   



        #################################################################################
        self.verilog_writer.write(file)


