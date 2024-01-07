#!/usr/bin/env python3
import math
import sys

from InstFun_Container import *
from FileList_Generator import *
from SecCSA_Generator import SecCSA
from SecAnd_PINI1_Generator import SecAnd_PINI1
from SecCSATree_Generator import SecCSATree




#################################################################################
 # class name       : SecCSATree_arch
 # description      : Initialize the parameters of SecCSATree architecutre
 #                    write files
 #
 # function         : @add_leaf             : add leaf to this tree
 # function         : @show_leaf            : print leaf to console
 # function         : @showtree             : print self to concole
 # function         : @write_leaf           : write leaf to file
 # function         : @write                : write this to file
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
class SecCSATree_arch:
    def __init__(self, shares, width, iter_depth):
        self.shares           = shares
        self.width            = width
        self.id               = iter_depth   
        self.name             = "SecCSATree_n{}k{}".format(self.shares, self.width)

        self.tree_name        = ""
        self.tree_r_start     = int(0)
        self.tree_r_len       = int(0)
        self.tree_latency     = int(0)

        self.csa_name         = ""
        self.and_name         = ""
        self.csa_r_start      = int(0)
        self.csa_r_len        = int(0)
        self.csa_latency      = int(0)
        self.csa_shares       = int(0)
        self.csa_width        = int(0)
        self.leaf_pointer     = self.add_leaf()

        self.latency          = self.tree_latency + self.csa_latency
        self.r_start          = int(0)
        self.r_len            = self.csa_r_start + self.csa_r_len



    def add_leaf(self):
        handler             = int(-1)
        if self.shares <= int(3):
            self.csa_name       = "SecCSA_n{}k{}".format(self.shares, self.width)
            self.and_name       = "SecAnd_PINI1_n{}k{}".format(self.shares, self.width)
            self.csa_r_start    = int(0)
            self.csa_r_len      = get_num_of_rand(self.shares)
            self.csa_latency    = int(2)
            self.csa_shares     = int(3)
            self.csa_width      = self.width
        else:
            handler             = SecCSATree_arch(self.shares-1, self.width, self.id+int(1))
            self.tree_name      = "SecCSATree_n{}k{}".format(self.shares-1, self.width)
            self.tree_r_start   = int(0)
            self.tree_r_len     = handler.r_len
            self.tree_latency   = handler.latency
            self.csa_name       = "SecCSA_n{}k{}".format(self.shares, self.width)
            self.and_name       = "SecAnd_PINI1_n{}k{}".format(self.shares, self.width)
            self.csa_r_start    = self.tree_r_start + self.tree_r_len
            self.csa_r_len      = get_num_of_rand(self.shares)
            self.csa_latency    = int(2) 
            self.csa_shares     = self.shares-int(1)
            self.csa_width      = self.width           

        return handler



    def show_leaf(self):
        if self.leaf_pointer != int(-1):
            self.leaf_pointer.showtree()



    def showtree(self):
        print("="*80,"\n")
        print("|","-"*(self.id+1),">","name             =",self.name,"\n")  
        print("|","-"*(self.id+1),">","shares           =",self.shares,"\n")
        print("|","-"*(self.id+1),">","width            =",self.width,"\n")              
        print("|","-"*(self.id+1),">","iter_depth       =",self.id,"\n")   
        print("|","-"*(self.id+1),">","tree_name        =",self.tree_name,"\n")   
        print("|","-"*(self.id+1),">","tree_r_start     =",self.tree_r_start,"\n")
        print("|","-"*(self.id+1),">","tree_r_len       =",self.tree_r_len,"\n")
        print("|","-"*(self.id+1),">","tree_latency     =",self.tree_latency,"\n")
        print("|","-"*(self.id+1),">","csa_name         =",self.csa_name,"\n")   
        print("|","-"*(self.id+1),">","and_name         =",self.and_name,"\n")
        print("|","-"*(self.id+1),">","csa_r_start      =",self.csa_r_start,"\n")
        print("|","-"*(self.id+1),">","csa_r_len        =",self.csa_r_len,"\n")
        print("|","-"*(self.id+1),">","csa_latency      =",self.csa_latency,"\n")
        print("|","-"*(self.id+1),">","latency          =",self.latency,"\n")  
        print("|","-"*(self.id+1),">","r_start          =",self.r_start,"\n") 
        print("|","-"*(self.id+1),">","r_len            =",self.r_len,"\n") 
        self.show_leaf()




    def write_leaf(self, fp_filelist):
        if self.leaf_pointer != int(-1):
            self.leaf_pointer.write(fp_filelist)



    def write(self, fp_filelist):
        #################################################################################
        g_inst = SecCSATree(self.name, self.shares, self.width, self)
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
        g_inst = SecCSA(self.csa_name, self.shares, self.width)
        g_inst.write()            
        print("gen {}".format(g_inst.name))
        print("="*80)
        fp_filelist.add(File(g_inst.name, True))



        #################################################################################
        self.write_leaf(fp_filelist)



