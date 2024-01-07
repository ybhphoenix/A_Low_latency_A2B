#!/usr/bin/env python3
import math
import sys

from InstFun_Container import *
from Yaml_Loader import *
from Verilog_Writer import *



#################################################################################
 # class name       : SecCSA
 # description      : generate SecCSA verilog file
 #                    
 # function         : @my_ports                     : define the ports
 # function         : @my_signals                   : define the signals
 # function         : @module_ports                 : get the module ports
 # function         : @module_logics                : get the module signals 
 # function         : @instance_SecAnd_ports        : define the SecAnd_PINI1 ports
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
class SecCSA:
    def __init__(self, name, shares, width):
        self.verilog_writer = VerilogWriter(name, True, False, False)
        self.name           = name
        self.shares         = shares
        self.width          = width
        self.output_file    = "{}.v".format(name)
        self.latency        = 2
        self.inst_cnt       = int(0)



    def my_ports(self, share, width):
        num_of_rand = get_num_of_rand(share)
        num_of_x_y  = share
        ports = [
            ("dvld" , False , 0),
            ("rvld" , False , 0),
            ("n"    , False , num_of_rand*width),
            ("x"    , False , num_of_x_y*width),
            ("y"    , False , num_of_x_y*width),
            ("c_in" , False , num_of_x_y*width),
            ("c"    , True  , num_of_x_y*width),  
            ("s"    , True  , num_of_x_y*width), 
            ("dvld" , True  , 0),      
        ]
        return ports



    def my_signals(self, share, width):
        num_of_rand = get_num_of_rand(share)
        num_of_x_y  = share
        signals = [
            ("a"    , num_of_x_y*width),
            ("s"    , num_of_x_y*width),
            ("w"    , num_of_x_y*width),
            ("v"    , num_of_x_y*width),
            ("vls"  , num_of_x_y*width),
            ("sd"   , num_of_x_y*width),
            ("xd"   , num_of_x_y*width),
            ("xxv"  , num_of_x_y*width),
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
    
 

    def instance_SecAnd_ports(self):
        ports = [Port('clk_i'   , 'clk_i'),
                 Port('rst_ni'  , 'rst_ni'),
                 Port('i_dvld'  , 'i_dvld'),
                 Port('i_rvld'  , 'i_rvld'),
                 Port('i_n'     , 'i_n'),
                 Port('i_x'     , 'a'),
                 Port('i_y'     , 'w'),
                 Port('o_c'     , 'v'),
                 Port('o_dvld'  , 'o_dvld'),
        ]
        return ports


 
    def write(self):

        file = self.output_file



        self.verilog_writer.add(ModulePort('clk_i'  , 'input'))
        self.verilog_writer.add(ModulePort('rst_ni' , 'input'))



        ports = self.module_ports(self.shares, self.width, True)
        for port in ports:
            self.verilog_writer.add(port)      



        logics = self.module_logics(self.shares, self.width)
        for logic in logics:
            self.verilog_writer.add(logic)



        #################################################################################
        raw  = ""
        raw += add_comment("a[i]=x[i]^y[i];")
        self.verilog_writer.add(Raw(raw))


        inst_module_name    = "lix_xor"
        inst_name           = "u{}_lix_xor".format(self.inst_cnt)
        self.inst_cnt       = self.inst_cnt + int(1)
        inst_parameters     = [ Parameter('W',"{}".format(self.shares*self.width) ),]
        inst_ports          = instance_xor(ports[3].get_name(),  ports[4].get_name(), logics[0].get_name())
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
        raw += add_comment("s[i]=a[i]^cin[i];")
        self.verilog_writer.add(Raw(raw))


        inst_module_name    = "lix_xor"
        inst_name           = "u{}_lix_xor".format(self.inst_cnt)
        self.inst_cnt       = self.inst_cnt + int(1)
        inst_parameters     = [ Parameter('W',"{}".format(self.shares*self.width) ),]
        inst_ports          = instance_xor(logics[0].get_name(),  ports[5].get_name(), logics[1].get_name())
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
        raw += add_comment("w[i]=x[i]^cin[i];")
        self.verilog_writer.add(Raw(raw))


        inst_module_name    = "lix_xor"
        inst_name           = "u{}_lix_xor".format(self.inst_cnt)
        self.inst_cnt       = self.inst_cnt + int(1)
        inst_parameters     = [ Parameter('W',"{}".format(self.shares*self.width) ),]
        inst_ports          = instance_xor(ports[3].get_name(),  ports[5].get_name(), logics[2].get_name())
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
        raw += add_comment("SecAnd_PINI1(a,w,v,k,n);")
        self.verilog_writer.add(Raw(raw))



        inst_module_name    = "SecAnd_PINI1_n{}k{}_1".format(self.shares, self.width)
        inst_name           = "u{}_{}".format(self.inst_cnt, inst_module_name)
        self.inst_cnt       = self.inst_cnt + int(1)
        inst_parameters     = []
        inst_ports          = self.instance_SecAnd_ports()
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
        raw += add_comment("Delay s")
        self.verilog_writer.add(Raw(raw))


        inst_module_name    = "lix_shr0"
        inst_name           = "u{}_lix_shr0".format(self.inst_cnt)
        self.inst_cnt       = self.inst_cnt + int(1)
        inst_parameters     = [ Parameter('W',"{}".format(self.width*self.shares) ), Parameter('N',"2")]
        inst_ports          = instance_shr0(ports[0].get_name(), ports[1].get_name(), logics[1].get_name(), logics[5].get_name())
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
        raw += add_comment("Delay i_x")
        self.verilog_writer.add(Raw(raw))


        inst_module_name    = "lix_shr0"
        inst_name           = "u{}_lix_shr0".format(self.inst_cnt)
        self.inst_cnt       = self.inst_cnt + int(1)
        inst_parameters     = [ Parameter('W',"{}".format(self.width*self.shares) ), Parameter('N',"2")]
        inst_ports          = instance_shr0(ports[0].get_name(), ports[1].get_name(), ports[3].get_name(), logics[6].get_name())
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
        raw += add_comment("x[i] ^ v[i]")
        self.verilog_writer.add(Raw(raw))

        
        inst_module_name    = "lix_xor"
        inst_name           = "u{}_lix_xor".format(self.inst_cnt)
        self.inst_cnt       = self.inst_cnt + int(1)
        inst_parameters     = [ Parameter('W',"{}".format(self.shares*self.width) ),]
        inst_ports          = instance_xor(logics[6].get_name(), logics[3].get_name(), logics[7].get_name())
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
        raw += add_comment("c[i]=((x[i] ^ v[i])<<1) &MASK;")
        raw += assigns_1o1(logics[4].get_name(),logics[7].get_name() ," << ", 1, 0, self.shares,self.width)
        raw += add_comment("Connect to output")
        raw += assigns_1o1(ports[6].get_name(),logics[4].get_name() ,"",1,0,1,self.shares*self.width)
        raw += add_comment("Connect to output")
        raw += assigns_1o1(ports[7].get_name(),logics[5].get_name() ,"",1,0,1,self.shares*self.width)
        self.verilog_writer.add(Raw(raw))



        self.verilog_writer.write(file)


