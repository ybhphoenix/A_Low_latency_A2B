#!/usr/bin/env python3
import math
import sys


from InstFun_Container import *
from Yaml_Loader import *
from Verilog_Writer import *
from Sdc_Writer import SdcWriter



#################################################################################
 # class name       : SecA2B
 # description      : generate SecA2B verilog file
 #                    
 # function         : @find_CSAW                : find the number of ramdom for SecCSA
 # function         : @my_ports                 : define the ports
 # function         : @module_ports             : get the module ports
 # function         : @module_logics            : define the module signals 
 # function         : @instance_csatree_ports   : define the SecCSA ports
 # function         : @instance_ksa_ports       : define the SecKSA ports
 # function         : @write                    : write file
 #       
 # input            : @name                 : the name             
 # input            : @shares               : the shares
 # input            : @width                : the width
 # input            : @list_par             : the instance parameter list
 # returns          : this class
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
class SecA2B:
    def __init__(self, name, shares, width, list_par):
        self.name           = "{}_{}".format(name, list_par.exist_odvld)        
        self.verilog_writer = VerilogWriter(self.name, True, False, False)
        self.sdc_writer     = SdcWriter(self.name)
        self.shares         = shares
        self.width          = width
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



    def module_ports(self, is_input):
        ports = []
        for (name, _dir, width) in self.my_ports():
            prefix = 'o' if is_input == _dir else 'i'
            ports.append(ModulePort("{}_{}".format(prefix,name),
                                'output' if is_input == _dir else 'input',
                                width))
        return ports



    def module_logics(self):
        logics = []
        if self.shares > int(1):
            logics.append(Wire("s"     , self.shares*self.width))
            logics.append(Wire("c"     , self.shares*self.width))
            logics.append(Wire("vk"    , 0))
        return logics



    def instance_csatree_ports(self):
        ports = [Port('clk_i'  , 'clk_i'),
                 Port('rst_ni' , 'rst_ni'),
                 Port('i_dvld' , 'i_dvld'),
                 Port('i_rvld' , 'i_rvld'),
                 Port('i_n'    , "i_n[{}+:{}]".format(self.list_par.tree_r_start*self.width,self.list_par.tree_r_len*self.width)),
                 Port('i_x'    , "i_a"),
                 Port('o_s'    , "s"),                 
                 Port('o_c'    , "c"),
                 Port('o_dvld' , "vk"),
        ]
        return ports



    def instance_ksa_ports(self):
        ports = [Port('clk_i'  , 'clk_i'),
                 Port('rst_ni' , 'rst_ni'),
                 Port('i_dvld' , 'vk'),
                 Port('i_rvld' , 'i_rvld'),
                 Port('i_n'    , "i_n[{}+:{}]".format(self.list_par.ksa_r_start*self.width, self.list_par.ksa_r_len*self.width)),
                 Port('i_x'    , "s"),
                 Port('i_y'    , 'c'),
                 Port('o_z'    , 'o_z'),
                 Port('o_dvld' , 'o_dvld'),
        ]
        return ports

 

    def write(self):

        file = self.output_file



        self.verilog_writer.add(ModulePort('clk_i'  , 'input'))
        


        self.verilog_writer.add(ModulePort('rst_ni' , 'input'))
        


        self.sdc_writer.add_clock('clk_i', 0.18)



        ports = self.module_ports(True)
        for port in ports:
            self.verilog_writer.add(port) 


        logics = self.module_logics()
        for logic in logics:
            self.verilog_writer.add(logic)


        # for (name, _dir, width) in self.my_ports():
        #     self.sdc_writer.add_port(name, _dir, width, 0)     


        if self.shares <= int(1):
            raw  = ""
            raw += add_comment("z[0]=A[0];\nreturn;")
            raw += "assign o_z = i_a;\n"
            self.verilog_writer.add(Raw(raw))
        else:
            if self.shares == int(2):
                raw  = ""
                raw += add_comment("s[0]=A[0];\ns[1]=0;\nc[0]=0;\nc[1]=A[1];")
                raw += "assign s[{}+:{}] = i_a[{}+:{}];\n".format(self.width*0, self.width, self.width*0, self.width)
                raw += "assign s[{}+:{}] = {}'d0;\n".format(self.width*1, self.width, self.width)
                raw += "assign c[{}+:{}] = {}'d0;\n".format(self.width*0, self.width, self.width)
                raw += "assign c[{}+:{}] = i_a[{}+:{}];\n".format(self.width*1, self.width, self.width*1, self.width)
                raw += add_comment("Connect i_dvld to ksa vld")
                raw += "assign vk = i_dvld;\n"
                self.verilog_writer.add(Raw(raw))
            else: 
                #################################################################################
                raw = ""
                raw += add_comment("Do SecCSAtree instance")
                self.verilog_writer.add(Raw(raw)) 

                inst_module_name    = self.list_par.csatree_list.name
                inst_name           = "u{}_{}".format(self.inst_cnt, inst_module_name)
                self.inst_cnt       = self.inst_cnt + int(1)
                inst_parameters     = []                        
                inst_ports          = self.instance_csatree_ports()
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
            raw += add_comment("Do SecKSA instance")
            self.verilog_writer.add(Raw(raw)) 

            inst_module_name    = self.list_par.ksa_list.name
            inst_name           = "u{}_{}".format(self.inst_cnt, inst_module_name)
            self.inst_cnt       = self.inst_cnt + int(1)
            inst_parameters     = []                        
            inst_ports          = self.instance_ksa_ports()
            inst_fraw           = ""
            inst_praw           = ""    
            self.verilog_writer.add(Instance(inst_module_name,
                                             inst_name,
                                             inst_parameters,
                                             inst_ports,
                                             inst_fraw,
                                             inst_praw)) 



        self.verilog_writer.write(file)



        self.sdc_writer.write()


