#!/usr/bin/env python3
import math
import sys

from InstFun_Container import *
from Yaml_Loader import *
from Verilog_Writer import *



#################################################################################
 # class name       : SecKSA_1l
 # description      : generate SecKSA one loop verilog file
 #                    
 # function         : @my_ports                     : define the ports
 # function         : @my_signals                   : define the signals
 # function         : @module_ports                 : get the module ports
 # function         : @module_logics                : get the module signals 
 # function         : @instance_SecAnd_0_ports      : define the SecAnd_PINI1 ports
 # function         : @instance_SecAnd_1_ports      : define the SecAnd_PINI1 ports
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
class SecKSA_1l:
    def __init__(self, name, shares, width):
        self.verilog_writer = VerilogWriter(name, True, False, False)
        self.name           = name
        self.shares         = shares
        self.width          = width
        self.output_file    = "{}.v".format(name)
        self.wrand          = get_num_of_rand(shares)*width
        self.inst_cnt       = int(0)



    def my_ports(self, share, width):
        num_of_rand = get_num_of_rand(share)
        num_of_x_y  = share;
        ports = [
            ("dvld" , False , 0),
            ("rvld" , False , 0),
            ("n"    , False , (2)*num_of_rand*width),
            ("p"    , False , num_of_x_y*width),
            ("g"    , False , num_of_x_y*width),
            ("p"    , True  , num_of_x_y*width),  
            ("g"    , True  , num_of_x_y*width), 
            ("dvld" , True  , 0),      
        ]
        return ports
    


    def my_signals(self, share, width):
        num_of_rand = get_num_of_rand(share)
        num_of_x_y  = share;
        signals = [
            ("tmp1" , num_of_x_y*width),
            ("a1"   , num_of_x_y*width),
            ("gd"   , num_of_x_y*width),
            ("tmp2" , num_of_x_y*width),
            ("a2"   , num_of_x_y*width),
        ]
        return signals



    def module_ports(self,share, width, is_input):
        ports = []
        for (name, _dir, width) in self.my_ports(share, width):
            prefix = 'o' if is_input == _dir else 'i'
            ports.append(ModulePort("{}_{}".format(prefix,name),
                                'output' if is_input == _dir else 'input',
                                width))
        return ports



    def module_logics(self,share, width):
        logics = []
        for (n, w) in self.my_signals(share, width):
            logics.append(Wire("{}".format(n), w))
        return logics
    


    def instance_SecAnd_0_ports(self,rand_idx):
        ports = [Port('clk_i'  , 'clk_i'),
                 Port('rst_ni' , 'rst_ni'),
                 Port('i_dvld' , 'i_dvld'),
                 Port('i_rvld' , 'i_rvld'),
                 Port('i_n'    , "i_n[{}+:{}]".format(rand_idx*self.wrand,self.wrand)),
                 Port('i_x'    , 'i_p'),
                 Port('i_y'    , 'tmp1'),
                 Port('o_c'    , 'a1'),
                 Port('o_dvld' , 'o_dvld'),
        ]
        return ports



    def instance_SecAnd_1_ports(self,rand_idx):
        ports = [Port('clk_i'  , 'clk_i'),
                 Port('rst_ni' , 'rst_ni'),
                 Port('i_dvld' , 'i_dvld'),
                 Port('i_rvld' , 'i_rvld'),
                 Port('i_n'    , "i_n[{}+:{}]".format(rand_idx*self.wrand,self.wrand)),
                 Port('i_x'    , 'i_p'),
                 Port('i_y'    , 'tmp2'),
                 Port('o_c'    , 'a2'),
        ]
        return ports


 
    def write(self):

        file = self.output_file

        self.verilog_writer.add(ModuleParameter('SHIFT','1'))
        self.verilog_writer.add(ModuleParameter('POW','2**SHIFT'))



        self.verilog_writer.add(ModulePort('clk_i' , 'input'))
        self.verilog_writer.add(ModulePort('rst_ni', 'input'))



        ports = self.module_ports(self.shares, self.width, True)
        for port in ports:
            self.verilog_writer.add(port)      



        logics = self.module_logics(self.shares, self.width)
        for logic in logics:
            self.verilog_writer.add(logic)



        #################################################################################        
        raw = ""
        raw += add_comment("tmp[i]=(g[i]<<pow)&MASK;")
        raw += assigns_1o1(logics[0].get_name(),ports[4].get_name() ," << ",'POW',0,self.shares,self.width)
        raw += add_comment("tmp[i]=(p[i]<<pow)&MASK;")
        raw += assigns_1o1(logics[3].get_name(),ports[3].get_name() ," << ",'POW',0,self.shares,self.width)  
        self.verilog_writer.add(Raw(raw))



        #################################################################################        
        raw  = ""
        raw += add_comment("SecAnd_PINI1(p,tmp,a,k,n);")
        self.verilog_writer.add(Raw(raw))

        inst_module_name    = "SecAnd_PINI1_n{}k{}_1".format(self.shares, self.width)
        inst_name           = "u{}_{}".format(self.inst_cnt, inst_module_name)
        self.inst_cnt       = self.inst_cnt + int(1)
        inst_parameters     = []
        inst_ports          = self.instance_SecAnd_0_ports(0)
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
        raw += add_comment("SecAnd_PINI1(p,tmp,a,k,n);")
        self.verilog_writer.add(Raw(raw))

        inst_module_name    = "SecAnd_PINI1_n{}k{}_0".format(self.shares, self.width)
        inst_name           = "u{}_{}".format(self.inst_cnt, inst_module_name)
        self.inst_cnt       = self.inst_cnt + int(1)
        inst_parameters     = []
        inst_ports          = self.instance_SecAnd_1_ports(1)
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
        raw += add_comment("Delay i_g")
        self.verilog_writer.add(Raw(raw))
  
        inst_module_name    = "lix_shr0"
        inst_name           = "u{}_lix_shr0".format(self.inst_cnt)
        self.inst_cnt       = self.inst_cnt + int(1)
        inst_parameters     = [ Parameter('W',"{}".format(self.width*self.shares) ), Parameter('N',"2")]
        inst_ports          = instance_shr0(ports[0].get_name(), ports[1].get_name(), ports[4].get_name(), logics[2].get_name())
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
        raw += add_comment("g[i]=g[i]^a[i];")
        self.verilog_writer.add(Raw(raw))

        inst_module_name    = "lix_xor"
        inst_name           = "u{}_lix_xor".format(self.inst_cnt)
        self.inst_cnt       = self.inst_cnt + int(1)
        inst_parameters     = [ Parameter('W',"{}".format(self.shares*self.width) ),]
        inst_ports          = instance_xor(logics[2].get_name(), logics[1].get_name(), ports[6].get_name())
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
        raw += add_comment("Connect a2 to output")
        raw += assigns_1o1(ports[5].get_name(),logics[4].get_name() ,"",1,0,1,self.shares*self.width)
        self.verilog_writer.add(Raw(raw))



        self.verilog_writer.write(file)


