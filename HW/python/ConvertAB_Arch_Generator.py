#!/usr/bin/env python3
import math
import sys

from InstFun_Container import *
from FileList_Generator import *
from ConvertAB_Generator import *
from Expand1_Generator import *
from Expand2_Generator import *
from SecAnd_PINI1_Generator import SecAnd_PINI1
from SecKSA_1l_Generator import SecKSA_1l
from SecKSA_Generator import SecKSA



#################################################################################
 # class name       : ConvertAB_arch
 # description      : 1. Initialize the parameters of ConvertAB architecutre
 #                    2. write files
 #
 # function         : @exist_ll_odvld       : if left leaf need o_dvld
 # function         : @add_left_leaf        : add left leaf for this tree
 # function         : @add_right_leaf       : add right leaf for this tree
 # function         : @show_left_leaf       : print left leaf to console
 # function         : @show_right_leaf      : print right leaf to console 
 # function         : @showtree             : print trunk to concole
 # function         : @write_left_leaf      : write left leaf to file
 # function         : @write_right_leaf     : write right leaf to file
 # function         : @write                : write trunk to file
 #       
 # input            : @name                 : the name             
 # input            : @shares               : the shares
 # input            : @width                : the width
 # input            : @iter_depth           : the depth of iteration
 # returns          : this class
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
class ConvertAB_arch:
    def __init__(self, shares, width, iter_depth, exist_odvld=int(1)):
        self.name             = "ConvertAB_n{}k{}".format(shares, width)        
        self.shares           = shares
        self.width            = width
        self.id               = iter_depth   
        self.exist_odvld      = exist_odvld
        self.ksa_w            = find_w(self.width)
        self.n_r              = get_num_of_rand(self.shares)
             
        self.ll_convert_name  = ""
        self.ll_expand_name   = ""
        self.ll_shares        = int(0)
        self.ll_width         = int(0)
        self.ll_a_start       = int(0)
        self.ll_a_len         = int(0)    
        self.ll_latency       = int(0)    
        self.ll_r_start       = int(0)
        self.ll_r_len         = int(0)
        self.ll               = self.add_left_leaf()

        self.rl_convert_name  = ""
        self.rl_expand_name   = ""
        self.rl_shares        = int(0)
        self.rl_width         = int(0)
        self.rl_a_start       = int(0)
        self.rl_a_len         = int(0)
        self.rl_latency       = int(0)
        self.rl_r_start       = int(0)
        self.rl_r_len         = int(0)
        self.rl               = self.add_right_leaf()

        self.ll_exist_odvld   = self.exist_ll_odvld()

        if self.shares <= int(1):
            self.ksa_name           = ""
            self.and_name           = ""
            self.ksa_w1l_name       = ""
            self.ksa_latency        = int(0)
            self.ksa_r_start        = int(0)
            self.ksa_r_len          = int(0)
        else:
            self.ksa_name           = "SecKSA_n{}k{}".format(self.shares, self.width)
            self.and_name           = "SecAnd_PINI1_n{}k{}".format(self.shares, self.width)
            self.ksa_w1l_name       = "SecKSA_1l_n{}k{}".format(self.shares, self.width)
            self.ksa_latency        = self.ksa_w*2+4
            self.ksa_r_start        = self.rl_r_start + self.rl_r_len
            self.ksa_r_len          = (2*self.ksa_w+2)*self.n_r        

        self.max_leaf_latency = max(self.ll_latency, self.rl_latency)
        self.latency          = self.max_leaf_latency + self.ksa_latency
        self.r_start          = int(0)
        self.r_len            = self.ksa_r_start + self.ksa_r_len



    def exist_ll_odvld(self):
        if self.rl_latency > self.ll_latency:
            exist = int(1)
        else:
            exist = int(0)
        return exist



    def add_left_leaf(self):
        handler             = int(-1)
        self.ll_shares      = int(self.shares/2)
        self.ll_width       = self.width    
        self.ll_expand_name = "Expand1_n{}o{}k{}".format(self.ll_shares, self.shares, self.ll_width)
        self.ll_a_start     = int(0)
        self.ll_a_len       = self.ll_shares        
        if self.ll_shares > int(1):
            self.ll_convert_name    = "ConvertAB_n{}k{}".format(self.ll_shares, self.ll_width)
            handler                 = ConvertAB_arch(self.ll_shares, self.width, self.id+int(1), int(1))
            self.ll_latency         = handler.latency
            self.ll_r_len           = handler.r_len
        return handler



    def add_right_leaf(self):
        handler             = int(-1)
        self.rl_shares      = int((self.shares+1)/2)
        self.rl_width       = self.width    
        self.rl_expand_name = "Expand2_n{}o{}k{}".format(self.rl_shares, self.shares, self.rl_width)
        self.rl_a_start     = int((self.shares)/2)
        self.rl_a_len       = self.rl_shares  
        self.rl_r_start     = self.ll_r_start + self.ll_r_len      
        if self.rl_shares > int(1):
            self.rl_convert_name    = "ConvertAB_n{}k{}".format(self.rl_shares, self.rl_width)
            handler                 = ConvertAB_arch(self.rl_shares, self.width, self.id+1, int(1))
            self.rl_latency         = handler.latency
            self.rl_r_len           = handler.r_len
        return handler



    def show_left_leaf(self):
        print("="*80,"\n")
        print("|","-"*(self.id+1),">","ll_convert_name  =",self.ll_convert_name,"\n")
        print("|","-"*(self.id+1),">","ll_expand_name   =",self.ll_expand_name,"\n")
        print("|","-"*(self.id+1),">","ll_shares        =",self.ll_shares,"\n")
        print("|","-"*(self.id+1),">","ll_width         =",self.ll_width,"\n")
        print("|","-"*(self.id+1),">","ll_a_start       =",self.ll_a_start,"\n")
        print("|","-"*(self.id+1),">","ll_a_len         =",self.ll_a_len,"\n")            
        print("|","-"*(self.id+1),">","ll_latency       =",self.ll_latency,"\n") 
        print("|","-"*(self.id+1),">","ll_r_start       =",self.ll_r_start,"\n") 
        print("|","-"*(self.id+1),">","ll_r_len         =",self.ll_r_len,"\n") 
        print("|","-"*(self.id+1),">","ll_exist_odvld   =",self.ll_exist_odvld,"\n") 
        print("|","-"*(self.id+1),">","ll               =",self.ll,"\n")    
        if self.ll != int(-1):
            self.ll.showtree()



    def show_right_leaf(self):
        print("="*80,"\n")
        print("|","-"*(self.id+1),">","rl_convert_name  =",self.rl_convert_name,"\n")
        print("|","-"*(self.id+1),">","rl_expand_name   =",self.rl_expand_name,"\n")
        print("|","-"*(self.id+1),">","rl_shares        =",self.rl_shares,"\n")
        print("|","-"*(self.id+1),">","rl_width         =",self.rl_width,"\n")
        print("|","-"*(self.id+1),">","rl_a_start       =",self.rl_a_start,"\n")
        print("|","-"*(self.id+1),">","rl_a_len         =",self.rl_a_len,"\n")            
        print("|","-"*(self.id+1),">","rl_latency       =",self.rl_latency,"\n")  
        print("|","-"*(self.id+1),">","rl_r_start       =",self.rl_r_start,"\n") 
        print("|","-"*(self.id+1),">","rl_r_len         =",self.rl_r_len,"\n") 
        print("|","-"*(self.id+1),">","rl               =",self.rl,"\n")    
        if self.rl != int(-1):
            self.rl.showtree()



    def showtree(self):
        print("="*80,"\n")
        print("|","-"*(self.id+1),">","name             =",self.name,"\n")  
        print("|","-"*(self.id+1),">","shares           =",self.shares,"\n")
        print("|","-"*(self.id+1),">","width            =",self.width,"\n")              
        print("|","-"*(self.id+1),">","iter_depth       =",self.id,"\n")   
        print("|","-"*(self.id+1),">","exist_odvld      =",self.exist_odvld,"\n")   
        print("|","-"*(self.id+1),">","max_leaf_latency =",self.max_leaf_latency,"\n")  
        print("|","-"*(self.id+1),">","latency          =",self.latency,"\n")  
        print("|","-"*(self.id+1),">","ksa_r_start      =",self.ksa_r_start,"\n") 
        print("|","-"*(self.id+1),">","ksa_r_len        =",self.ksa_r_len,"\n") 
        print("|","-"*(self.id+1),">","r_start          =",self.r_start,"\n") 
        print("|","-"*(self.id+1),">","r_len            =",self.r_len,"\n") 
        self.show_left_leaf()
        self.show_right_leaf()



    def write_left_leaf(self, fp_filelist):
        if self.ll != int(-1):
            self.ll.exist_odvld = self.ll_exist_odvld            
            self.ll.write(fp_filelist)



    def write_right_leaf(self, fp_filelist):
        if self.rl != int(-1):
            self.rl.write(fp_filelist)



    def write(self, fp_filelist):
        #################################################################################
        g_inst = ConvertAB(self.name, self.shares, self.width, self)
        g_inst.write()
        print("gen {}".format(g_inst.name))
        print("="*80)
        fp_filelist.add(File(g_inst.name, True)) 
        


        #################################################################################
        g_inst = Expand1(self.ll_expand_name, self.ll_shares, self.shares, self.ll_width)
        g_inst.write()
        print("gen {}".format(g_inst.name))
        print("="*80)
        fp_filelist.add(File(g_inst.name, True)) 



        #################################################################################
        g_inst = Expand2(self.rl_expand_name, self.rl_shares, self.shares, self.rl_width)
        g_inst.write()
        print("gen {}".format(g_inst.name))
        print("="*80)
        fp_filelist.add(File(g_inst.name, True))



        #################################################################################        
        g_inst = SecAnd_PINI1(self.and_name, self.shares, self.width, int(0))
        g_inst.write()
        print("gen {}".format(g_inst.name))
        print("="*80)
        fp_filelist.add(File(g_inst.name, True))



        #################################################################################        
        g_inst = SecAnd_PINI1(self.and_name, self.shares, self.width, int(1))
        g_inst.write()
        print("gen {}".format(g_inst.name))
        print("="*80)
        fp_filelist.add(File(g_inst.name, True))



        #################################################################################        
        g_inst = SecKSA_1l(self.ksa_w1l_name, self.shares, self.width)
        g_inst.write()
        print("gen {}".format(g_inst.name)) 
        print("="*80)
        fp_filelist.add(File(g_inst.name, True))



        #################################################################################        
        g_inst = SecKSA(self.ksa_name, self.shares, self.width, self.exist_odvld)   
        g_inst.write() 
        print("gen {}".format(g_inst.name)) 
        print("="*80)
        fp_filelist.add(File(g_inst.name, True))  



        #################################################################################
        self.write_left_leaf(fp_filelist)
        self.write_right_leaf(fp_filelist)


