#!/usr/bin/env python3
import math
import sys

from InstFun_Container import *
from Yaml_Loader import *
from Verilog_Writer import *



#################################################################################
 # class name       : SecAnd_PINI1
 # description      : generate SecAnd_PINI1 verilog file
 #                    
 # function         : @my_ports             : define the ports
 # function         : @module_ports         : get the module ports
 # function         : @get_rand_index       : get rand index
 # function         : @get_xy_index         : get xy index 
 # function         : @write                : write file
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
class SecAnd_PINI1:
    def __init__(self, name, shares, width, exist_odvld=int(1)):
        self.name           = "{}_{}".format(name, exist_odvld)         
        self.verilog_writer = VerilogWriter(self.name, True, False, False)
        self.shares         = shares
        self.width          = width
        self.exist_odvld    = exist_odvld
        self.output_file    = "{}.v".format(self.name)
        self.ports          = self.module_ports(self.shares, self.width, True)
        self.latency        = 2
        self.inst_cnt       = int(0)
        self.con_reg        = int(1)
        self.con_logic      = int(1)



    def my_ports(self, share, width):
        num_of_rand = get_num_of_rand(share)
        num_of_x_y  = share
        ports = [
            ("dvld" , False , 0),
            ("rvld" , False , 0),
            ("n"    , False , num_of_rand*width),
            ("x"    , False , num_of_x_y*width),
            ("y"    , False , num_of_x_y*width),
            ("c"    , True  , num_of_x_y*width),  
            ("dvld" , True  , 0),      
        ]
        return ports


    
    def module_ports(self, share, width, is_input):
        ports = []
        for (name, _dir, width) in self.my_ports(share, width):
            prefix = 'o' if is_input == _dir else 'i'
            if not (name =="dvld" and prefix =="o" and self.exist_odvld==int(0)):
                ports.append(ModulePort("{}_{}".format(prefix, name),
                                        'output' if is_input == _dir else 'input',
                                        width))
        return ports



    def get_rand_index(self,x,y):
        if self.shares==2 :
            list_2 = [[0,0], \
                      [0,0]]
            return list_2[x][y]
        elif self.shares==3 :
            list_3 = [[0,0,1], \
                      [0,0,2], \
                      [1,2,0]]
            return list_3[x][y]
        elif self.shares==4 :
            list_4 = [[0,0,1,2], \
                      [0,0,3,4], \
                      [1,3,0,5], \
                      [2,4,5,0]]
            return list_4[x][y]
        elif self.shares==5 :
            list_5 = [[0,0,1,2,3], \
                      [0,0,4,5,6], \
                      [1,4,0,7,8], \
                      [2,5,7,0,9], \
                      [3,6,8,9,0]]
            return list_5[x][y]
        elif self.shares==6 :
            list_6 = [[ 0, 0, 1, 2, 3, 4], \
                      [ 0, 0, 5, 6, 7, 8], \
                      [ 1, 5, 0, 9,10,11], \
                      [ 2, 6, 9, 0,12,13], \
                      [ 3, 7,10,12, 0,14], \
                      [ 4, 8,11,13,14, 0]]
            return list_6[x][y]
        elif self.shares==7 :
            list_7 = [[ 0, 0, 1, 2, 3, 4, 5], \
                      [ 0, 0, 6, 7, 8, 9,10], \
                      [ 1, 6, 0,11,12,13,14], \
                      [ 2, 7,11, 0,15,16,17], \
                      [ 3, 8,12,15, 0,18,19], \
                      [ 4, 9,13,16,18, 0,20], \
                      [ 5,10,14,17,19,20, 0]]
            return list_7[x][y]
        elif self.shares==8 :
            list_8 = [[ 0, 0, 1, 2, 3, 4, 5, 6], \
                      [ 0, 0, 7, 8, 9,10,11,12], \
                      [ 1, 7, 0,13,14,15,16,17], \
                      [ 2, 8,13, 0,18,19,20,21], \
                      [ 3, 9,14,18, 0,22,23,24], \
                      [ 4,10,15,19,22, 0,25,26], \
                      [ 5,11,16,20,23,25, 0,27], \
                      [ 6,12,17,21,24,26,27, 0]]
            return list_8[x][y]
        elif self.shares==9 :
            list_9 = [[ 0, 0, 1, 2, 3, 4, 5, 6, 7], \
                      [ 0, 0, 8, 9,10,11,12,13,14], \
                      [ 1, 8, 0,15,16,17,18,19,20], \
                      [ 2, 9,15, 0,21,22,23,24,25], \
                      [ 3,10,16,21, 0,26,27,28,29], \
                      [ 4,11,17,22,26, 0,30,31,32], \
                      [ 5,12,18,23,27,30, 0,33,34], \
                      [ 6,13,19,24,28,31,33, 0,35], \
                      [ 7,14,20,25,29,32,34,35, 0]]
            return list_9[x][y]
        elif self.shares==10:
            list_10= [[ 0, 0, 1, 2, 3, 4, 5, 6, 7, 8], \
                      [ 0, 0, 9,10,11,12,13,14,15,16], \
                      [ 1, 9, 0,17,18,19,20,21,22,23], \
                      [ 2,10,17, 0,24,25,26,27,28,29], \
                      [ 3,11,18,24, 0,30,31,32,33,34], \
                      [ 4,12,19,25,30, 0,35,36,37,38], \
                      [ 5,13,20,26,31,35, 0,39,40,41], \
                      [ 6,14,21,27,32,36,39, 0,42,43], \
                      [ 7,15,22,28,33,37,40,42, 0,44], \
                      [ 8,16,23,29,34,38,41,43,44, 0]]
            return list_10[x][y]
        else :
            return 0

    def get_xy_index(self,x,y):
        if self.shares==2 :
            list_2 = [[0,0], \
                      [1,0]]
            return list_2[x][y]
        elif self.shares==3 :
            list_3 = [[0,0,1], \
                      [2,0,3], \
                      [4,5,0]]
            return list_3[x][y]
        elif self.shares==4 :
            list_4 = [[ 0, 0, 1, 2], \
                      [ 3, 0, 4, 5], \
                      [ 6, 7, 0, 8], \
                      [ 9,10,11, 0]]
            return list_4[x][y]
        elif self.shares==5 :
            list_5 = [[ 0, 0, 1, 2, 3], \
                      [ 4, 0, 5, 6, 7], \
                      [ 8, 9, 0,10,11], \
                      [12,13,14, 0,15], \
                      [16,17,18,19, 0]]
            return list_5[x][y]
        elif self.shares==6 :
            list_6 = [[ 0, 0, 1, 2, 3, 4], \
                      [ 5, 0, 6, 7, 8, 9], \
                      [10,11, 0,12,13,14], \
                      [15,16,17, 0,18,19], \
                      [20,21,22,23, 0,24], \
                      [25,26,27,28,29, 0]]
            return list_6[x][y]
        elif self.shares==7 :
            list_7 = [[ 0, 0, 1, 2, 3, 4, 5], \
                      [ 6, 0, 7, 8, 9,10,11], \
                      [12,13, 0,14,15,16,17], \
                      [18,19,20, 0,21,22,23], \
                      [24,25,26,27, 0,28,29], \
                      [30,31,32,33,34, 0,35], \
                      [36,37,38,39,40,41, 0]]
            return list_7[x][y]
        elif self.shares==8 :
            list_8 = [[ 0, 0, 1, 2, 3, 4, 5, 6], \
                      [ 7, 0, 8, 9,10,11,12,13], \
                      [14,15, 0,16,17,18,19,20], \
                      [21,22,23, 0,24,25,26,27], \
                      [28,29,30,31, 0,32,33,34], \
                      [35,36,37,38,39, 0,40,41], \
                      [42,43,44,45,46,47, 0,48], \
                      [49,50,51,52,53,54,55, 0]]
            return list_8[x][y]
        elif self.shares==9 :
            list_9 = [[ 0, 0, 1, 2, 3, 4, 5, 6, 7], \
                      [ 8, 0, 9,10,11,12,13,14,15], \
                      [16,17, 0,18,19,20,21,22,23], \
                      [24,25,26, 0,27,28,29,30,31], \
                      [32,33,34,35, 0,36,37,38,39], \
                      [40,41,42,43,44, 0,45,46,47], \
                      [48,49,50,51,52,53, 0,54,55], \
                      [56,57,58,59,60,61,62, 0,63], \
                      [64,65,66,67,68,69,70,71, 0]]
            return list_9[x][y]
        elif self.shares==10:
            list_10= [[ 0, 0, 1, 2, 3, 4, 5, 6, 7, 8], \
                      [ 9, 0,10,11,12,13,14,15,16,17], \
                      [18,19, 0,20,21,22,23,24,25,26], \
                      [27,28,29, 0,30,31,32,33,34,35], \
                      [36,37,38,39, 0,40,41,42,43,44], \
                      [45,46,47,48,49, 0,50,51,52,53], \
                      [54,55,56,57,58,59, 0,60,61,62], \
                      [63,64,65,66,67,68,69, 0,70,71], \
                      [72,73,74,75,76,77,78,79, 0,80], \
                      [81,82,83,84,85,86,87,88,89, 0]]
            return list_10[x][y]
        else :
            return 0



    def write(self, fp_file_list = ""):

        file = self.output_file



        self.verilog_writer.add(ModulePort('clk_i'  , 'input'))
        self.verilog_writer.add(ModulePort('rst_ni' , 'input'))



        for port in self.ports:
            self.verilog_writer.add(port)        



        #################################################################################
        raw = ""


        # reg
        if self.con_reg == int(0):
            raw += "wire  vldd1;\n"
        else:
            raw += "(*DONT_TOUCH=\"YES\"*)(*KEEP=\"TRUE\"*)wire  vldd1;"
            raw += """// synopsys keep_signal_name "vldd1" \n"""
            #raw += "\n"
        

        
        # reg
        for i in range(0, self.shares):
            if self.con_reg == int(0):
                raw += "wire [{}:0] xd_{};\n".format(self.width-1,i)
            else:
                raw += "(*DONT_TOUCH=\"YES\"*)(*KEEP=\"TRUE\"*)wire [{}:0] xd_{};".format(self.width-1,i)
                raw += "// synopsys keep_signal_name \"xd_{}\"\n".format(i)
            #raw += "\n"



        # reg 
        for i in range(0, self.shares):
            if self.con_reg == int(0):
                raw += "wire [{}:0] yd_{};\n".format(self.width-1,i)  
            else:
                raw += "(*DONT_TOUCH=\"YES\"*)(*KEEP=\"TRUE\"*)wire [{}:0] yd_{};".format(self.width-1,i)   
                raw += "// synopsys keep_signal_name \"yd_{}\"\n".format(i)
            #raw += "\n"
        


        # reg
        for i in range(0, self.shares*(self.shares-1)):
            if self.con_reg == int(0):
                raw += "wire [{}:0] r_{};\n".format(self.width-1,i) 
            else:
                raw += "(*DONT_TOUCH=\"YES\"*)(*KEEP=\"TRUE\"*)wire [{}:0] r_{};".format(self.width-1,i) 
                raw += "// synopsys keep_signal_name \"r_{}\"\n".format(i)
            #raw += "\n"



        # logic
        for i in range(0, self.shares*(self.shares-1)):
            if self.con_logic == int(0):
                raw += "wire [{}:0] yxn_{};\n".format(self.width-1,i)
            else:
                raw += "(*DONT_TOUCH=\"YES\"*)(*KEEP=\"TRUE\"*)wire [{}:0] yxn_{};".format(self.width-1,i)
                raw += "// synopsys keep_signal_name \"yxn_{}\"\n".format(i)
            #raw += "\n"
        


        # reg
        for i in range(0, self.shares*(self.shares-1)):
            if self.con_reg == int(0):
                raw += "wire [{}:0] v_{};\n".format(self.width-1,i)
            else:
                raw += "(*DONT_TOUCH=\"YES\"*)(*KEEP=\"TRUE\"*)wire [{}:0] v_{};".format(self.width-1,i)
                raw += "// synopsys keep_signal_name \"v_{}\"\n".format(i)
            #raw += "\n"



        # reg
        if self.exist_odvld == int(1):
            if self.con_reg == int(0):
                raw += "wire vldd2;\n" 
            else:
                raw += "(*DONT_TOUCH=\"YES\"*)(*KEEP=\"TRUE\"*)wire vldd2;" 
                #raw += """// synopsys keep_signal_name "vldd2" \n"""
                raw += "\n"



        # logic
        for i in range(0, self.shares*(self.shares-1)):
            if self.con_logic == int(0):
                raw += "wire [{}:0] xdn_{};\n".format(self.width-1,i)
            else:
                raw += "(*DONT_TOUCH=\"YES\"*)(*KEEP=\"TRUE\"*)wire [{}:0] xdn_{};".format(self.width-1,i)
                raw += "// synopsys keep_signal_name \"xdn_{}\"\n".format(i)
            #raw += "\n"



        # logic
        for i in range(0, self.shares*(self.shares-1)):
            if self.con_logic == int(0):
                raw += "wire [{}:0] xar_{};\n".format(self.width-1,i)
            else:
                raw += "(*DONT_TOUCH=\"YES\"*)(*KEEP=\"TRUE\"*)wire [{}:0] xar_{};".format(self.width-1,i)
                raw += "// synopsys keep_signal_name \"xar_{}\"\n".format(i)
            #raw += "\n"



        # reg 
        for i in range(0, self.shares*(self.shares-1)):
            if self.con_reg == int(0):
                raw += "wire [{}:0] u_{};\n".format(self.width-1,i)            
            else:
                raw += "(*DONT_TOUCH=\"YES\"*)(*KEEP=\"TRUE\"*)wire [{}:0] u_{};".format(self.width-1,i)
                raw += "// synopsys keep_signal_name \"u_{}\"\n".format(i)
            #raw += "\n"



        # logic
        for  i in range(0, self.shares):
            if self.con_logic == int(0):
                raw += "wire [{}:0] xay_{};\n".format(self.width-1,i)
            else:
                raw += "(*DONT_TOUCH=\"YES\"*)(*KEEP=\"TRUE\"*)wire [{}:0] xay_{};".format(self.width-1,i)
                raw += "// synopsys keep_signal_name \"xay_{}\"\n".format(i)  
            #raw += "\n"


        # reg
        for  i in range(0, self.shares):
            if self.con_reg == int(0):
                raw += "wire [{}:0] k_{};\n".format(self.width-1,i)
            else:
                raw += "(*DONT_TOUCH=\"YES\"*)(*KEEP=\"TRUE\"*)wire [{}:0] k_{};".format(self.width-1,i)
                raw += "// synopsys keep_signal_name \"k_{}\"\n".format(i)  
            #raw += "\n"



        # logic
        for i in range(0, self.shares*(self.shares-1)):
            if self.con_logic == int(0):
                raw += "wire [{}:0] xav_{};\n".format(self.width-1,i)
            else:
                raw += "(*DONT_TOUCH=\"YES\"*)(*KEEP=\"TRUE\"*)wire [{}:0] xav_{};".format(self.width-1,i)
                raw += "// synopsys keep_signal_name \"xav_{}\"\n".format(i)  
            #raw += "\n" 



        # reg
        for i in range(0, self.shares*(self.shares-1)):
            if self.con_reg == int(0):
                raw += "wire [{}:0] t_{};\n".format(self.width-1,i)
            else:
                raw += "(*DONT_TOUCH=\"YES\"*)(*KEEP=\"TRUE\"*)wire [{}:0] t_{};".format(self.width-1,i)
                raw += "// synopsys keep_signal_name \"t_{}\"\n".format(i)  
            #raw += "\n"      
        


        # logic
        for i in range(0, self.shares*(self.shares-1)):
            if self.con_logic == int(0):
                raw += "wire [{}:0] z_{};\n".format(self.width-1,i)
            else:            
                raw += "(*DONT_TOUCH=\"YES\"*)(*KEEP=\"TRUE\"*)wire [{}:0] z_{};".format(self.width-1,i)
                raw += "// synopsys keep_signal_name \"z_{}\"\n".format(i) 
            #raw += "\n"



        # logic
        for i in range(0, self.shares*(self.shares-2)):
            if self.con_logic == int(0):
                raw += "wire [{}:0] zxz_{};\n".format(self.width-1,i)
            else:
                raw += "(*DONT_TOUCH=\"YES\"*)(*KEEP=\"TRUE\"*)wire [{}:0] zxz_{};".format(self.width-1,i)
                raw += "// synopsys keep_signal_name \"zxz_{}\"\n".format(i) 
            #raw += "\n"



        #################################################################################
        self.verilog_writer.add(Raw(raw))
        


        #################################################################################
        # delay i_dvld
        inst_module_name    = "lix_reg"
        inst_name           = "u{}_lix_reg".format(self.inst_cnt)
        self.inst_cnt       = self.inst_cnt + int(1)
        inst_parameters     = [ Parameter('W',"{}".format(1) ),]
        inst_ports          = instance_reg('1\'d1', 'i_rvld', 'i_dvld', 'vldd1')
        inst_fraw           = "\n// delay i_dvld\n"
        inst_praw           = ""    
        self.verilog_writer.add(Instance(inst_module_name,
                                         inst_name,
                                         inst_parameters,
                                         inst_ports,
                                         inst_fraw,
                                         inst_praw))



        #################################################################################
        # x delay
        for i in range(0, self.shares):
            inst_module_name    = "lix_reg"
            inst_name           = "u{}_lix_reg".format(self.inst_cnt)
            self.inst_cnt       = self.inst_cnt + int(1)
            inst_parameters     = [ Parameter('W',"{}".format(self.width) ),]
            inst_ports          = instance_reg('i_dvld', 'i_rvld', 'i_x[{}+:{}]'.format(i*self.width, self.width), 'xd_{}'.format(i))
            inst_fraw           = "\n// delay i_x[{}+:{}]\n".format(i*self.width, self.width)
            inst_praw           = ""   
            self.verilog_writer.add(Instance(inst_module_name,
                                             inst_name,
                                             inst_parameters,
                                             inst_ports,
                                             inst_fraw,
                                             inst_praw))



        #################################################################################
        # y delay
        for i in range(0, self.shares):
            inst_module_name    = "lix_reg"
            inst_name           = "u{}_lix_reg".format(self.inst_cnt)
            self.inst_cnt       = self.inst_cnt + int(1)
            inst_parameters     = [ Parameter('W',"{}".format(self.width) ),]
            inst_ports          = instance_reg('i_dvld', 'i_rvld', 'i_y[{}+:{}]'.format(i*self.width, self.width), 'yd_{}'.format(i))
            inst_fraw           = "\n// delay i_y[{}+:{}]\n".format(i*self.width, self.width)
            inst_praw           = ""   
            self.verilog_writer.add(Instance(inst_module_name,
                                             inst_name,
                                             inst_parameters,
                                             inst_ports,
                                             inst_fraw,
                                             inst_praw))



        #################################################################################
        # n delay
        for i in range(0, self.shares):
            for j in range(0, self.shares):
                if i != j:
                    inst_module_name    = "lix_reg"
                    inst_name           = "u{}_lix_reg".format(self.inst_cnt)
                    self.inst_cnt       = self.inst_cnt + int(1)
                    inst_parameters     = [ Parameter('W',"{}".format(self.width) ),]
                    inst_ports          = instance_reg('i_dvld', 'i_rvld', 'i_n[{}+:{}]'.format(self.get_rand_index(i,j)*self.width, self.width), 'r_{}'.format(self.get_xy_index(i,j)))
                    inst_fraw           = "\n// delay i_n{}\n".format(self.get_rand_index(i,j), self.width)
                    inst_praw           = ""   
                    self.verilog_writer.add(Instance(inst_module_name,
                                                     inst_name,
                                                     inst_parameters,
                                                     inst_ports,
                                                     inst_fraw,
                                                     inst_praw))



        #################################################################################
        # proc y xor n
        for i in range(0, self.shares):
            for j in range(0, self.shares):
                if i != j:
                    inst_module_name    = "lix_xor"
                    inst_name           = "u{}_lix_xor".format(self.inst_cnt)
                    self.inst_cnt       = self.inst_cnt + int(1)
                    inst_parameters     = [ Parameter('W',"{}".format(self.width) ),]
                    inst_ports          = instance_xor('i_y[{}+:{}]'.format(j*self.width, self.width), 'i_n[{}+:{}]'.format(self.get_rand_index(i,j)*self.width, self.width), 'yxn_{}'.format(self.get_xy_index(i,j)))
                    inst_fraw           = "\n// i_y[{}+:{}] ^ i_n[{}+:{}]\n".format(i*self.width, self.width, self.get_rand_index(i,j)*self.width, self.width)
                    inst_praw           = ""   
                    self.verilog_writer.add(Instance(inst_module_name,
                                                     inst_name,
                                                     inst_parameters,
                                                     inst_ports,
                                                     inst_fraw,
                                                     inst_praw))



        #################################################################################
        # delay y xor n, is v
        for i in range(0, self.shares):
            for j in range(0, self.shares):
                if i != j:
                    inst_module_name    = "lix_reg"
                    inst_name           = "u{}_lix_reg".format(self.inst_cnt)
                    self.inst_cnt       = self.inst_cnt + int(1)
                    inst_parameters     = [ Parameter('W',"{}".format(self.width) ),]
                    inst_ports          = instance_reg('i_dvld', 'i_rvld', 'yxn_{}'.format(self.get_xy_index(i,j)), 'v_{}'.format(self.get_xy_index(i,j)))
                    inst_fraw           = "\n// delay yxn_{}\n".format(self.get_xy_index(i,j))
                    inst_praw           = ""   
                    self.verilog_writer.add(Instance(inst_module_name,
                                                     inst_name,
                                                     inst_parameters,
                                                     inst_ports,
                                                     inst_fraw,
                                                     inst_praw))



        #################################################################################
        # delay vldd1
        if self.exist_odvld==int(1):
            inst_module_name    = "lix_reg"
            inst_name           = "u{}_lix_reg".format(self.inst_cnt)
            self.inst_cnt       = self.inst_cnt + int(1)
            inst_parameters     = [ Parameter('W',"{}".format(1) ),]
            inst_ports          = instance_reg('1\'d1', 'i_rvld', 'vldd1', 'vldd2')
            inst_fraw           = "\n// delay vldd1\n"
            inst_praw           = ""    
            self.verilog_writer.add(Instance(inst_module_name,
                                             inst_name,
                                             inst_parameters,
                                             inst_ports,
                                             inst_fraw,
                                             inst_praw))



        #################################################################################
        # proc ~x_d1
        for i in range(0, self.shares):
            inst_module_name    = "lix_not"
            inst_name           = "u{}_lix_not".format(self.inst_cnt)
            self.inst_cnt       = self.inst_cnt + int(1)
            inst_parameters     = [ Parameter('W',"{}".format(self.width) ),]
            inst_ports          = instance_not('xd_{}'.format(i), 'xdn_{}'.format(i))
            inst_fraw           = "\n// not  xd_{}\n".format(i)
            inst_praw           = ""   
            self.verilog_writer.add(Instance(inst_module_name,
                                             inst_name,
                                             inst_parameters,
                                             inst_ports,
                                             inst_fraw,
                                             inst_praw))



        #################################################################################
        # proc ~x_d1 & r
        for i in range(0, self.shares):
            for j in range(0, self.shares):
                if i != j:
                    inst_module_name    = "lix_and"
                    inst_name           = "u{}_lix_and".format(self.inst_cnt)
                    self.inst_cnt       = self.inst_cnt + int(1)
                    inst_parameters     = [ Parameter('W',"{}".format(self.width) ),]
                    inst_ports          = instance_and('xdn_{}'.format(i), 'r_{}'.format(self.get_xy_index(i,j)), 'xar_{}'.format(self.get_xy_index(i,j)))
                    inst_fraw           = "\n// ~xd_{} & r_{}\n".format(i, self.get_xy_index(i,j))
                    inst_praw           = ""   
                    self.verilog_writer.add(Instance(inst_module_name,
                                                     inst_name,
                                                     inst_parameters,
                                                     inst_ports,
                                                     inst_fraw,
                                                     inst_praw))



        #################################################################################
        # delay ~x_d1 & r, is u
        for i in range(0, self.shares):
            for j in range(0, self.shares):
                if i != j:
                    inst_module_name    = "lix_reg"
                    inst_name           = "u{}_lix_reg".format(self.inst_cnt)
                    self.inst_cnt       = self.inst_cnt + int(1)
                    inst_parameters     = [ Parameter('W',"{}".format(self.width) ),]
                    inst_ports          = instance_reg('vldd1', 'i_rvld', 'xar_{}'.format(self.get_xy_index(i,j)), 'u_{}'.format(self.get_xy_index(i,j)))
                    inst_fraw           = "\n// delay ~xd_{} & r_{}\n".format(self.get_xy_index(i,j), self.get_xy_index(i,j))
                    inst_praw           = ""   
                    self.verilog_writer.add(Instance(inst_module_name,
                                                     inst_name,
                                                     inst_parameters,
                                                     inst_ports,
                                                     inst_fraw,
                                                     inst_praw))



        #################################################################################
        # proc x_d1 & y_d1
        for i in range(0, self.shares):
            inst_module_name    = "lix_and"
            inst_name           = "u{}_lix_and".format(self.inst_cnt)
            self.inst_cnt       = self.inst_cnt + int(1)
            inst_parameters     = [ Parameter('W',"{}".format(self.width) ),]
            inst_ports          = instance_and('xd_{}'.format(i), 'yd_{}'.format(i), 'xay_{}'.format(i))
            inst_fraw           = "\n// xd_{} & yd_{}\n".format(i, i)
            inst_praw           = ""   
            self.verilog_writer.add(Instance(inst_module_name,
                                             inst_name,
                                             inst_parameters,
                                             inst_ports,
                                             inst_fraw,
                                             inst_praw))



        #################################################################################
        # delay x_d1 & y_d1, is k
        for i in range(0, self.shares):
            inst_module_name    = "lix_reg"
            inst_name           = "u{}_lix_reg".format(self.inst_cnt)
            self.inst_cnt       = self.inst_cnt + int(1)
            inst_parameters     = [ Parameter('W',"{}".format(self.width) ),]
            inst_ports          = instance_reg('vldd1', 'i_rvld', 'xay_{}'.format(i), 'k_{}'.format(i))
            inst_fraw           = "\n// delay xd_{} & yd_{}\n".format(i, i)
            inst_praw           = ""   
            self.verilog_writer.add(Instance(inst_module_name,
                                             inst_name,
                                             inst_parameters,
                                             inst_ports,
                                             inst_fraw,
                                             inst_praw))



        #################################################################################
        # proc x_d1 & v
        for i in range(0, self.shares):
            for j in range(0, self.shares):
                if i != j:
                    inst_module_name    = "lix_and"
                    inst_name           = "u{}_lix_and".format(self.inst_cnt)
                    self.inst_cnt       = self.inst_cnt + int(1)
                    inst_parameters     = [ Parameter('W',"{}".format(self.width) ),]
                    inst_ports          = instance_and('xd_{}'.format(i), 'v_{}'.format(self.get_xy_index(i,j)), 'xav_{}'.format(self.get_xy_index(i,j)))
                    inst_fraw           = "\n// xd_{} & v_{}\n".format(i, self.get_xy_index(i,j))
                    inst_praw           = ""   
                    self.verilog_writer.add(Instance(inst_module_name,
                                                     inst_name,
                                                     inst_parameters,
                                                     inst_ports,
                                                     inst_fraw,
                                                     inst_praw))



        #################################################################################
        # delay x_d1 & v, is t
        for i in range(0, self.shares):
            for j in range(0, self.shares):
                if i != j:
                    inst_module_name    = "lix_reg"
                    inst_name           = "u{}_lix_reg".format(self.inst_cnt)
                    self.inst_cnt       = self.inst_cnt + int(1)
                    inst_parameters     = [ Parameter('W',"{}".format(self.width) ),]
                    inst_ports          = instance_reg('vldd1', 'i_rvld', 'xav_{}'.format(self.get_xy_index(i,j)), 't_{}'.format(self.get_xy_index(i,j)))
                    inst_fraw           = "\n// delay xd_{} & v_{}\n".format(self.get_xy_index(i,j), self.get_xy_index(i,j))
                    inst_praw           = ""   
                    self.verilog_writer.add(Instance(inst_module_name,
                                                     inst_name,
                                                     inst_parameters,
                                                     inst_ports,
                                                     inst_fraw,
                                                     inst_praw))



        #################################################################################
        # proc u xor t, is z
        for i in range(0, self.shares):
            for j in range(0, self.shares):
                if i != j:
                    inst_module_name    = "lix_xor"
                    inst_name           = "u{}_lix_xor".format(self.inst_cnt)
                    self.inst_cnt       = self.inst_cnt + int(1)
                    inst_parameters     = [ Parameter('W',"{}".format(self.width) ),]
                    inst_ports          = instance_xor('u_{}'.format(self.get_xy_index(i,j)), 't_{}'.format(self.get_xy_index(i,j)), 'z_{}'.format(self.get_xy_index(i,j)))
                    inst_fraw           = "\n// u_{} ^ t_{}\n".format(self.get_xy_index(i,j), self.get_xy_index(i,j))
                    inst_praw           = ""   
                    self.verilog_writer.add(Instance(inst_module_name,
                                                     inst_name,
                                                     inst_parameters,
                                                     inst_ports,
                                                     inst_fraw,
                                                     inst_praw))




        #################################################################################
        # proc zxz_[i] ^= z[j]
        if self.shares > int(2):
            for i in range(0, self.shares):
                for j in range(0, self.shares-2):
                    if j == int(0):
                        inst_module_name    = "lix_xor"
                        inst_name           = "u{}_lix_xor".format(self.inst_cnt)
                        self.inst_cnt       = self.inst_cnt + int(1)
                        inst_parameters     = [ Parameter('W',"{}".format(self.width) ),]
                        inst_ports          = instance_xor('z_{}'.format(i*(self.shares-1)+j), 'z_{}'.format(i*(self.shares-1)+j+1), 'zxz_{}'.format(i*(self.shares-2)+j))
                        inst_fraw           = "\n// z_{} ^ z_{}\n".format(i*(self.shares-1)+j+1, i*(self.shares-1)+j)
                        inst_praw           = ""   
                        self.verilog_writer.add(Instance(inst_module_name,
                                                         inst_name,
                                                         inst_parameters,
                                                         inst_ports,
                                                         inst_fraw,
                                                         inst_praw))
                    else:
                        inst_module_name    = "lix_xor"
                        inst_name           = "u{}_lix_xor".format(self.inst_cnt)
                        self.inst_cnt       = self.inst_cnt + int(1)
                        inst_parameters     = [ Parameter('W',"{}".format(self.width) ),]
                        inst_ports          = instance_xor('z_{}'.format(i*(self.shares-1)+j+1), 'zxz_{}'.format(i*(self.shares-2)+j-1), 'zxz_{}'.format(i*(self.shares-2)+j))
                        inst_fraw           = "\n// z_{} ^ zxz_{}\n".format(i*(self.shares-1)+j+1, i*(self.shares-2)+j-1)
                        inst_praw           = ""   
                        self.verilog_writer.add(Instance(inst_module_name,
                                                         inst_name,
                                                         inst_parameters,
                                                         inst_ports,
                                                         inst_fraw,
                                                         inst_praw))




        #################################################################################
        # proc c
        for i in range(0, self.shares):
            if self.shares <= int(2):
                inst_module_name    = "lix_xor"
                inst_name           = "u{}_lix_xor".format(self.inst_cnt)
                self.inst_cnt       = self.inst_cnt + int(1)
                inst_parameters     = [ Parameter('W',"{}".format(self.width) ),]
                inst_ports          = instance_xor('k_{}'.format(i), 'z_{}'.format(i), 'o_c[{}+:{}]'.format(i*self.width,self.width))
                inst_fraw           = "\n// k_{} ^ z_{}\n".format(i, i)
                inst_praw           = ""   
                self.verilog_writer.add(Instance(inst_module_name,
                                                 inst_name,
                                                 inst_parameters,
                                                 inst_ports,
                                                 inst_fraw,
                                                 inst_praw))               

            else:
                inst_module_name    = "lix_xor"
                inst_name           = "u{}_lix_xor".format(self.inst_cnt)
                self.inst_cnt       = self.inst_cnt + int(1)
                inst_parameters     = [ Parameter('W',"{}".format(self.width) ),]
                inst_ports          = instance_xor('k_{}'.format(i), 'zxz_{}'.format((i+1)*(self.shares-2)-1), 'o_c[{}+:{}]'.format(i*self.width,self.width))
                inst_fraw           = "\n// k_{} ^ zxz_{}\n".format(i, (i+1)*(self.shares-2)-1)
                inst_praw           = ""   
                self.verilog_writer.add(Instance(inst_module_name,
                                                 inst_name,
                                                 inst_parameters,
                                                 inst_ports,
                                                 inst_fraw,
                                                 inst_praw))



        #################################################################################
        raw = "\n"
        if self.exist_odvld==int(1):
            raw += "assign o_dvld = vldd2;\n" 
            raw += "\n"        
        self.verilog_writer.add(Raw(raw))



        self.verilog_writer.write(file)



        #################################################################################
        if fp_file_list != "":
            fp_filelist.add(File(self.name, True, False, int(0)))
