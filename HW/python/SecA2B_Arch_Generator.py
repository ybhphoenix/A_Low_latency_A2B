#!/usr/bin/env python3
import math
import sys

from InstFun_Container import *
from FileList_Generator import *
from SecAnd_PINI1_Generator import SecAnd_PINI1
from SecCSATree_Arch_Generator import SecCSATree_arch
from SecKSA_1l_Generator import SecKSA_1l
from SecKSA_Generator import SecKSA
from SecA2B_Generator import SecA2B



#################################################################################
 # class name       : SecA2B_arch
 # description      : Initialize the parameters of SecA2B architecture
 #                    
 # function         : @get_SecCSATree_arch : get SecCSATree parameters
 # function         : @get_SecAnd_PINI1_0  : get SecAnd_PINI1 parameters
 # function         : @get_SecAnd_PINI1_1  : get SecAnd_PINI1 parameters
 # function         : @get_SecKSA_1l       : get SecKSA_1l parameters
 # function         : @get_SecKSA          : get SecKSA parameters
 # function         : @get_SecA2B          : get SecA2B parameters
 # function         : @write               : write file
 #                    
 # input            : @shares    : the shares
 # input            : @width     : the width
 # returns          : no
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
class SecA2B_arch:
    def __init__(self, shares, width, exist_odvld=int(1)):
        self.shares       = shares
        self.width        = width
        self.name         = "SecA2B_n{}k{}".format(self.shares, self.width)
        self.exist_odvld  = exist_odvld
        self.csatree_list = self.get_SecCSATree_arch()
        self.and0_list    = self.get_SecAnd_PINI1_0()
        self.and1_list    = self.get_SecAnd_PINI1_1()
        self.ksa_w1l_list = self.get_SecKSA_1l()
        self.ksa_list     = self.get_SecKSA()
        self.a2b_list     = self.get_SecA2B()
        if shares < 3:
            self.latency      = self.ksa_list.latency
            self.tree_r_start = int(0)
            self.tree_r_len   = int(0)
        else:
            self.latency      = self.csatree_list.latency + self.ksa_list.latency
            self.tree_r_start = self.csatree_list.r_start
            self.tree_r_len   = self.csatree_list.r_len
        self.ksa_r_start  = self.tree_r_start  + self.tree_r_len   
        self.ksa_r_len    = self.ksa_list.r_len
        self.r_start      = int(0)
        self.r_len        = self.ksa_r_start + self.ksa_r_len



    def get_SecCSATree_arch(self):
        if self.shares > 2:
            g_inst        = SecCSATree_arch(self.shares, self.width, int(0))
        else:
            g_inst        = int(-1)
        return g_inst  



    def get_SecAnd_PINI1_0(self):
        name              = "{}_n{}k{}".format("SecAnd_PINI1", self.shares, self.width)        
        g_inst            = SecAnd_PINI1(name, self.shares, self.width, int(0))
        return g_inst          



    def get_SecAnd_PINI1_1(self):
        name              = "{}_n{}k{}".format("SecAnd_PINI1", self.shares, self.width)        
        g_inst            = SecAnd_PINI1(name, self.shares, self.width, int(1))
        return g_inst  



    def get_SecKSA_1l(self):
        name              = "{}_n{}k{}".format("SecKSA_1l", self.shares, self.width)
        g_inst            = SecKSA_1l(name, self.shares, self.width)
        return g_inst         



    def get_SecKSA(self):
        name              = "{}_n{}k{}".format("SecKSA", self.shares, self.width)
        g_inst            = SecKSA(name, self.shares, self.width)
        return g_inst 



    def get_SecA2B(self):
        name              = "{}_n{}k{}".format("SecA2B", self.shares, self.width)
        g_inst            = SecA2B(name, self.shares, self.width, self)
        return g_inst 

        

    def write(self, fp_filelist, print_debug = False):
        #################################################################################
        g_inst = self.csatree_list
        if g_inst != int(-1):
            print("gen {}".format(g_inst.name))
            print("="*80)
            if print_debug == True:
                g_inst.showtree()
            g_inst.write(fp_filelist)



        #################################################################################
        g_inst = self.and0_list
        print("gen {}".format(g_inst.name))
        print("="*80)
        g_inst.write()
        fp_filelist.add(File(g_inst.name, True))



        #################################################################################
        g_inst = self.and1_list
        print("gen {}".format(g_inst.name))
        print("="*80)
        g_inst.write()
        fp_filelist.add(File(g_inst.name, True))



        #################################################################################
        g_inst = self.ksa_w1l_list
        print("gen {}".format(g_inst.name))
        print("="*80)
        g_inst.write()
        fp_filelist.add(File(g_inst.name, True))



        #################################################################################
        g_inst = self.ksa_list
        print("gen {}".format(g_inst.name))
        print("="*80)
        g_inst.write()
        fp_filelist.add(File(g_inst.name, True))



        ################################################################################# 
        g_inst = self.a2b_list
        print("gen {}".format(g_inst.name))
        print("="*80)
        g_inst.write() 
        fp_filelist.add(File(g_inst.name, True))
