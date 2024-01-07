#!/usr/bin/env python3

import sys

from InstFun_Container import *
from FileList_Generator import *
from DcTcl_Writer import DcTclWriter

from SecA2B_Arch_Generator import *
from SecA2B_TB_Generator import *

from ConvertAB_Arch_Generator import *
from ConvertAB_TB_Generator import *

from ConvertAB_RCA_Arch_Generator import *
from ConvertAB_RCA_TB_Generator import *


#################################################################################
 #  This is the main proc                                 
################################################################################# 
if __name__ == "__main__":


    if len(sys.argv) < 6:
        raise Exception("Invalid parameters!\n example: python Main_Generator.py type shares width dump print_debug")

    type = sys.argv[1]
    if type != "SecA2B" and type != "ConvertAB" and type != "ConvertAB_RCA":
        raise Exception("Invalid type!\n The type should be SecA2B or ConvertAB or ConvertAB_RCA")        

    if int(sys.argv[2]) < 11 and int(sys.argv[2]) > 1:
        shares = int(sys.argv[2])
    else:
        raise Exception("Invalid shares!\n The shares should be from 2 to 10")

    if int(sys.argv[3]) < 65 and int(sys.argv[3]) > 7:
        width  = int(sys.argv[3])
    else:
        raise Exception("Invalid width!\n The width shoud be from 8 to 64")

    if int(sys.argv[4]) != int(0):
        dumpon = 1
    else:
        dumpon = 0

    if int(sys.argv[5]) != int(0):
        print_debug = True
    else:
        print_debug = False

    print("argv[0]=",sys.argv[0],"argv[1]=",sys.argv[1],"argv[2]=",sys.argv[2],"argv[3]=",sys.argv[3],"argv[4]=",sys.argv[4],"dumpon=",dumpon, "print_debug=",print_debug,"\n")



    #################################################################################
     #  Generate SecA2B                                 
    #################################################################################    
    if type == "SecA2B":
        g_A2B_flist = FListGen("SecA2B")

        # generate rtl
        g_A2B = SecA2B_arch(shares,width)
        print("="*33,"SecA2B arch ","="*33)
        g_A2B.write(g_A2B_flist, print_debug)

        # generate tcl file for design compiler 
        top_name = "{}_{}".format(g_A2B.name, g_A2B.exist_odvld)
        g_dctcl = DcTclWriter(top_name)
        g_dctcl.set_list(g_A2B_flist.get_rtl_list())
        g_dctcl.add_tcl("library_setup_dc.tcl")
        g_dctcl.add_tcl("dont_use.tcl")
        g_dctcl.add_sdc("{}.sdc".format(top_name)) 
        g_dctcl.write()       

        # generate test bench 
        tb_class_SecA2B_name = "SecA2B_tb"
        tb_inst_SecA2B_name = "{}_n{}k{}".format(tb_class_SecA2B_name, shares, width)
        g_tb = SecA2B_tb(tb_inst_SecA2B_name, shares, width, g_A2B, dumpon)
        g_tb.write()
        g_A2B_flist.add(File(tb_inst_SecA2B_name, False, False, int(1))) 

        # generate file list 
        g_A2B_flist.write()


    #################################################################################
     #  Generate ConvertAB
    #################################################################################
    if type == "ConvertAB":
        g_AB_flist = FListGen("ConvertAB")

        # generate rtl
        g_convertAB = ConvertAB_arch(shares, width , int(0))
        print("="*32,"ConvertAB arch","="*32)
        if print_debug == True:            
            g_convertAB.showtree()
        g_convertAB.write(g_AB_flist)

        # generate tcl file for design compiler 
        top_name = "{}_{}".format(g_convertAB.name, g_convertAB.exist_odvld)
        g_dctcl = DcTclWriter(top_name)
        g_dctcl.set_list(g_AB_flist.get_rtl_list())
        g_dctcl.add_tcl("library_setup_dc.tcl")
        g_dctcl.add_tcl("dont_use.tcl")
        g_dctcl.add_sdc("{}.sdc".format(top_name)) 
        g_dctcl.write()       

        # generate test bench 
        tb_class_convertAB_name = "ConvertAB_tb"
        tb_inst_convertAB_name = "{}_n{}k{}".format(tb_class_convertAB_name, shares, width)
        g_tb = ConvertAB_tb(tb_inst_convertAB_name, shares, width, g_convertAB, dumpon)
        g_tb.write()
        g_AB_flist.add(File(tb_inst_convertAB_name, False, False, int(1))) 

        # generate file list    
        g_AB_flist.write()



    #################################################################################
     #  Generate ConvertAB_RCA
    #################################################################################
    if type == "ConvertAB_RCA":
        g_AB_RCA_flist = FListGen("ConvertAB_RCA")

        # generate rtl
        g_convertAB_RCA = ConvertAB_RCA_arch(shares, width , int(0))
        print("="*30,"ConvertAB_RCA arch","="*30)
        if print_debug == True:            
            g_convertAB_RCA.showtree()
        g_convertAB_RCA.write(g_AB_RCA_flist)
        
        # generate tcl file for design compiler 
        top_name = "{}_{}".format(g_convertAB_RCA.name, g_convertAB_RCA.exist_odvld)
        g_dctcl = DcTclWriter(top_name)
        g_dctcl.set_list(g_AB_RCA_flist.get_rtl_list())
        g_dctcl.add_tcl("library_setup_dc.tcl")
        g_dctcl.add_tcl("dont_use.tcl")
        g_dctcl.add_sdc("{}.sdc".format(top_name)) 
        g_dctcl.write()     

        # generate test bench 
        tb_class_convertAB_name = "ConvertAB_RCA_tb"
        tb_inst_convertAB_name = "{}_n{}k{}".format(tb_class_convertAB_name, shares, width)
        g_tb = ConvertAB_RCA_tb(tb_inst_convertAB_name, shares, width, g_convertAB_RCA, dumpon)
        g_tb.write()
        g_AB_RCA_flist.add(File(tb_inst_convertAB_name, False, False, int(1))) 

        # generate file list    
        g_AB_RCA_flist.write()  