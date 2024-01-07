#!/usr/bin/env python3
import math
import sys

from InstFun_Container import *
from Yaml_Loader import *
from Verilog_Writer import *
from FileList_Generator import *

from SecAnd_PINI1_Generator import SecAnd_PINI1
from SecRCA_1b_Generator import * 



#################################################################################
 # class name       : SecRCA
 # description      : generate SecRCA verilog file
 #          
 # function         : @initial_parameter            : initial the parameters        
 # function         : @my_ports                     : define the ports
 # function         : @my_signals                   : define the signals
 # function         : @module_ports                 : get the module ports
 # function         : @module_logics                : get the module signals 
 # function         : @instance_SecRCA_1b_ports     : define the SecRCA_1b ports
 # function         : @write                        : write file
 #       
 # input            : @name                 : the name             
 # input            : @shares               : the shares
 # input            : @width                : the width
 # returns          : this class
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
class SecRCA:
    def __init__(self, name, shares, width, exist_odvld=int(1)):
        self.name           = "{}_{}".format(name, exist_odvld)       
        self.verilog_writer = VerilogWriter(self.name, True, False, False)
        self.shares         = shares
        self.width          = width
        self.exist_odvld    = exist_odvld
        self.and_instlist   = []
        self.rca_1b_instlist= []
        self.output_file    = "{}.v".format(self.name)
        self.wrand          = get_num_of_rand(shares)*(width-1)
        self.latency        = 2*(width-1)
        self.initial_parameter()
        self.inst_cnt       = int(0)



    def initial_parameter(self):
        inst_name = "SecAnd_PINI1_n{}k{}".format(self.shares, 1)
        self.and_instlist.append(SecAnd_PINI1(inst_name, self.shares, 1))
        for i in range(0, self.width-1):
            inst_name = "SecRCA_1b_n{}k{}_{}".format(self.shares, self.width, i)
            self.rca_1b_instlist.append(SecRCA_1b(inst_name, self.shares, self.width, i))



    def my_ports(self):
        ports = [
            ("dvld" , False , 0),
            ("rvld" , False , 0),
            ("n"    , False , self.wrand),            
            ("x"    , False , self.shares*self.width),
            ("y"    , False , self.shares*self.width),
            ("z"    , True  , self.shares*self.width),
            ("dvld" , True  , 0),      
        ]
        return ports


    
    def my_signals(self, index, a_width, x_width, c_width):
        suffix = "_{}".format(index)
        signals = [
            ("dvld"+suffix ,0),
            ("a"+suffix    ,a_width),
            ("x"+suffix    ,x_width),
            ("c"+suffix    ,c_width),
        ]
        return signals



    def module_ports(self,share, width, is_input):
        ports = []
        for (name, _dir, width) in self.my_ports():
            prefix = 'o' if is_input == _dir else 'i'
            if not (name =="dvld" and prefix =="o" and self.exist_odvld==int(0)):
                ports.append(ModulePort("{}_{}".format(prefix,name),
                                    'output' if is_input == _dir else 'input',
                                    width))
        return ports



    def module_logics(self):
        logics = []
        size = len(self.rca_1b_instlist)
        for i in range(0, size):
            for (n, w) in self.my_signals(i, 
                                          self.rca_1b_instlist[i].a_in_width , 
                                          self.rca_1b_instlist[i].x_in_width , 
                                          self.rca_1b_instlist[i].c_in_width ):
                logics.append(Wire("{}".format(n), w))
        for (n, w) in self.my_signals(size, 
                                      self.rca_1b_instlist[size-1].a_out_width,
                                      self.rca_1b_instlist[size-1].x_out_width, 
                                      self.rca_1b_instlist[size-1].c_out_width):
            logics.append(Wire("{}".format(n), w))    
        logics.append(Wire("c_e", self.shares*self.width))    
        return logics
    


    def instance_SecRCA_1b_ports(self, index):
        suffix0 = "_{}".format(index)
        suffix1 = "_{}".format(index+1)
        wrand   = get_num_of_rand(self.shares)
        ports = [Port('clk_i'  , 'clk_i'),
                 Port('rst_ni' , 'rst_ni'),
                 Port('i_dvld' , 'dvld'+suffix0),
                 Port('i_rvld' , 'i_rvld'),
                 Port('i_n'    , "i_n[{}+:{}]".format(wrand*index, wrand)),
                 Port("i_a"    , 'a'+suffix0),
                 Port("i_x"    , 'x'+suffix0),
                 Port("i_c"    , 'c'+suffix0),
                 Port("o_a"    , 'a'+suffix1),
                 Port("o_x"    , 'x'+suffix1),
                 Port("o_c"    , 'c'+suffix1),
                 Port('o_dvld' , 'dvld'+suffix1),
        ]
        return ports



    def write(self, fp_filelist = ""):

        file = self.output_file



        self.verilog_writer.add(ModulePort('clk_i' , 'input'))
        self.verilog_writer.add(ModulePort('rst_ni', 'input'))



        ports = self.module_ports(self.shares, self.width, True)
        for port in ports:
            self.verilog_writer.add(port)      
        


        logics = self.module_logics()
        for logic in logics:
            self.verilog_writer.add(logic)



        #################################################################################        
        raw  = "\n"
        raw += add_comment("c[i]=0;")
        raw += assigns_zeros(logics[3].get_name(), 0, 1, 1)
        self.verilog_writer.add(Raw(raw))



        #################################################################################
        raw  = ""
        raw += add_comment("a[i]=x[i] ^ y[i];")
        self.verilog_writer.add(Raw(raw))



        #################################################################################
        # a[i]=x[i] ^ y[i];
        inst_module_name    = "lix_xor"
        inst_name           = "u{}_lix_xor".format(self.inst_cnt)
        self.inst_cnt       = self.inst_cnt + int(1)
        inst_parameters     = [ Parameter('W',"{}".format(self.shares*self.width) ),]
        inst_ports          = instance_xor(ports[3].get_name(), ports[4].get_name(), logics[1].get_name())
        inst_fraw           = ""
        inst_praw           = ""   
        self.verilog_writer.add(Instance(inst_module_name,
                                         inst_name,
                                         inst_parameters,
                                         inst_ports,
                                         inst_fraw,
                                         inst_praw))

    

        #################################################################################
        raw  = ""
        # connect x to inst0'x
        raw += add_comment("connect x to SecRCA_1b inst0'x")
        raw += assigns_1o1(logics[2].get_name(), ports[3].get_name(), "", 0, 0, 1, self.shares*self.width)
        # connect i_dvld to inst0'i_dvld
        raw += add_comment("connect i_dvld to SecRCA_1b inst0'i_dvld")
        raw += assigns_1o1(logics[0].get_name(), ports[0].get_name(), "", 0, 0, 1, 1)
        self.verilog_writer.add(Raw(raw))




        #################################################################################
        # SecRCA_1b
        for i in range(0, self.width-1):
            raw  = ""
            raw += add_comment("Do SecRCA_1b {} instance".format(i))
            self.verilog_writer.add(Raw(raw))

            inst_module_name    = self.rca_1b_instlist[i].name
            inst_name           = "u{}_{}".format(self.inst_cnt,self.rca_1b_instlist[i].name)
            self.inst_cnt       = self.inst_cnt + int(1)
            inst_parameters     = []
            inst_ports          = self.instance_SecRCA_1b_ports(i)
            inst_fraw           = ""
            inst_praw           = ""   
            self.verilog_writer.add(Instance(inst_module_name,
                                             inst_name,
                                             inst_parameters,
                                             inst_ports,
                                             inst_fraw,
                                             inst_praw))  



        #################################################################################
        raw = ""  
        raw += add_comment("c[i] |= (tx[i] << (j+1))\nwhen j=0, bit0=0")
        raw += assign_rcat(logics[self.width*4].get_name(), logics[(self.width-1)*4+3].get_name(), 0, self.shares, self.width-1, "", 1)
        self.verilog_writer.add(Raw(raw))  



        #################################################################################
        # z[i]=a[i] ^ c[i]
        raw  = ""
        raw += add_comment("z[i]=a[i] ^ c[i]")
        self.verilog_writer.add(Raw(raw))

        inst_module_name    = "lix_xor"
        inst_name           = "u{}_lix_xor".format(self.inst_cnt)
        self.inst_cnt       = self.inst_cnt + int(1)
        inst_parameters     = [ Parameter('W',"{}".format(self.shares*self.width) ),]
        inst_ports          = instance_xor(logics[(self.width-1)*4+1].get_name(), logics[self.width*4].get_name(), ports[5].get_name())
        inst_fraw           = ""
        inst_praw           = ""   
        self.verilog_writer.add(Instance(inst_module_name,
                                         inst_name,
                                         inst_parameters,
                                         inst_ports,
                                         inst_fraw,
                                         inst_praw))



        #################################################################################         
        # connect last inst'o_dvld to port o_dvld
        if self.exist_odvld == int(1):
            raw = ""
            raw += add_comment("connect last inst'o_dvld to port o_dvld")
            raw += assigns_1o1(ports[6].get_name(), logics[(self.width-1)*4+0].get_name(), "", 0, 0, 1, 1)
            self.verilog_writer.add(Raw(raw))



        self.verilog_writer.write(file)



        #################################################################################
        for i in range(0, len(self.rca_1b_instlist)):        
            self.rca_1b_instlist[i].write()
        for i in range(0, len(self.and_instlist)):        
            self.and_instlist[i].write()



        #################################################################################
        if fp_filelist != "":
            fp_filelist.add(File(self.name, True))  
            for i in range(0, len(self.rca_1b_instlist)):
                fp_filelist.add(File(self.rca_1b_instlist[i].name, True))
            for i in range(0, len(self.and_instlist)):
                fp_filelist.add(File(self.and_instlist[i].name, True))


