#!/usr/bin/env python3
import math
import sys

from InstFun_Container import *
from Yaml_Loader import *
from Verilog_Writer import *



#################################################################################
 # class name       : SecKSA
 # description      : generate SecKSA verilog file
 #                    
 # function         : @my_ports                         : define the ports
 # function         : @my_signals                       : define the signals
 # function         : @module_ports                     : get the module ports
 # function         : @module_logics                    : get the module signals 
 # function         : @instance_SecAnd_0_ports          : define the SecAnd_PINI1 ports
 # function         : @instance_SecKSA_1l_ports         : define the SecKSA_1l ports
 # function         : @instance_SecAnd_1_0_ports        : define the SecAnd_PINI1 ports
 # function         : @instance_SecAnd_1_1_ports        : define the SecAnd_PINI1 ports
 # function         : @write                            : write file
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
class SecKSA:
    def __init__(self, name, shares, width, exist_odvld=int(1)):
        self.name           = "{}_{}".format(name, exist_odvld) 
        self.shares         = shares
        self.width          = width
        self.exist_odvld    = exist_odvld
        self.verilog_writer = VerilogWriter(self.name, True, False, False)        
        self.output_file    = "{}.v".format(self.name)
        self.W              = find_w(self.width)
        self.nrand          = get_num_of_rand(shares)
        self.wrand          = get_num_of_rand(shares)*width
        self.wxy            = shares*width
        self.latency        = self.W*2+4
        self.r_start        = int(0)
        self.r_len          = (2*self.W+2)*self.nrand
        self.inst_cnt       = int(0)



    def my_ports(self):
        ports = [
            ("dvld" , False , 0),
            ("rvld" , False , 0),
            ("n"    , False , self.r_len *self.width),
            ("x"    , False , self.shares*self.width),
            ("y"    , False , self.shares*self.width),
            ("z"    , True  , self.shares*self.width),  
            ("dvld" , True  , 0),      
        ]
        return ports



    def my_signals(self, share, width):
        num_of_x_y  = share
        W = self.W+1
        signals = [
            ("p"               , num_of_x_y*width),
            ("g"               , num_of_x_y*width),
            ("tmp"             , num_of_x_y*width),
            ("a"               , num_of_x_y*width),
            ("vld0"            , 0),
            ("vld"             , W*1),
            ("pl"              , W*num_of_x_y*width),
            ("gl"              , W*num_of_x_y*width),
            ("ga"              , num_of_x_y*width),
            ("xd"              , num_of_x_y*width),
            ("yd"              , num_of_x_y*width),
            ("gd"              , num_of_x_y*width),
            ("glw"             , num_of_x_y*width),
            ("glh"             , num_of_x_y*width),
            ("gals"            , num_of_x_y*width),
            ("pd"              , num_of_x_y*width),
            ("plh"             , num_of_x_y*width),
            ("vld{}".format(W), 0),
            ("xxy"             , num_of_x_y*width),
        ]
        return signals



    def module_ports(self, share, width, is_input):
        ports = []
        for (name, _dir, width) in self.my_ports():
            prefix = 'o' if is_input == _dir else 'i'
            if not (name =="dvld" and prefix =="o" and self.exist_odvld==int(0)):
                ports.append(ModulePort("{}_{}".format(prefix,name),
                                    'output' if is_input == _dir else 'input',
                                    width))
        return ports



    def module_logics(self, share, width):
        logics = []
        for (n, w) in self.my_signals(share, width):
            logics.append(Wire("{}".format(n), w))
        return logics


    
    def instance_SecAnd_0_ports(self, rand_idx):
        ports = [Port('clk_i'  , 'clk_i'),
                 Port('rst_ni' , 'rst_ni'),
                 Port('i_dvld' , 'i_dvld'),
                 Port('i_rvld' , 'i_rvld'),
                 Port('i_n'    , "i_n[{}+:{}]".format(rand_idx*self.wrand,self.wrand)),
                 Port('i_x'    , 'i_x'),
                 Port('i_y'    , 'i_y'),
                 Port('o_c'    , 'g'),
                 Port('o_dvld' , 'vld0'),
        ]
        return ports



    def instance_SecKSA_1l_ports(self, rand_idx, inst_idx, rand_ofst):
        ports = [Port('clk_i'  , 'clk_i'),
                 Port('rst_ni' , 'rst_ni'),
                 Port('i_dvld' , "vld[{}]".format(inst_idx)),
                 Port('i_rvld' , "i_rvld"),
                 Port('i_n'    , "i_n[{}+:{}]".format(rand_idx*self.wrand*2+rand_ofst,self.wrand*2)),
                 Port('i_p'    , "pl[{}+:{}]".format(inst_idx*self.wxy,self.wxy)),
                 Port('i_g'    , "gl[{}+:{}]".format(inst_idx*self.wxy,self.wxy)),
                 Port('o_p'    , "pl[{}+:{}]".format((inst_idx+1)*self.wxy,self.wxy)),
                 Port('o_g'    , "gl[{}+:{}]".format((inst_idx+1)*self.wxy,self.wxy)),
                 Port('o_dvld' , "vld[{}]".format((inst_idx+1))),
        ]
        return ports



    def instance_SecAnd_1_0_ports(self, rand_idx, inst_idx, rand_ofst):
        ports = [Port('clk_i'  , 'clk_i'),
                 Port('rst_ni' , 'rst_ni'),
                 Port('i_dvld' , 'vld[{}]'.format(self.W)),
                 Port('i_rvld' , "i_rvld"),
                 Port('i_n'    , "i_n[{}+:{}]".format(rand_idx*self.wrand+rand_ofst,self.wrand)),
                 Port('i_x'    , "plh[{}+:{}]".format(inst_idx*self.wxy,self.wxy)),
                 Port('i_y'    , 'tmp[{}+:{}]'.format(0*self.wxy,self.wxy)),
                 Port('o_c'    , 'a[{}+:{}]'.format(0*self.wxy,self.wxy)),
        ]
        return ports



    def instance_SecAnd_1_1_ports(self, rand_idx, inst_idx, rand_ofst):
        ports = [Port('clk_i'  , 'clk_i'),
                 Port('rst_ni' , 'rst_ni'),
                 Port('i_dvld' , 'vld[{}]'.format(self.W)),
                 Port('i_rvld' , "i_rvld"),
                 Port('i_n'    , "i_n[{}+:{}]".format(rand_idx*self.wrand+rand_ofst,self.wrand)),
                 Port('i_x'    , "plh[{}+:{}]".format(inst_idx*self.wxy,self.wxy)),
                 Port('i_y'    , 'tmp[{}+:{}]'.format(0*self.wxy,self.wxy)),
                 Port('o_c'    , 'a[{}+:{}]'.format(0*self.wxy,self.wxy)),
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
        raw += add_comment("p[i]=x[i]^y[i];")
        self.verilog_writer.add(Raw(raw))

        inst_module_name    = "lix_xor"
        inst_name           = "u{}_lix_xor".format(self.inst_cnt)
        self.inst_cnt       = self.inst_cnt + int(1)
        inst_parameters     = [ Parameter('W',"{}".format(self.shares*self.width) ),]
        inst_ports          = instance_xor(ports[3].get_name(), ports[4].get_name(), logics[0].get_name())
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
        raw += add_comment("Delay p")
        self.verilog_writer.add(Raw(raw))


        inst_module_name    = "lix_shr0"
        inst_name           = "u{}_lix_shr0".format(self.inst_cnt)
        self.inst_cnt       = self.inst_cnt + int(1)
        inst_parameters     = [ Parameter('W',"{}".format(self.width*self.shares) ), Parameter('N',"2")]
        inst_ports          = instance_shr0(ports[0].get_name(), ports[1].get_name(), logics[0].get_name(), logics[15].get_name())
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
        raw += add_comment("Do a SecAnd instance")
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
        raw += add_comment("Connect SecAnd'output to KSA_w1l'input")
        raw += assigns_1o1("vld[0]","vld0" ,"",1,0,1,0) 
        raw += add_comment("Connect delayed p to KSA_w1l'input")
        raw += assigns_1o1(logics[6].get_name(),logics[15].get_name() ,"",1,0,1,self.shares*self.width)
        raw += add_comment("Connect SecAnd'output to KSA_w1l'input")        
        raw += assigns_1o1(logics[7].get_name(),logics[1].get_name() ,"",1,0,1,self.shares*self.width)        
        self.verilog_writer.add(Raw(raw)) 


        for i in range(0,self.W):
            #################################################################################
            raw  = ""
            raw += add_comment("Do a SecKSA_1l instance with SHIFT={}".format(i))
            self.verilog_writer.add(Raw(raw))

            inst_module_name    = "SecKSA_1l_n{}k{}".format(self.shares, self.width)
            inst_name           = "u{}_{}".format(self.inst_cnt, inst_module_name)
            self.inst_cnt       = self.inst_cnt + int(1)            
            inst_parameters     = [ Parameter('SHIFT',"{}".format(i) ),]
            inst_ports          = self.instance_SecKSA_1l_ports(i,i,self.wrand)
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
        raw += add_comment("Connect SecKSA_1l to delay module")
        raw += assigns_ofs(logics[13].get_name(),logics[7].get_name(),0,1,self.W,self.shares*self.width)
        raw += add_comment("Connect SecKSA_1l to SecAnd")
        raw += assigns_ofs(logics[16].get_name(),logics[6].get_name(),0,1,self.W,self.shares*self.width)
        raw += add_comment("Connect SecKSA_1l to delay module")
        raw += assigns_ofs(logics[17].get_name(),logics[5].get_name(self.W),0,1,self.W,0)
        raw += add_comment("Connect SecKSA_1l to SecAnd with left shift\ntmp[i]=(g[i]<<(1<<W))&MASK;")
        raw += assigns_1o1(logics[2].get_name(),logics[13].get_name() ," << ",2**self.W,0,self.shares,self.width)     
        self.verilog_writer.add(Raw(raw))    



        #################################################################################
        raw  = ""
        raw += add_comment("Delay SecKSA_1l'output")
        self.verilog_writer.add(Raw(raw))


        inst_module_name    = "lix_shr0"
        inst_name           = "u{}_lix_shr0".format(self.inst_cnt)
        self.inst_cnt       = self.inst_cnt + int(1)
        inst_parameters     = [ Parameter('W',"{}".format(self.width*self.shares) ), Parameter('N',"2")]
        inst_ports          = instance_shr0(logics[17].get_name(), ports[1].get_name(), logics[13].get_name(), logics[11].get_name())
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
        raw += add_comment("Do a SecAnd instance")
        self.verilog_writer.add(Raw(raw))


        if self.exist_odvld == int(1):
            inst_module_name    = "SecAnd_PINI1_n{}k{}_1".format(self.shares, self.width)
            inst_name           = "u{}_{}".format(self.inst_cnt, inst_module_name)
            self.inst_cnt       = self.inst_cnt + int(1)        
            inst_parameters     = []
            inst_ports          = self.instance_SecAnd_1_1_ports(0, 0, self.wrand*(self.W*2+1))
            inst_fraw           = "";
            inst_praw           = "";
            self.verilog_writer.add(Instance(inst_module_name,
                                             inst_name,
                                             inst_parameters,
                                             inst_ports,
                                             inst_fraw,
                                             inst_praw))      
        else:
            inst_module_name    = "SecAnd_PINI1_n{}k{}_0".format(self.shares, self.width)
            inst_name           = "u{}_{}".format(self.inst_cnt, inst_module_name)
            self.inst_cnt       = self.inst_cnt + int(1)        
            inst_parameters     = []
            inst_ports          = self.instance_SecAnd_1_0_ports(0, 0, self.wrand*(self.W*2+1))
            inst_fraw           = "";
            inst_praw           = "";
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
        inst_ports          = instance_xor(logics[11].get_name(), logics[3].get_name(), logics[8].get_name())
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
        raw += add_comment("Delay i_x;")
        self.verilog_writer.add(Raw(raw))

        inst_module_name    = "lix_shr0"
        inst_name           = "u{}_lix_shr0".format(self.inst_cnt)
        self.inst_cnt       = self.inst_cnt + int(1)
        inst_parameters     = [ Parameter('W',"{}".format(self.width*self.shares) ), Parameter('N',"{}".format(self.W*2+4))]
        inst_ports          = instance_shr0(ports[0].get_name(), ports[1].get_name(), ports[3].get_name(), logics[9].get_name())
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
        raw += add_comment("Delay i_y;")
        self.verilog_writer.add(Raw(raw))


        inst_module_name    = "lix_shr0"
        inst_name           = "u{}_lix_shr0".format(self.inst_cnt)
        self.inst_cnt       = self.inst_cnt + int(1)
        inst_parameters     = [ Parameter('W',"{}".format(self.width*self.shares) ), Parameter('N',"{}".format(self.W*2+4))]
        inst_ports          = instance_shr0(ports[0].get_name(), ports[1].get_name(), ports[4].get_name(), logics[10].get_name())
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
        raw += add_comment("(g[i]<<1))")
        raw += assigns_1o1(logics[14].get_name(),logics[8].get_name() ," << ",1,0,self.shares,self.width)
        self.verilog_writer.add(Raw(raw))   



        #################################################################################
        raw  = ""
        raw += add_comment("x[i]^y[i]")
        self.verilog_writer.add(Raw(raw))

        inst_module_name    = "lix_xor"
        inst_name           = "u{}_lix_xor".format(self.inst_cnt)
        self.inst_cnt       = self.inst_cnt + int(1)
        inst_parameters     = [ Parameter('W',"{}".format(self.shares*self.width) ),]
        inst_ports          = instance_xor(logics[9].get_name(), logics[10].get_name(), logics[18].get_name())
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
        raw += add_comment("z[i]=(x[i]^y[i]^(g[i]<<1))&MASK;")
        self.verilog_writer.add(Raw(raw))   

        inst_module_name    = "lix_xor"
        inst_name           = "u{}_lix_xor".format(self.inst_cnt)
        self.inst_cnt       = self.inst_cnt + int(1)
        inst_parameters     = [ Parameter('W',"{}".format(self.shares*self.width) ),]
        inst_ports          = instance_xor(logics[14].get_name(), logics[18].get_name(), ports[5].get_name())
        inst_fraw           = ""
        inst_praw           = ""   
        self.verilog_writer.add(Instance(inst_module_name,
                                         inst_name,
                                         inst_parameters,
                                         inst_ports,
                                         inst_fraw,
                                         inst_praw))  


        self.verilog_writer.write(file)


