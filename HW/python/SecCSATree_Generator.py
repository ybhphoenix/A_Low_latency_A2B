#!/usr/bin/env python3
import math
import sys

from InstFun_Container import *
from Yaml_Loader import *
from Verilog_Writer import *




#################################################################################
 # class name       : SecCSATree
 # description      : generate SecCSATree verilog file
 #                    
 # function         : @my_ports                 : define the ports
 # function         : @module_ports             : get the module ports
 # function         : @module_logics            : define the module signals 
 # function         : @instance_CSATree_ports   : define the CSATree ports
 # function         : @instance_csa_ports       : define the SecCSA ports
 # function         : @write                    : write file
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
class SecCSATree:
    def __init__(self, name, shares, width, list_par):
        self.verilog_writer = VerilogWriter(name, True, False, False)
        self.name           = name
        self.shares         = shares
        self.width          = width
        self.output_file    = "{}.v".format(name)
        self.list_par       = list_par
        self.inst_cnt       = int(0)



    def my_ports(self):
        ports = [
            ("dvld" , False , 0),
            ("rvld" , False , 0),
            ("n"    , False , self.list_par.r_len*self.width),
            ("x"    , False , self.shares*self.width),
            ("s"    , True  , self.shares*self.width),  
            ("c"    , True  , self.shares*self.width),             
            ("dvld" , True  , 0),      
        ]
        return ports



    def module_ports(self,share, width, is_input):
        ports = []
        for (name, _dir, width) in self.my_ports():
            prefix = 'o' if is_input == _dir else 'i'
            ports.append(ModulePort("{}_{}".format(prefix,name),
                                'output' if is_input == _dir else 'input',
                                width))
        return ports



    def module_logics(self):
        logics = []
        if self.list_par.shares > int(1):
            logics.append(Wire("y1"     , self.list_par.shares*self.list_par.width))
            logics.append(Wire("y2"     , self.list_par.shares*self.list_par.width))
            logics.append(Wire("y3"     , self.list_par.shares*self.list_par.width))
            logics.append(Wire("vc"     , 0))
            if self.shares > int(3):     
                logics.append(Wire("xd"     , self.list_par.width))                   
                logics.append(Wire("s"      , self.list_par.csa_shares*self.list_par.csa_width))
                logics.append(Wire("c"      , self.list_par.csa_shares*self.list_par.csa_width))
        return logics
  


    def instance_CSATree_ports(self):
        ports = [Port('clk_i'  , 'clk_i'),
                 Port('rst_ni' , 'rst_ni'),
                 Port('i_dvld' , 'i_dvld'),
                 Port('i_rvld' , 'i_rvld'),
                 Port('i_n'    , "i_n[{}+:{}]".format(self.list_par.tree_r_start*self.list_par.width,self.list_par.tree_r_len*self.list_par.width)),
                 Port('i_x'    , "i_x[{}+:{}]".format(0,(self.list_par.shares-1)*self.list_par.width)),
                 Port('o_s'    , "s"),                 
                 Port('o_c'    , "c"),
                 Port('o_dvld' , "vc"),
        ]
        return ports



    def instance_csa_ports(self):
        ports = [Port('clk_i'  , 'clk_i'),
                 Port('rst_ni' , 'rst_ni'),
                 Port('i_dvld' , 'vc'),
                 Port('i_rvld' , 'i_rvld'),
                 Port('i_n'    , "i_n[{}+:{}]".format(self.list_par.csa_r_start*self.list_par.width, self.list_par.csa_r_len*self.list_par.width)),
                 Port('i_x'    , "y1"),
                 Port('i_y'    , "y2"),
                 Port('i_c_in' , "y3"),
                 Port('o_s'    , "o_s"),                 
                 Port('o_c'    , "o_c"),
                 Port('o_dvld' , "o_dvld"),
        ]
        return ports


 
    def write(self):

        file = self.output_file



        self.verilog_writer.add(ModulePort('clk_i'  , 'input'))
        self.verilog_writer.add(ModulePort('rst_ni', 'input'))



        ports = self.module_ports(self.shares, self.width, True)
        for port in ports:
            self.verilog_writer.add(port)      



        logics = self.module_logics()
        for logic in logics:
            self.verilog_writer.add(logic)



        if self.list_par.tree_name == "":
            #################################################################################
            raw  = ""
            raw += add_comment("y1[0]= x[0];\ny1[1]= 0;\ny1[2]= 0;")
            for i in range(0, 3):
                if i == int(0):
                    raw += "assign y1[{}+:{}] = i_x[{}+:{}];\n".format(i*self.width, self.width, i*self.width, self.width)
                else:
                    raw += "assign y1[{}+:{}] = {}'d0;\n".format(i*self.width, self.width, self.width)
            raw += add_comment("y2[0]= 0;\ny2[1]= x[1];\ny2[2]= 0;")
            for i in range(0, 3):
                if i == int(1):
                    raw += "assign y2[{}+:{}] = i_x[{}+:{}];\n".format(i*self.width, self.width, i*self.width, self.width)
                else:
                    raw += "assign y2[{}+:{}] = {}'d0;\n".format(i*self.width, self.width, self.width)
            raw += add_comment("y3[0]= 0;\ny3[1]= 0;\ny3[2]= x[2];")
            for i in range(0, 3):
                if i == int(2):
                    raw += "assign y3[{}+:{}] = i_x[{}+:{}];\n".format(i*self.width, self.width, i*self.width, self.width)
                else:
                    raw += "assign y3[{}+:{}] = {}'d0;\n".format(i*self.width, self.width, self.width)
            self.verilog_writer.add(Raw(raw))

            raw  = ""
            raw += add_comment("connect i_dvld to csa valid")
            raw += "assign vc = i_dvld;\n"
            self.verilog_writer.add(Raw(raw))



            #################################################################################
            raw = ""
            raw += add_comment("Do SecCSA instance")
            self.verilog_writer.add(Raw(raw)) 

            inst_module_name    = self.list_par.csa_name
            inst_name           = "u{}_{}".format(self.inst_cnt, self.list_par.csa_name)
            self.inst_cnt       = self.inst_cnt + int(1)
            inst_parameters     = []                        
            inst_ports          = self.instance_csa_ports()
            inst_fraw           = ""
            inst_praw           = ""    
            self.verilog_writer.add(Instance(inst_module_name,
                                             inst_name,
                                             inst_parameters,
                                             inst_ports,
                                             inst_fraw,
                                             inst_praw)) 

        else:
            #################################################################################
            raw = ""
            raw += add_comment("Do SecCSAtree instance")
            self.verilog_writer.add(Raw(raw)) 

            inst_module_name    = self.list_par.tree_name
            inst_name           = "u{}_{}".format(self.inst_cnt, self.list_par.tree_name)
            self.inst_cnt       = self.inst_cnt + int(1)
            inst_parameters     = []                        
            inst_ports          = self.instance_CSATree_ports()
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
            raw += add_comment("Do pipeline instance")
            self.verilog_writer.add(Raw(raw)) 

            x_start             = (self.list_par.shares-1)*self.list_par.width
            x_width             = self.list_par.width
            inst_module_name    = "lix_shr0"
            inst_name           = "u{}_lix_shr0".format(self.inst_cnt)
            self.inst_cnt       = self.inst_cnt + int(1)
            inst_parameters     = [ Parameter('W',"{}".format(x_width) ), Parameter('N',"{}".format(self.list_par.tree_latency))]
            inst_ports          = instance_shr0(ports[0].get_name(), ports[1].get_name(), ports[3].get_name(), logics[4].get_name(), x_width, x_start )
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
            raw += add_comment("for(i=0;i<n-1;i++) y1[i]=s[i];\ny1[n-1]=0;")
            for i in range(0, self.list_par.shares):
                if i < self.list_par.shares - int(1):
                    raw += "assign y1[{}+:{}] = s[{}+:{}];\n".format(i*self.width, self.width, i*self.width, self.width)
                else:
                    raw += "assign y1[{}+:{}] = {}'d0;\n".format(i*self.width, self.width, self.width)
            raw += add_comment("for(i=0;i<n-1;i++) y2[i]=c[i];\ny2[n-1]=0;")
            for i in range(0, self.list_par.shares):
                if i < self.list_par.shares - int(1):
                    raw += "assign y2[{}+:{}] = c[{}+:{}];\n".format(i*self.width, self.width, i*self.width, self.width)
                else:
                    raw += "assign y2[{}+:{}] = {}'d0;\n".format(i*self.width, self.width, self.width)
            raw += add_comment("for(i=0;i<n-1;i++) y3[i]=0;\ny3[n-1]=x[n-1];")
            for i in range(0, self.list_par.shares):
                if i < self.list_par.shares - int(1):
                    raw += "assign y3[{}+:{}] = {}'d0;\n".format(i*self.width, self.width, self.width) 
                else:
                    raw += "assign y3[{}+:{}] = xd[{}+:{}];\n".format(i*self.width, self.width, 0*self.width, self.width)
            self.verilog_writer.add(Raw(raw))



            #################################################################################
            raw = ""
            raw += add_comment("Do SecCSA instance")
            self.verilog_writer.add(Raw(raw)) 

            inst_module_name    = self.list_par.csa_name
            inst_name           = "u{}_{}".format(self.inst_cnt, self.list_par.csa_name)
            self.inst_cnt       = self.inst_cnt + int(1)
            inst_parameters     = []                        
            inst_ports          = self.instance_csa_ports()
            inst_fraw           = ""
            inst_praw           = ""    
            self.verilog_writer.add(Instance(inst_module_name,
                                             inst_name,
                                             inst_parameters,
                                             inst_ports,
                                             inst_fraw,
                                             inst_praw)) 


        

        self.verilog_writer.write(file)


