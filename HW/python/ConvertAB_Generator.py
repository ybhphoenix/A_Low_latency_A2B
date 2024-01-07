#!/usr/bin/env python3
import math
import sys

from InstFun_Container import *
from Yaml_Loader import *
from Verilog_Writer import *
from Sdc_Writer import SdcWriter



#################################################################################
 # class name       : ConvertAB
 # description      : generate ConvertAB verilog file
 #                    
 # function         : @my_ports                     : define the ports
 # function         : @module_ports                 : get the module ports
 # function         : @module_logics                : get the module signals 
 # function         : @instance_convertabx_0_ports  : define the left convertAB ports
 # function         : @instance_convertabx_1_ports  : define the left convertAB ports
 # function         : @instance_expandx_ports       : define the left expand ports
 # function         : @instance_convertaby_ports    : define the right convertAB ports
 # function         : @instance_expandy_ports       : define the right expand ports
 # function         : @instance_ksa_0_ports         : define the SecKSA ports
 # function         : @instance_ksa_1_ports         : define the SecKSA ports
 # function         : @write                        : write file
 #       
 # input            : @name                 : the name             
 # input            : @shares               : the shares
 # input            : @width                : the width
 # input            : @list_par             : the parameter list
 # input            : @inst_cnt             : the counter of instance
 # returns          : this class
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
class ConvertAB:
    def __init__(self, name, shares, width, list_par):
        self.name           = "{}_{}".format(name, list_par.exist_odvld) 
        self.shares         = shares
        self.width          = width        
        self.verilog_writer = VerilogWriter(self.name, True, False, False)
        self.sdc_writer     = SdcWriter(self.name)
        self.output_file    = "{}.v".format(self.name)
        self.list_par       = list_par
        self.inst_cnt       = int(0)



    def my_ports(self):
        ports = [
            ("dvld" , False , 0),
            ("rvld" , False , 0),
            ("n"    , False , self.list_par.r_len*self.width),
            ("a"    , False , self.shares*self.width),
            ("z"    , True  , self.shares*self.width),  
            ("dvld" , True  , 0),      
        ]
        return ports



    def module_ports(self, share, width, is_input):
        ports = []
        for (name, _dir, width) in self.my_ports():
            prefix = 'o' if is_input == _dir else 'i'
            if not (name =="dvld" and prefix =="o" and self.list_par.exist_odvld==int(0)):
                ports.append(ModulePort("{}_{}".format(prefix,name),
                                    'output' if is_input == _dir else 'input',
                                    width))
        return ports



    def module_logics(self):
        logics = []
        if self.list_par.shares > int(1):
            logics.append(Wire("x"      , self.list_par.ll_shares*self.list_par.ll_width))
            logics.append(Wire("xd"     , self.list_par.ll_shares*self.list_par.ll_width))
            logics.append(Wire("xp"     , self.list_par.shares*self.list_par.width))
            logics.append(Wire("y"      , self.list_par.rl_shares*self.list_par.rl_width))
            logics.append(Wire("yd"     , self.list_par.rl_shares*self.list_par.rl_width))
            logics.append(Wire("yp"     , self.list_par.shares*self.list_par.width))  
            logics.append(Wire("vrl"    , 0))                                     
            logics.append(Wire("vy"     , 0)) 
            if self.list_par.ll_exist_odvld == int(1):
                logics.append(Wire("vll"    , 0)) 
        return logics
  


    def instance_convertabx_0_ports(self):
        ports = [Port('clk_i'   , 'clk_i'),
                 Port('rst_ni'  , 'rst_ni'),
                 Port('i_dvld'  , 'i_dvld'),
                 Port('i_rvld'  , 'i_rvld'),
                 Port('i_n'     , "i_n[{}+:{}]".format(self.list_par.ll_r_start*self.list_par.ll_width,self.list_par.ll_r_len*self.list_par.ll_width)),
                 Port('i_a'     , "i_a[{}+:{}]".format(self.list_par.ll_a_start*self.list_par.ll_width,self.list_par.ll_a_len*self.list_par.ll_width)),
                 Port('o_z'     , "x[{}+:{}]".format(0,self.list_par.ll_shares*self.list_par.ll_width)),
        ]
        return ports



    def instance_convertabx_1_ports(self):
        ports = [Port('clk_i'   , 'clk_i'),
                 Port('rst_ni'  , 'rst_ni'),
                 Port('i_dvld'  , 'i_dvld'),
                 Port('i_rvld'  , 'i_rvld'),
                 Port('i_n'     , "i_n[{}+:{}]".format(self.list_par.ll_r_start*self.list_par.ll_width,self.list_par.ll_r_len*self.list_par.ll_width)),
                 Port('i_a'     , "i_a[{}+:{}]".format(self.list_par.ll_a_start*self.list_par.ll_width,self.list_par.ll_a_len*self.list_par.ll_width)),
                 Port('o_z'     , "x[{}+:{}]".format(0,self.list_par.ll_shares*self.list_par.ll_width)),
                 Port('o_dvld'  , "vll"),
        ]
        return ports



    def instance_expandx_ports(self):
        ports = [
                 Port('i_x' , "xd[{}+:{}]".format(0,self.list_par.ll_shares*self.list_par.ll_width)),
                 Port('o_xp', "xp[{}+:{}]".format(0,self.shares*self.width)),
        ]
        return ports



    def instance_convertaby_ports(self):
        ports = [Port('clk_i'   , 'clk_i'),
                 Port('rst_ni'  , 'rst_ni'),
                 Port('i_dvld'  , 'i_dvld'),
                 Port('i_rvld'  , 'i_rvld'),
                 Port('i_n'     , "i_n[{}+:{}]".format(self.list_par.rl_r_start*self.list_par.rl_width,self.list_par.rl_r_len*self.list_par.rl_width)),
                 Port('i_a'     , "i_a[{}+:{}]".format(self.list_par.rl_a_start*self.list_par.rl_width,self.list_par.rl_a_len*self.list_par.rl_width)),
                 Port('o_z'     , "y[{}+:{}]".format(0,self.list_par.rl_shares*self.list_par.rl_width)),
                 Port('o_dvld'  , "vrl"),
        ]
        return ports



    def instance_expandy_ports(self):
        ports = [
                 Port('i_x'     , "yd[{}+:{}]".format(0,self.list_par.rl_shares*self.list_par.rl_width)),
                 Port('o_xp'    , "yp[{}+:{}]".format(0,self.shares*self.width)),
        ]
        return ports



    def instance_ksa_0_ports(self):
        ports = [Port('clk_i'   , 'clk_i'),
                 Port('rst_ni'  , 'rst_ni'),
                 Port('i_dvld'  , 'vy'),
                 Port('i_rvld'  , 'i_rvld'),
                 Port('i_n'     , "i_n[{}+:{}]".format(self.list_par.ksa_r_start*self.width, self.list_par.ksa_r_len*self.width)),
                 Port('i_x'     , "xp[{}+:{}]".format(0,self.shares*self.width)),
                 Port('i_y'     , "yp[{}+:{}]".format(0,self.shares*self.width)),
                 Port('o_z'     , 'o_z[{}+:{}]'.format(0,self.shares*self.width)),
        ]
        return ports



    def instance_ksa_1_ports(self):
        ports = [Port('clk_i'   , 'clk_i'),
                 Port('rst_ni'  , 'rst_ni'),
                 Port('i_dvld'  , 'vy'),
                 Port('i_rvld'  , 'i_rvld'),
                 Port('i_n'     , "i_n[{}+:{}]".format(self.list_par.ksa_r_start*self.width, self.list_par.ksa_r_len*self.width)),
                 Port('i_x'     , "xp[{}+:{}]".format(0,self.shares*self.width)),
                 Port('i_y'     , "yp[{}+:{}]".format(0,self.shares*self.width)),
                 Port('o_z'     , 'o_z[{}+:{}]'.format(0,self.shares*self.width)),
                 Port('o_dvld'  , 'o_dvld'),
        ]
        return ports


 
    def write(self):

        file = self.output_file



        self.verilog_writer.add(ModulePort('clk_i'  , 'input'))
        self.verilog_writer.add(ModulePort('rst_ni', 'input'))
        self.sdc_writer.add_clock('clk_i', 0.18)



        ports = self.module_ports(self.shares, self.width, True)
        for port in ports:
            self.verilog_writer.add(port)      



        logics = self.module_logics()
        for logic in logics:
            self.verilog_writer.add(logic)



        # for (name, _dir, width) in self.my_ports():
        #     self.sdc_writer.add_port(name, _dir, width, 0)  
 

        #################################################################################
        # left leaf inst
        if self.list_par.ll_convert_name == "":
            raw  = ""
            if self.list_par.ll_exist_odvld == int(1):
                raw += add_comment("Connect i_dvld to left leaf valid")
                raw += assigns_1o1(logics[8].get_name(),ports[0].get_name() ,"", 1, 0, 1, 0)
            raw += add_comment("Connect input port to left leaf data")
            raw += assigns_ofs(logics[0].get_name(),ports[3].get_name() , 0, 1, self.list_par.ll_a_start, self.list_par.ll_width)
            self.verilog_writer.add(Raw(raw))            
        else:
            #################################################################################
            raw = ""
            raw += add_comment("Do ConvertAB(left leaf) instance")
            self.verilog_writer.add(Raw(raw)) 


            if self.list_par.ll_exist_odvld == int(1):
                inst_module_name    = "{}_1".format(self.list_par.ll_convert_name)
                inst_name           = "u{}_{}".format(self.inst_cnt, inst_module_name)
                self.inst_cnt       = self.inst_cnt + int(1)
                inst_parameters     = []                        
                inst_ports          = self.instance_convertabx_1_ports()
                inst_fraw           = ""
                inst_praw           = ""    
                self.verilog_writer.add(Instance(inst_module_name,
                                                 inst_name,
                                                 inst_parameters,
                                                 inst_ports,
                                                 inst_fraw,
                                                 inst_praw))  
            else:
                inst_module_name    = "{}_0".format(self.list_par.ll_convert_name)
                inst_name           = "u{}_{}".format(self.inst_cnt, inst_module_name)
                self.inst_cnt       = self.inst_cnt + int(1)
                inst_parameters     = []                        
                inst_ports          = self.instance_convertabx_0_ports()
                inst_fraw           = ""
                inst_praw           = ""    
                self.verilog_writer.add(Instance(inst_module_name,
                                                 inst_name,
                                                 inst_parameters,
                                                 inst_ports,
                                                 inst_fraw,
                                                 inst_praw))                  



        if self.list_par.ll_latency >= self.list_par.rl_latency:
            raw  = ""
            raw += add_comment("Connect left leaf data to Expand'input")
            raw += assigns_ofs(logics[1].get_name(), logics[0].get_name(), 0, 1, 0, self.list_par.ll_shares*self.list_par.ll_width)
            self.verilog_writer.add(Raw(raw))                    
        else:
            #################################################################################
            delay               = self.list_par.rl_latency - self.list_par.ll_latency            
            width               = self.list_par.ll_shares*self.list_par.ll_width

            raw = ""
            raw += add_comment("Delay left leaf")
            self.verilog_writer.add(Raw(raw)) 

            inst_module_name    = "lix_shr0"
            inst_name           = "u{}_lix_shr0".format(self.inst_cnt)
            self.inst_cnt       = self.inst_cnt + int(1)
            inst_parameters     = [ Parameter('W',"{}".format(width) ), Parameter('N','{}'.format(delay))]
            inst_ports          = instance_shr0(logics[8].get_name(), ports[1].get_name(), logics[0].get_name(), logics[1].get_name(), width, 0 )
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
        raw += add_comment("Do a Expand(left leaf) instance")
        self.verilog_writer.add(Raw(raw)) 


        inst_module_name    = self.list_par.ll_expand_name
        inst_name           = "u{}_{}".format(self.inst_cnt, self.list_par.ll_expand_name)
        self.inst_cnt       = self.inst_cnt + int(1)
        inst_parameters     = []                        
        inst_ports          = self.instance_expandx_ports()
        inst_fraw           = ""
        inst_praw           = ""    
        self.verilog_writer.add(Instance(inst_module_name,
                                         inst_name,
                                         inst_parameters,
                                         inst_ports,
                                         inst_fraw,
                                         inst_praw))  



        #################################################################################
        # right leaf inst
        if self.list_par.rl_convert_name == "":
            raw  = ""
            raw += add_comment("Connect i_dvld to right leaf valid")
            raw += assigns_1o1(logics[6].get_name(),ports[0].get_name() ,"", 1, 0, 1, 0)
            raw += add_comment("Connect input port to rifht leaf data")
            raw += assigns_ofs(logics[3].get_name(),ports[3].get_name() , 0, self.list_par.rl_a_len, self.list_par.rl_a_start, self.list_par.rl_width)
            self.verilog_writer.add(Raw(raw))            
        else:
            #################################################################################
            raw = ""
            raw += add_comment("Do ConvertAB(right leaf) instance")
            self.verilog_writer.add(Raw(raw)) 

            inst_module_name    = "{}_1".format(self.list_par.rl_convert_name)
            inst_name           = "u{}_{}".format(self.inst_cnt, inst_module_name)
            self.inst_cnt       = self.inst_cnt + int(1)
            inst_parameters     = []                        
            inst_ports          = self.instance_convertaby_ports()
            inst_fraw           = ""
            inst_praw           = ""    
            self.verilog_writer.add(Instance(inst_module_name,
                                             inst_name,
                                             inst_parameters,
                                             inst_ports,
                                             inst_fraw,
                                             inst_praw))  



        if self.list_par.rl_latency >= self.list_par.ll_latency:
            raw  = ""
            raw += add_comment("Connect right leaf valid to right leaf output")
            raw += assigns_1o1(logics[7].get_name(),logics[6].get_name() ,"", 1, 0, 1, 0)
            raw += add_comment("Connect right leaf data to Expand'input")
            raw += assigns_ofs(logics[4].get_name(), logics[3].get_name(), 0, 1, 0, self.list_par.rl_shares*self.list_par.rl_width)
            self.verilog_writer.add(Raw(raw))                    
        else:
            #################################################################################
            delay = self.list_par.rl_latency - self.list_par.ll_latency
            width = self.list_par.rl_shares*self.list_par.rl_width

            raw = ""
            raw += add_comment("Delay right leaf")
            self.verilog_writer.add(Raw(raw)) 

            inst_module_name    = "lix_shr1"
            inst_name           = "u{}_lix_shr1".format(self.inst_cnt)
            self.inst_cnt       = self.inst_cnt + int(1)
            inst_parameters     = [ Parameter('W',"{}".format(width) ), Parameter('N','{}'.format(delay))]
            inst_ports          = instance_shr1(logics[6].get_name(h), ports[1].get_name(), logics[3].get_name(), logics[9].get_name(), logics[4].get_name(), width, 0 )
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
        raw += add_comment("Do a Expand(right leaf) instance")
        self.verilog_writer.add(Raw(raw)) 
      

        inst_module_name    = self.list_par.rl_expand_name
        inst_name           = "u{}_{}".format(self.inst_cnt, self.list_par.rl_expand_name)
        self.inst_cnt       = self.inst_cnt + int(1)
        inst_parameters     = []                        
        inst_ports          = self.instance_expandy_ports()
        inst_fraw           = ""
        inst_praw           = ""    
        self.verilog_writer.add(Instance(inst_module_name,
                                         inst_name,
                                         inst_parameters,
                                         inst_ports,
                                         inst_fraw,
                                         inst_praw))  



        #################################################################################
        # ksa inst
        raw = ""
        raw += add_comment("Do a KSA instance")
        self.verilog_writer.add(Raw(raw)) 

        if self.list_par.exist_odvld == int(1):
            inst_module_name    = "{}_1".format(self.list_par.ksa_name)
            inst_name           = "u{}_{}".format(self.inst_cnt, inst_module_name)
            self.inst_cnt       = self.inst_cnt + int(1)
            inst_parameters     = []                        
            inst_ports          = self.instance_ksa_1_ports()
            inst_fraw           = ""
            inst_praw           = ""    
            self.verilog_writer.add(Instance(inst_module_name,
                                             inst_name,
                                             inst_parameters,
                                             inst_ports,
                                             inst_fraw,
                                             inst_praw)) 
        else:
            inst_module_name    = "{}_0".format(self.list_par.ksa_name)
            inst_name           = "u{}_{}".format(self.inst_cnt, inst_module_name)
            self.inst_cnt       = self.inst_cnt + int(1)
            inst_parameters     = []                        
            inst_ports          = self.instance_ksa_0_ports()
            inst_fraw           = ""
            inst_praw           = ""    
            self.verilog_writer.add(Instance(inst_module_name,
                                             inst_name,
                                             inst_parameters,
                                             inst_ports,
                                             inst_fraw,
                                             inst_praw))              


        
        #################################################################################
        self.verilog_writer.write(file)
        if self.list_par.id == int(0):
            self.sdc_writer.write()


