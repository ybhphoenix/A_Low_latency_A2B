#!/usr/bin/env python3
import math
import sys

from InstFun_Container import *
from Yaml_Loader import *
from Verilog_Writer import *



#################################################################################
 # class name       : Expand1
 # description      : generate Expand1 verilog file
 #                    
 # function         : @my_ports             : define the ports
 # function         : @module_ports         : get the module ports
 # function         : @write                : write file
 #       
 # input            : @name                 : the name             
 # input            : @n2                   : the shares n2
 # input            : @n                    : the shares n
 # input            : @width                : the width
 # returns          : this class
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
class Expand1:
    def __init__(self, name, n2, n, width):
        self.verilog_writer = VerilogWriter(name, True, False)
        self.name           = name
        self.n2             = n2
        self.n              = n
        self.width          = width
        self.output_file    = "{}.v".format(name)



    def my_ports(self):
        ports = [
            ("x"    , False , self.n2*self.width),
            ("xp"   , True  , self.n*self.width),  
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



    def write(self):

        file = self.output_file



        ports = self.module_ports(True)
        for port in ports:
            self.verilog_writer.add(port)      



        #################################################################################        
        raw  = ""
        raw += add_comment("for(i=0;i<{};i++)\n".format(self.n2)+"{\n  xp[i]=x[i];\n}")
        raw += assigns_ofs(ports[1].get_name(),ports[0].get_name() , 0, self.n2, 0, self.width)
        raw += add_comment("for(i={};i<{};i++)\n".format(self.n2, self.n)+"{"+"\n  xp[i]=0;\n"+"}")
        raw += assigns_zeros(ports[1].get_name(), self.n2, self.n, self.width) 
        raw += "\n\n"
        self.verilog_writer.add(Raw(raw))                  



        #################################################################################
        self.verilog_writer.write(file)


