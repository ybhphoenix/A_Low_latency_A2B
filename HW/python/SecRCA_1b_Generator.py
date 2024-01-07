#!/usr/bin/env python3
import math
import sys

from InstFun_Container import *
from Yaml_Loader import *
from Verilog_Writer import *



#################################################################################
 # class name       : SecRCA_1b
 # description      : generate SecRCA one bit verilog file
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
 # input            : @index                : the index of this class instance
 # returns          : this class
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
class SecRCA_1b:
    def __init__(self, name, shares, width, index):
        self.verilog_writer = VerilogWriter(name,  True, False, False)
        self.name           = name
        self.shares         = shares
        self.width          = width
        self.index          = index
        self.output_file    = "{}.v".format(name)
        self.wrand          = get_num_of_rand(shares)*1
        self.latency        = 2
        self.a_in_width     = width*shares
        self.a_out_width    = width*shares
        self.x_in_width     = (width-index)*shares
        self.x_out_width    = (width-index-1)*shares
        self.c_in_width     = (index)*shares
        self.c_out_width    = (index+1)*shares
        self.sig_aj_width   = shares
        self.sig_xj_width   = shares
        self.sig_b_width    = shares
        self.sig_tmp_width  = shares
        self.sig_cj_width   = shares
        self.sig_tx_width   = shares
        self.sig_a_d_width  = width*shares
        self.sig_x_d_width  = (width-index-1)*shares
        self.sig_c_d_width  = index*shares
        self.sig_xj_d_width = shares
        self.inst_cnt       = int(0)



    def my_ports(self):
        ports = [
            ("dvld" , False , 0),
            ("rvld" , False , 0),
            ("n"    , False , self.wrand),            
            ("a"    , False , self.a_in_width),
            ("x"    , False , self.x_in_width),
            ("c"    , False , self.c_in_width),
            ("a"    , True  , self.a_out_width),
            ("x"    , True  , self.x_out_width),
            ("c"    , True  , self.c_out_width),
            ("dvld" , True  , 0),      
        ]
        return ports
 


    def my_signals(self):
        signals = [
            ("aj"   , self.sig_aj_width),
            ("xj"   , self.sig_xj_width),
            ("xrs"  , self.x_out_width),            
            ("b"    , self.sig_b_width),
            ("tmp"  , self.sig_tmp_width),
            ("cj"   , self.sig_cj_width),
            ("tx"   , self.sig_tx_width),
            ("ad"   , self.sig_a_d_width),
            ("xd"   , self.sig_x_d_width),
            ("cd"   , self.sig_c_d_width),
            ("xjd"  , self.sig_xj_d_width),
        ]
        return signals



    def module_ports(self,share, width, is_input):
        ports = []
        for (name, _dir, width) in self.my_ports():
            prefix = 'o' if is_input == _dir else 'i'
            ports.append(ModulePort("{}_{}".format(prefix,name),
                                'output' if is_input == _dir else 'input',
                                width))
        return ports



    def module_logics(self,share, width):
        logics = []
        for (n, w) in self.my_signals():
            logics.append(Wire("{}".format(n), w))
        return logics
    


    def instance_SecAnd_ports(self):
        ports = [Port('clk_i'  , 'clk_i'),
                 Port('rst_ni' , 'rst_ni'),
                 Port('i_dvld' , 'i_dvld'),
                 Port('i_rvld' , 'i_rvld'),
                 Port('i_n'    , "i_n"),
                 Port('i_x'    , 'b'),
                 Port('i_y'    , 'aj'),
                 Port('o_c'    , 'tmp'),
                 Port('o_dvld' , 'o_dvld'),
        ]
        return ports



    def write(self):

        file = self.output_file


        self.verilog_writer.add(ModulePort('clk_i' , 'input'))
        self.verilog_writer.add(ModulePort('rst_ni', 'input'))



        ports = self.module_ports(self.shares, self.width, True)
        for port in ports:
            self.verilog_writer.add(port)      
        


        logics = self.module_logics(self.shares, self.width)
        for logic in logics:
            self.verilog_writer.add(logic)


        #################################################################################        
        raw  = ""
        # aj
        raw += add_comment("Get the j={} bit in per shares\naj[i] = (a[i]>>j) & (uint32_t)1;".format(self.index))
        raw += assign_1mo1v(logics[0].get_name(), ports[3].get_name(), 0, self.shares, self.width, self.index)
        # xj
        raw += add_comment("Get the low bit in per shares\nx[i] & (uint32_t)1;")
        raw += assign_1mo1v(logics[1].get_name(), ports[4].get_name(), 0, self.shares, (self.width-self.index), 0)
        # xrs
        raw += add_comment("Remove the low bit in per shares\nx[i] = x[i] >> 1;")
        raw += assign_rsh(logics[2].get_name(), ports[4].get_name(), 0, self.shares, self.width-self.index, 1)
        # cj
        raw += add_comment("Get the j={} bit in per shares\ncj[i] = (c[i]>>j) & (uint32_t)1;".format(self.index-1))
        raw += assign_1mo1v(logics[5].get_name(), ports[5].get_name(), 0, self.shares, self.index, (self.index-1))
        self.verilog_writer.add(Raw(raw))


        #################################################################################
        # b
        raw  = ""
        raw += add_comment("b[i] = xj[i] ^ cj[i];")
        self.verilog_writer.add(Raw(raw))

        inst_module_name    = "lix_xor"
        inst_name           = "u{}_lix_xor".format(self.inst_cnt)
        self.inst_cnt       = self.inst_cnt + int(1)
        inst_parameters     = [ Parameter('W',"{}".format(self.shares) ),]
        inst_ports          = instance_xor(logics[1].get_name(), logics[5].get_name(), logics[3].get_name())
        inst_fraw           = ""
        inst_praw           = ""   
        self.verilog_writer.add(Instance(inst_module_name,
                                         inst_name,
                                         inst_parameters,
                                         inst_ports,
                                         inst_fraw,
                                         inst_praw))


        #################################################################################
        # SecAND
        raw  = ""
        raw += add_comment("Do a SecAnd instance")
        self.verilog_writer.add(Raw(raw))

        inst_module_name    = "SecAnd_PINI1_n{}k{}_1".format(self.shares, 1)
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
        # a delay
        raw  = ""
        raw += add_comment("Delay i_a")
        self.verilog_writer.add(Raw(raw))

        width               = self.shares*self.width
        inst_module_name    = "lix_shr0"
        inst_name           = "u{}_lix_shr0".format(self.inst_cnt)
        self.inst_cnt       = self.inst_cnt + int(1)
        inst_parameters     = [ Parameter('W',"{}".format(width) ), Parameter('N','{}'.format(2))]
        inst_ports          = instance_shr0(ports[0].get_name(), ports[1].get_name(), ports[3].get_name(), logics[7].get_name(), width, 0 )
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
        raw += add_comment("Connect to the output") 
        raw += assigns_1o1(ports[6].get_name(),logics[7].get_name() ,"",1,0,1,self.shares*self.width)
        self.verilog_writer.add(Raw(raw))


        #################################################################################
        # x delay
        raw  = ""
        raw += add_comment("Delay xrs")
        self.verilog_writer.add(Raw(raw))

        width               = self.x_out_width
        inst_module_name    = "lix_shr0"
        inst_name           = "u{}_lix_shr0".format(self.inst_cnt)
        self.inst_cnt       = self.inst_cnt + int(1)
        inst_parameters     = [ Parameter('W',"{}".format(width) ), Parameter('N','{}'.format(2))]
        inst_ports          = instance_shr0(ports[0].get_name(), ports[1].get_name(), logics[2].get_name(), logics[8].get_name(), width, 0 )
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
        raw += add_comment("Connect to the output")         
        raw += assigns_1o1(ports[7].get_name(),logics[8].get_name() ,"",1,0,1,self.x_out_width)
        self.verilog_writer.add(Raw(raw))


        #################################################################################
        # c delay
        raw  = ""
        raw += add_comment("Delay i_c")
        self.verilog_writer.add(Raw(raw))

        if self.c_in_width == int(0):
            width = 1;
        else:
            width               = self.c_in_width
        inst_module_name    = "lix_shr0"
        inst_name           = "u{}_lix_shr0".format(self.inst_cnt)
        self.inst_cnt       = self.inst_cnt + int(1)
        inst_parameters     = [ Parameter('W',"{}".format(width) ), Parameter('N','{}'.format(2))]
        inst_ports          = instance_shr0(ports[0].get_name(), ports[1].get_name(), ports[5].get_name(), logics[9].get_name(), self.c_in_width, 0 )
        inst_fraw           = ""
        inst_praw           = ""   
        self.verilog_writer.add(Instance(inst_module_name,
                                         inst_name,
                                         inst_parameters,
                                         inst_ports,
                                         inst_fraw,
                                         inst_praw)) 


        #################################################################################
        # xj delay
        raw  = ""
        raw += add_comment("Delay xj")
        self.verilog_writer.add(Raw(raw))

        width               = self.sig_xj_d_width
        inst_module_name    = "lix_shr0"
        inst_name           = "u{}_lix_shr0".format(self.inst_cnt)
        self.inst_cnt       = self.inst_cnt + int(1)
        inst_parameters     = [ Parameter('W',"{}".format(width) ), Parameter('N','{}'.format(2))]
        inst_ports          = instance_shr0(ports[0].get_name(), ports[1].get_name(), logics[1].get_name(), logics[10].get_name(), width, 0 )
        inst_fraw           = ""
        inst_praw           = ""   
        self.verilog_writer.add(Instance(inst_module_name,
                                         inst_name,
                                         inst_parameters,
                                         inst_ports,
                                         inst_fraw,
                                         inst_praw)) 


        #################################################################################
        # cal tx
        raw  = ""
        raw += add_comment("tx[i] = tmp[i] ^ xj[i];")
        self.verilog_writer.add(Raw(raw))

        inst_module_name    = "lix_xor"
        inst_name           = "u{}_lix_xor".format(self.inst_cnt)
        self.inst_cnt       = self.inst_cnt + int(1)
        inst_parameters     = [ Parameter('W',"{}".format(self.sig_xj_d_width) ),]
        inst_ports          = instance_xor(logics[4].get_name(), logics[10].get_name(), logics[6].get_name())
        inst_fraw           = ""
        inst_praw           = ""   
        self.verilog_writer.add(Instance(inst_module_name,
                                         inst_name,
                                         inst_parameters,
                                         inst_ports,
                                         inst_fraw,
                                         inst_praw))


        #################################################################################
        # get c
        raw  = ""
        raw += add_comment("c[i] |= (tx[i] << (j+1));")
        raw += assign_lcat(ports[8].get_name(), logics[9].get_name(), 0, self.shares, self.index, logics[6].get_name(), 1)
        self.verilog_writer.add(Raw(raw))



        self.verilog_writer.write(file)


