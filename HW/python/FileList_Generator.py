import datetime
import os


from InstFun_Container import *



#################################################################################
 # class name       : File
 # description      : file
 #    
 #                
 # input            : @name          : the file name
 # input            : @is_rtl        : is RTL, not test bench
 # input            : @is_def        : is define file
 # input            : @type          : 0: verilog 1: system verilog 2: vhdl
 # returns          : this class
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
class File:
    def __init__(self, name, is_rtl = True, is_def = False, type = int(0)):
        self.name   = name
        self.is_rtl = is_rtl
        self.is_def = is_def
        self.type   = type



#################################################################################
 # class name       : FListGen
 # description      : generate file list file
 #    
 # function         : @get_rtl_list  : get rtl file list
 # function         : @get_sim_list  : get sim file list
 # function         : @get_def_list  : get define file list
 # function         : @add           : add file to file list
 # function         : @write         : write file
 #                
 # input            : @name          : the file list name
 # input            : @proj_path     : the project path
 # returns          : no
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
class FListGen:
    def __init__(self, name, proj_path = "."):
        self.rtl_flist_name = "{}_rtl.flist".format(name)
        self.sim_flist_name = "{}_sim.flist".format(name)
        self.list           = []  
        self.proj_path      = proj_path
        self.add_ComFiles()



    def get_rtl_list(self):
        list = []
        for i in range(0, len(self.list)):
            if self.list[i].is_rtl == int(1):
                list.append(self.list[i])
        return list



    def get_sim_list(self):
        list = []
        for i in range(0, len(self.list)):
            if self.list[i].is_rtl == int(0):
                list.append(list[i])
        return list        



    def get_def_list(self):
        list = []
        for i in range(0, len(self.list)):
            if self.list[i].is_def == int(1):
                list.append(list[i])
        return list



    def add(self, obj):
        if isinstance(obj, File):
            is_exist = 0
            for i in range(0,len(self.list)):
                if self.list[i].name == obj.name:
                    is_exist = 1
                    break
            if is_exist == int(0):
                self.list.append(obj)
        else:
            raise Exception("Invalid type!" + str(obj))



    def add_ComFiles(self):
        for name, is_rtl, is_def, in get_ComFiles():
            self.list.append(File(name, is_rtl, is_def, int(0)))
        self.list.append(File("../syn_lib/NangateOpenCellLibrary", False, False, int(0)))



    def write(self, file=None):
        rtl_s = ""
        tb_s = ""
        folder_name = os.path.basename(os.getcwd())



        #################################################################################        
        L = len(self.list)
        for l in range(0,L):
            if self.list[l].is_rtl:
                if self.list[l].type == int(0):
                    if self.proj_path == ".":
                        rtl_s += "./src/{}.v\n".format(self.list[l].name)
                    else:
                        rtl_s += "${}/{}/src/{}.v\n".format(self.proj_path, folder_name, self.list[l].name)
                elif self.list[l].type == int(1):
                    if self.proj_path == ".":
                        rtl_s += "./src/{}.sv\n".format(self.list[l].name)
                    else:                    
                        rtl_s += "${}/{}/src/{}.sv\n".format(self.proj_path, folder_name, self.list[l].name)
                else:
                    rtl_s += "${}/{}/src/{}.vhd\n".format(self.proj_path, folder_name, self.list[l].name)
            else:
                if self.list[l].type == int(0):
                    if self.proj_path == ".":
                        tb_s += "./tb/{}.v\n".format(self.list[l].name)
                    else:
                        tb_s += "${}/{}/tb/{}.v\n".format(self.proj_path, folder_name, self.list[l].name)
                elif self.list[l].type == int(1): 
                    if self.proj_path == ".":
                        tb_s += "./tb/{}.sv\n".format(self.list[l].name)
                    else:                                   
                        tb_s += "${}/{}/tb/{}.sv\n".format(self.proj_path, folder_name, self.list[l].name)
                else:
                    if self.proj_path == ".":
                        tb_s += "./tb/{}.vhd\n".format(self.list[l].name)
                    else:                    
                        tb_s += "${}/{}/tb/{}.vhd\n".format(self.proj_path, folder_name, self.list[l].name)



        #################################################################################        
        if not os.path.exists('src'):
            os.mkdir('src')
        if not os.path.exists('tb'):
            os.mkdir('tb')



        #################################################################################
        fpath = os.getcwd()
        rtl_name = fpath+ "/src/" + self.rtl_flist_name
        f = open(rtl_name,'w')
        f.write(rtl_s)
        sim_name = fpath+ "/tb/" + self.sim_flist_name
        f = open(sim_name,'w')
        f.write(tb_s)