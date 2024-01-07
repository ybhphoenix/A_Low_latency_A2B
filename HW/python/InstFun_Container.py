#!/usr/bin/env python3
import math
import re


from Verilog_Writer import *




#################################################################################
 # function name    : add_comment
 # description      : add comments for RTL
 # 
 # input            : comment
 # input            : 
 # 
 # returns          : the strings
 # 
 # algorithm        : 
 #                    
 # 
 # 
#################################################################################
def add_comment(comment):
    comments = comment.split('\n')
    raw  = "\n"
    raw += "// ------------------------------------------------------------------------------\n"
    for str in comments:
        raw += "// {}\n".format(str)
    raw += "// ------------------------------------------------------------------------------\n"
    return raw




#################################################################################
 # function name    : get_ComFiles
 # description      : get common library
 # input            : 
 # input            : 
 # 
 # returns          : all common files
 # 
 # algorithm        : 
 #                    
 # 
 # 
#################################################################################
def get_ComFiles():
    Comfiles = [["lib/lix_define", 1, 1], \
                ["lib/lix_and",    1, 0], \
                ["lib/lix_not",    1, 0], \
                ["lib/lix_or",     1, 0], \
                ["lib/lix_reg",    1, 0], \
                ["lib/lix_shr0",   1, 0], \
                ["lib/lix_shr1",   1, 0], \
                ["lib/lix_xor",    1, 0]  ]
    return Comfiles



#################################################################################
 # function name    : find_w
 # description      : find the w for SecKSA
 # input            : @width: SecKSA Data'width
 # input            : 
 # 
 # returns          : w
 # 
 # algorithm        : 
 #                    W = ceil(log(kf) / log(2))-1;
 # 
 # 
#################################################################################
def find_w(width):
    w = int(math.ceil(math.log(width,2)))-1
    return w



#################################################################################
 # function name    : get_num_of_rand
 # description      : get the number of ramdom for SecAnd_PINI1
 # input            : @share: the shares
 # input            : 
 # 
 # returns          : @temp : the number of ramdom
 # 
 # algorithm        : 
 #                    calculate the number of ramdom for r matrix, that is 2-dim 
 #                    matrix
 # 
#################################################################################
def get_num_of_rand(share):
    temp = 0;
    for i in range(1,share):
        temp += i;
    return temp;



#################################################################################
 # class name       : Parameter
 # description      : define a class
 # input            : @name : the name
 # input            : @value: the value
 # 
 # returns          : no returns
 # 
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
class Parameter:
    def __init__(self, name, value):
        self.name  = name
        self.value = value



#################################################################################
 # class name       : inst
 # description      : define a class
 # input            : @name : the name of instance
 # input            : @value: the value of instance
 # 
 # returns          : no returns
 # 
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
class inst:
    def __init__(self, name, value):
        self.name   = name
        self.value  = value



#################################################################################
 # function name    : instance_and
 # description      : do bitwise AND operators by lix_and instances
 #                    z = x & y
 #
 # input            : @x
 # input            : @y
 # output           : @z
 # 
 # parameter        : @width
 # parameter        : @x_start
 # parameter        : @y_start
 # parameter        : @z_start
 # 
 # returns          : ports
 # 
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
def instance_and(x, y, z, width = int(0), x_start = int(0), y_start = int(0), z_start = int(0)):
    ports = []
    if width <= int(0):
        ports.append(Port('i_x'   , '{}'.format(x)))
        ports.append(Port('i_y'   , '{}'.format(y)))
        ports.append(Port('o_z'   , '{}'.format(z)))
    elif width == int(1):
        ports.append(Port('i_x'   , '{}[{}]'.format(x, x_start)))
        ports.append(Port('i_y'   , '{}[{}]'.format(y, y_start)))
        ports.append(Port('o_z'   , '{}[{}]'.format(z, z_start)))
    else:
        ports.append(Port('i_x'   , '{}[{}+:{}]'.format(x, x_start, width)))
        ports.append(Port('i_y'   , '{}[{}+:{}]'.format(y, y_start, width)))
        ports.append(Port('o_z'   , '{}[{}+:{}]'.format(z, z_start, width)))
    return ports



#################################################################################
 # function name    : instance_xor
 # description      : do bitwise XOR operators by lix_xor instances
 #                    z = x ^ y
 #
 # input            : @x
 # input            : @y
 # output           : @z
 #
 # parameter        : @width
 # parameter        : @x_start
 # parameter        : @y_start
 # parameter        : @z_start
 # 
 # returns          : ports
 # 
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################   
def instance_xor(x, y, z, width = int(0), x_start = int(0), y_start = int(0), z_start = int(0)):
    ports = []
    if width <= int(0):
        ports.append(Port('i_x'   , '{}'.format(x)))
        ports.append(Port('i_y'   , '{}'.format(y)))
        ports.append(Port('o_z'   , '{}'.format(z)))
    elif width == int(1):
        ports.append(Port('i_x'   , '{}[{}]'.format(x, x_start)))
        ports.append(Port('i_y'   , '{}[{}]'.format(y, y_start)))
        ports.append(Port('o_z'   , '{}[{}]'.format(z, z_start)))
    else:
        ports.append(Port('i_x'   , '{}[{}+:{}]'.format(x, x_start, width)))
        ports.append(Port('i_y'   , '{}[{}+:{}]'.format(y, y_start, width)))
        ports.append(Port('o_z'   , '{}[{}+:{}]'.format(z, z_start, width)))
    return ports



#################################################################################
 # function name    : instance_not
 # description      : do bitwise NOT operators by lix_not instances
 #                    z = ~ x
 #
 # input            : @x
 # output           : @z
 # 
 # parameter        : @width
 # parameter        : @x_start
 # parameter        : @z_start
 # 
 # returns          : ports
 # 
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################  
def instance_not(x, z, width = int(0), x_start = int(0), z_start = int(0)):
    ports = []
    if width <= int(0):
        ports.append(Port('i_x'   , '{}'.format(x)))
        ports.append(Port('o_z'   , '{}'.format(z)))
    elif width == int(1):
        ports.append(Port('i_x'   , '{}[{}]'.format(x, x_start)))
        ports.append(Port('o_z'   , '{}[{}]'.format(z, z_start)))
    else:
        ports.append(Port('i_x'   , '{}[{}+:{}]'.format(x, x_start, width)))
        ports.append(Port('o_z'   , '{}[{}+:{}]'.format(z, z_start, width)))
    return ports



#################################################################################
 # function name    : instance_reg
 # description      : do register instance with valid and enable
 #                    by lix_reg instances
 #                    z = reg(x)
 #
 # input            : @idvld : valid
 # input            : @irvld : enable
 # input            : @x
 # output           : @z
 # 
 # parameter        : @width
 # parameter        : @x_start
 # parameter        : @z_start
 # 
 # returns          : ports
 # 
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
def instance_reg(idvld, irvld, x, z, width = int(0), x_start = int(0), z_start = int(0)):
    ports = []
    ports.append(Port('clk_i'  , 'clk_i'))
    ports.append(Port('rst_ni' , 'rst_ni'))
    ports.append(Port('i_vld'  , '{}'.format(idvld)))
    ports.append(Port('i_en'   , '{}'.format(irvld)))
    if width <= int(0):
        ports.append(Port('i_x'   , '{}'.format(x)))
        ports.append(Port('o_z'   , '{}'.format(z)))
    elif width == int(1):
        ports.append(Port('i_x'   , '{}[{}]'.format(x, x_start)))
        ports.append(Port('o_z'   , '{}[{}]'.format(z, z_start)))
    else:
        ports.append(Port('i_x'   , '{}[{}+:{}]'.format(x, x_start, width)))
        ports.append(Port('o_z'   , '{}[{}+:{}]'.format(z, z_start, width)))
    return ports



#################################################################################
 # function name    : instance_shr0
 # description      : do pipeline register instance with valid and enable
 #                    by library lix_shr0 instances
 #                    without output valid
 # input            : @idvld : valid
 # input            : @irvld : enable
 # input            : @x
 # output           : @z
 # 
 # parameter        : @x_start
 # parameter        : @x_width
 # 
 # returns          : ports
 # 
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
def instance_shr0(idvld, irvld, x, z, width = int(0), x_start = int(0), z_start = int(0)):
    ports = []
    ports.append(Port('clk_i'  , 'clk_i'))
    ports.append(Port('rst_ni' , 'rst_ni'))
    ports.append(Port('i_vld'  , '{}'.format(idvld)))
    ports.append(Port('i_en'   , '{}'.format(irvld)))
    if width <= int(0):
        ports.append(Port('i_x'   , '{}'.format(x)))
    elif width == int(1):
        ports.append(Port('i_x'   , '{}[{}]'.format(x, x_start)))
    else:
        ports.append(Port('i_x'   , '{}[{}+:{}]'.format(x, x_start, width)))
    if width <= int(0):
        ports.append(Port('o_z'   , '{}'.format(z)))
    elif width == int(1):
        ports.append(Port('o_z'   , '{}[{}]'.format(z, z_start)))
    else:
        ports.append(Port('o_z'   , '{}[{}+:{}]'.format(z, z_start, width)))
    return ports



#################################################################################
 # function name    : instance_shr1
 # description      : do pipeline register instance with valid and enable
 #                    by library lix_shr1 instances
 #
 # input            : @idvld : valid
 # input            : @irvld : enable
 # input            : @x
 # output           : @odvld
 # output           : @z
 # 
 # parameter        : @x_start
 # parameter        : @x_width
 # 
 # returns          : ports
 # 
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
def instance_shr1(idvld, irvld, x, odvld, z, width = int(0), x_start = int(0), z_start = int(0)):
    ports = []
    ports.append(Port('clk_i'  , 'clk_i'))
    ports.append(Port('rst_ni' , 'rst_ni'))
    ports.append(Port('i_vld'  , '{}'.format(idvld)))
    ports.append(Port('i_en'   , '{}'.format(irvld)))
    if width <= int(0):
        ports.append(Port('i_x'   , '{}'.format(x)))
    elif width == int(1):
        ports.append(Port('i_x'   , '{}[{}]'.format(x, x_start)))
    else:
        ports.append(Port('i_x'   , '{}[{}+:{}]'.format(x, x_start, width)))
    ports.append(Port('o_vld'  , '{}'.format(odvld)))
    if width <= int(0):
        ports.append(Port('o_z'   , '{}'.format(z)))
    elif width == int(1):
        ports.append(Port('o_z'   , '{}[{}]'.format(z, z_start)))
    else:
        ports.append(Port('o_z'   , '{}[{}+:{}]'.format(z, z_start, width)))
    return ports



#################################################################################
 # function name    : assigns_3o1
 # description      : do a verilog assign statement, with 3 source
 #                    example: assign dest = src1 ^ src2 ^ src3;
 # 
 # output           : @dest : the assigned signals
 # input            : @src1 : the source 1
 # input            : @optr1: the operator between src1 and src2
 # input            : @src2 : the source 2
 # input            : @optr2: the operator between src2 and src3
 # input            : @src3 : the source 3
 # 
 # parameter        : @start: the start of signal, in units of width
 # parameter        : @end  : the end of signal, in unites of width
 # parameter        : @width: the width
 # 
 # returns          : @raw  : the strings include assign statement
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
def assigns_3o1(dest, src1, optr1, src2, optr2, src3, start, end, width):
    raw = '\n'
    for n in range(start,end):
        raw += "assign {}[{}+:{}] = {}[{}+:{}] {} {}[{}+:{}] {} {}[{}+:{}];\n" \
               .format(dest,n*width,width,src1,n*width,width,optr1,src2,n*width,width,optr2,src3,n*width,width)
    raw += "\n"
    return raw



#################################################################################
 # function name    : assigns_2o1
 # description      : do a verilog assign statement, with 2 source
 #                    example: assign dest = src1 ^ src2;
 # 
 # output           : @dest : the assigned signals
 # input            : @src1 : the source 1
 # input            : @optr : the operator between src1 and src2
 # input            : @src2 : the source 2
 # 
 # parameter        : @start: the start of signal, in units of width
 # parameter        : @end  : the end of signal, in unites of width
 # parameter        : @width: the width
 # 
 # returns          : @raw  : the strings include assign statement
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
def assigns_2o1(dest, src1, optr, src2, start, end, width):
    raw = '\n'
    if width <= int(1):
        max_width_value = end
    else:
        max_width_value = end*width
    max_width = math.ceil(math.log(max_width_value,10))
    list_optr = ["==","<=",">=","<",">","||","&&"]
    for i in range(0,len(list_optr)):
        pos = optr.find(list_optr[i])
        if pos != int(-1):
            break;
    for n in range(start,end):
        if  pos != int(-1):
            raw += "assign {} = ".format(dest)
            l_idx = "{}".format(n*width)
            r_idx = "{}".format(width)
            raw += "{}[{}+:{}] ".format(src1,l_idx.rjust(max_width),r_idx.rjust(max_width))  
            raw += "{} ".format(optr)
            l_idx = "{}".format(n*width)
            r_idx = "{}".format(width)            
            raw += "{}[{}+:{}];\n".format(src2,l_idx.rjust(max_width),r_idx.rjust(max_width))     
        else:
            l_idx = "{}".format(n*width)
            r_idx = "{}".format(width)
            raw += "assign {}[{}+:{}] = ".format(dest,l_idx.rjust(max_width),r_idx.rjust(max_width))
            l_idx = "{}".format(n*width)
            r_idx = "{}".format(width)
            raw += "{}[{}+:{}] ".format(src1,l_idx.rjust(max_width),r_idx.rjust(max_width))
            raw += "{} ".format(optr)
            l_idx = "{}".format(n*width)
            r_idx = "{}".format(width)         
            raw += "{}[{}+:{}];\n".format(src2,l_idx.rjust(max_width),r_idx.rjust(max_width))
    raw += "\n"
    return raw



#################################################################################
 # function name    : assigns_zeros
 # description      : do a verilog assign statement, with zeros
 #                    example: assign dest = 32'd0;
 # 
 # output           : @dest : the assigned signals
 # 
 # parameter        : @start: the start of signal, in units of width
 # parameter        : @end  : the end of signal, in unites of width
 # parameter        : @width: the width
 # 
 # returns          : @raw  : the strings include assign statement
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
def assigns_zeros(dest, start, end, width):
    raw = ''
    if width <= int(1):
        max_width_value = end
    else:
        max_width_value = end*width
    max_width = math.ceil(math.log(max_width_value,10))
    for n in range(start,end):
        if width <= int(1):
            raw += "assign {} = 1'd0;\n".format(dest)
        else:
            l_idx = "{}".format(n*width)
            r_idx = "{}".format(width)
            raw += "assign {}[{}+:{}] = {}'d0;\n".format(dest,l_idx.rjust(max_width),r_idx.rjust(max_width),width)
    #raw += "\n"
    return raw



#################################################################################
 # function name    : assigns_1o1
 # description      : do a verilog assign statement, only 1 source
 #                    with constant operation
 #                    example: assign dest = src1 << 1;
 # 
 # output           : @dest : the assigned signals
 # input            : @src1 : the source 1
 # input            : @optr : the operator, example: <<, >>,
 # input            : @optn : the operate number
 # 
 # parameter        : @start: the start of signal, in units of width
 # parameter        : @end  : the end of signal, in unites of width
 # parameter        : @width: the width
 # parameter        : @src_offset: the source 1 with offset
 # 
 # returns          : @raw  : the strings include assign statement
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
def assigns_1o1(dest, src1, optr, optn, start, end, width , src_offset = 0):
    raw = ''
    if width <= int(1):
        max_width_value = end
    else:
        max_width_value = end*width
    max_width = math.ceil(math.log(max_width_value,10))
    for n in range(start,end):
        if optr == "":
            if width <= int(1):
                raw += "assign {} = {};\n".format(dest,src1)
            else:
                l_idx = "{}".format(n*width)
                r_idx = "{}".format(width)
                raw += "assign {}[{}+:{}] = ".format(dest,l_idx.rjust(max_width),r_idx.rjust(max_width))
                l_idx = "{}".format((n+src_offset)*width)
                r_idx = "{}".format(width)                
                raw += "{}[{}+:{}];\n".format(src1,l_idx.rjust(max_width),r_idx.rjust(max_width))
        else:
            l_idx = "{}".format(n*width)
            r_idx = "{}".format(width)
            raw += "assign {}[{}+:{}] = ".format(dest,l_idx.rjust(max_width),r_idx.rjust(max_width))
            l_idx = "{}".format((n+src_offset)*width)
            r_idx = "{}".format(width) 
            raw += "{}[{}+:{}]".format(src1,l_idx.rjust(max_width),r_idx.rjust(max_width))
            raw += " {} {};\n".format(optr,optn)
    raw += "\n"
    return raw



#################################################################################
 # function name    : assign_1mo1v
 # description      : do a verilog assign statement
 #                    to can get a column vector (dest) from a matrix (src)
 #                    example: 
 #                             to do :
 #                                      assign_1mo1v(dest, src, 0, 3, 32, 3) 
 #                             to get:
 #                                      assign dest[ 0] = src[ 3];
 #                                      assign dest[ 1] = src[35];
 #                                      assign dest[ 2] = src[67];
 # 
 # output           : @dest     : the assigned signals
 # input            : @src      : the source
 # 
 # parameter        : @start    : the start of signal, in units of width
 # parameter        : @end      : the end of signal, in unites of width
 # parameter        : @width    : the width
 # parameter        : @col_idx  : the index of column
 # 
 # returns          : @raw      : the strings include assign statement
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
def assign_1mo1v(dest, src, start, end, width, col_idx):
    raw = ''
    if (width <= int(0)):
        max_width_value = end
    else:
        max_width_value = end*width
    max_width = math.ceil(math.log(max_width_value,10))
    for n in range(start,end):
        if width <= int(0):
            l_idx = "{}".format(n)
            raw += "assign {}[{}] = {};\n".format(dest,l_idx.rjust(max_width),src)
        else:
            l_idx = "{}".format(n)
            r_idx = "{}".format((n*width+col_idx))
            raw += "assign {}[{}] = {}[{}];\n".format(dest,l_idx.rjust(max_width),src,r_idx.rjust(max_width))
    raw += "\n"
    return raw    



#################################################################################
 # function name    : assign_rsh
 # description      : do a verilog assign statement
 #                    to can make a right shift and truncate low bits
 #                    example: 
 #                             to do :
 #                                      assign_rsh(dest, src, 0, 3, 9, 1) 
 #                             to get:
 #                                      assign dest[ 0+: 8] = src[ 1+: 8];
 #                                      assign dest[ 8+: 8] = src[10+: 8];
 #                                      assign dest[16+: 8] = src[19+: 8];
 # 
 # output           : @dest     : the assigned signals
 # input            : @src      : the source
 # 
 # parameter        : @start    : the start of signal, in units of width
 # parameter        : @end      : the end of signal, in unites of width
 # parameter        : @width    : the width
 # parameter        : @shift    : the bit number of right shift
 # 
 # returns          : @raw      : the strings include assign statement
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
def assign_rsh(dest, src, start, end, width, shift):
    src_width = width
    dest_width = width-shift
    max_width_value = src_width*end
    max_width = math.ceil(math.log(max_width_value,10))
    raw = ''
    for n in range(start, end):
        l_idx = "{}".format(n*dest_width)
        r_idx = "{}".format(dest_width)  
        raw += "assign {}[{}+:{}] = ".format(dest,l_idx.rjust(max_width),r_idx.rjust(max_width))   
        l_idx = "{}".format(n*src_width+shift)
        r_idx = "{}".format(dest_width)          
        raw += "{}[{}+:{}];\n".format(src,l_idx.rjust(max_width),r_idx.rjust(max_width))
    raw += "\n"
    return raw      



#################################################################################
 # function name    : assign_lsh
 # description      : do a verilog assign statement
 #                    to can make a left shift and add zeros on the low bits
 #                    example: 
 #                             to do :
 #                                      assign_lsh(dest, src, 0, 3, 9, 1) 
 #                             to get:
 #                                      assign dest[ 0+: 8] = {src[ 0+: 7],1'd0};
 #                                      assign dest[ 9+: 8] = {src[ 9+: 7],1'd0};
 #                                      assign dest[18+: 8] = {src[18+: 7],1'd0};
 # 
 # output           : @dest     : the assigned signals
 # input            : @src      : the source
 # 
 # parameter        : @start    : the start of signal, in units of width
 # parameter        : @end      : the end of signal, in unites of width
 # parameter        : @width    : the width
 # parameter        : @shift    : the bit number of right shift
 # 
 # returns          : @raw      : the strings include assign statement
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
def assign_lsh(dest, src, start, end, width, shift):
    src_width = width
    dest_width = width
    max_width_value = src_width*end
    max_width = math.ceil(math.log(max_width_value,10))
    raw = ''
    for n in range(start, end):
        l_idx = "{}".format(n*dest_width)
        r_idx = "{}".format(dest_width)  
        raw += "assign {}[{}+:{}] = ".format(dest,l_idx.rjust(max_width),r_idx.rjust(max_width))   
        l_idx = "{}".format(n*src_width)
        r_idx = "{}".format(dest_width-shift)   
        raw += """{"""       
        raw += "{}[{}+:{}],".format(src,l_idx.rjust(max_width),r_idx.rjust(max_width))
        raw += "{}'d0".format(shift)
        raw += """};\n"""
    raw += "\n"
    return raw   



#################################################################################
 # function name    : assign_lcat
 # description      : do a verilog assign statement
 #                    to can make a left cascade 
 #                    example: dest = src2 + src1
 #                             to do :
 #                                      assign_lcat(dest, src1, 0, 3, 1, src2, 1) 
 #                             to get:
 #                                      assign dest[0+:2] = {src2[0],src1[0]};
 #                                      assign dest[2+:2] = {src2[1],src1[1]};
 #                                      assign dest[4+:2] = {src2[2],src1[2]};
 # 
 # output           : @dest     : the assigned signals
 # input            : @src1     : the source 1
 # parameter        : @start    : the start of signal, in units of width
 # parameter        : @end      : the end of signal, in unites of width
 # parameter        : @width1   : the width for src1
 # input            : @src2     : the source 2
 # parameter        : @width2   : the width for src2
 # 
 # returns          : @raw      : the strings include assign statement
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
def assign_lcat(dest, src1, start, end, width1, src2, width2):
    dest_width = width1+width2
    raw = ''
    max_width_value = end*dest_width
    max_width = math.ceil(math.log(max_width_value,10))
    for n in range(start, end):
        if dest_width <= int(1):
            raw += "assign {}[{}]".format(dest,n)
        else:
            l_idx = "{}".format(n*dest_width)
            r_idx = "{}".format(dest_width)
            raw += "assign {}[{}+:{}]".format(dest,l_idx.rjust(max_width),r_idx.rjust(max_width))
        raw += " = "
        raw += """{"""
        if width2 <= int(1):
            raw += "{}[{}]".format(src2,n)
        else:
            l_idx = "{}".format(n*width2)
            r_idx = "{}".format(width2)
            raw += "{}[{}+:{}]".format(src2,l_idx.rjust(max_width),r_idx.rjust(max_width))
        if width1 == int(1):
            raw += ",{}[{}]".format(src1,n)
        elif width1 >= int(2):
            l_idx = "{}".format(n*width1)
            r_idx = "{}".format(width1)
            raw += ",{}[{}+:{}]".format(src1,l_idx.rjust(max_width),r_idx.rjust(max_width))
        raw += """};\n"""
    raw += "\n"
    return raw  



#################################################################################
 # function name    : assign_rcat
 # description      : do a verilog assign statement
 #                    to can make a right cascade 
 #                    example: dest = src1 + src2
 #                             to do :
 #                                      assign_lcat(dest, src1, 0, 3, 31, "", 1) 
 #                             to get:
 #                                      assign dest[ 0+:32] = {src1[ 0+:31],1'd0};
 #                                      assign dest[32+:32] = {src1[31+:31],1'd0};
 #                                      assign dest[64+:32] = {src1[62+:31],1'd0};
 # 
 # output           : @dest     : the assigned signals
 # input            : @src1     : the source 1
 # parameter        : @start    : the start of signal, in units of width
 # parameter        : @end      : the end of signal, in unites of width
 # parameter        : @width1   : the width for src1
 # input            : @src2     : the source 2
 # parameter        : @width2   : the width for src2
 # 
 # returns          : @raw      : the strings include assign statement
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
def assign_rcat(dest, src1, start, end, width1, src2, width2):
    dest_width = width1+width2
    raw = ''
    max_width_value = end*dest_width
    max_bit_width = math.ceil(math.log(max_width_value,10))
    for n in range(start, end):
        if dest_width <= int(1):
            raw += "assign {}[{}]".format(dest,n)
        else:
            l_idx = "{}".format(n*dest_width)
            r_idx = "{}".format(dest_width)
            raw += "assign {}[{}+:{}]".format(dest,l_idx.rjust(max_bit_width),r_idx.rjust(max_bit_width))
        raw += " = "
        raw += """{"""
        if width1 == int(1):
            raw += "{}[{}],".format(src1,n)
        elif width1 >= int(2):
            l_idx = "{}".format(n*width1)
            r_idx = "{}".format(width1)
            raw += "{}[{}+:{}],".format(src1,l_idx.rjust(max_bit_width),r_idx.rjust(max_bit_width))        
        if width2 <= int(1):
            if src2 == "":
                raw += "1'd0"
            else:
                raw += "{}".format(src2)
        else:
            if src2 == "":
                raw += "{}d'0".format(width2)
            else:
                l_idx = "{}".format(n*width2)
                r_idx = "{}".format(width2)
                raw += "{}[{}+:{}]".format(src2,l_idx.rjust(max_bit_width),r_idx.rjust(max_bit_width))
        raw += """};\n"""
    raw += "\n"
    return raw  



#################################################################################
 # function name    : assigns_ofs
 # description      : do a verilog assign statement
 #                    to can make a assign with different start 
 #                    example: dest = src
 #                             to do :
 #                                      assigns_ofs(dest, src, 0, 3, 1, 32) 
 #                             to get:
 #                                      assign dest[ 0+:32] = src[32+:32];
 #                                      assign dest[32+:32] = src[64+:32];
 #                                      assign dest[64+:32] = src[96+:32];
 # 
 # output           : @dest         : the assigned signals
 # input            : @src          : the source
 # 
 # parameter        : @dest_start   : the start of dest, in units of width
 # parameter        : @dest_end     : the end of dest, in unites of width
 # parameter        : @src_start    : the start of src, in units of width
 # parameter        : @width2       : the width for src
 # 
 # returns          : @raw          : the strings include assign statement
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
def assigns_ofs(dest, src, dest_start, dest_end, src_start, width):
    raw = ''
    if width <= int(0):
        max_width_value = dest_end
    else:        
        max_width_value = dest_end*width
    max_bit_width = math.ceil(math.log(max_width_value,10))
    if src_start == int(-1):
        src_start = dest_start;
    for n in range(0,dest_end - dest_start):
        if width == int(0):
            raw += "assign {} = {};\n".format(dest,src) 
        else:
            l_idx = "{}".format((n+dest_start)*width)
            r_idx = "{}".format(width)
            raw += "assign {}[{}+:{}] = ".format(dest,l_idx.rjust(max_bit_width),r_idx.rjust(max_bit_width))
            l_idx = "{}".format((n+src_start)*width)
            r_idx = "{}".format(width)
            raw += "{}[{}+:{}];\n".format(src,l_idx.rjust(max_bit_width),r_idx.rjust(max_bit_width))            
    raw += "\n"
    return raw



#################################################################################
 # function name    : inst_ff
 # description      : do a flip-flop instance by RTL level
 #                    to can get registers
 #                    example: 
 #                             to do :
 #                                      inst_ff(dest, src1, "", 1, 32, """) 
 #                             to get:
 #                                      reg [31:0] _ff_$dest;
 #                                      always@(negedge rst_ni or posedge clk_i) begin
 #                                        if (~rst_ni)begin
 #                                            _ff_$dest <= 32'd0;
 #                                        end else begin
 #                                            _ff_$dest <= $src1;
 #                                        end
 #                                      end
 #                                      assign $dest = _ff_$dest;
 # 
 # output           : @dest         : the assigned signals
 # input            : @src1         : the source 1
 # input            : @vld          : the valid of register
 # parameter        : @num          : the number of register, in unites of width
 # parameter        : @width        : the width of register
 # input            : @en           : the enable of register
 # 
 # returns          : @raw          : the strings include instance statement
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
def inst_ff(dest, src1, vld, num, width, en = ""):
    raw = ""
    reg_name = "ff_{}".format(dest)
    raw += "reg [{}:0] {};\n".format(width*num-1, reg_name)
    raw += "always@(negedge rst_ni or posedge clk_i) begin\n"
    raw += "  if (~rst_ni)begin\n"
    for n in range(0,num):
        raw += "    {}[{}+:{}] <= {}'d0;\n".format(reg_name,n*width,width,width)
    if vld == "":
        if en == "":
            raw += "  end else begin\n"
        else:
            raw += "  end else if {} begin\n".format(en)
    else:
        if en == "":
            raw += "  end else if {} begin\n".format(vld)
        else:
            raw += "  end else if {} && {} begin\n".format(vld, en)
    for n in range(0,num):
        raw += "    {}[{}+:{}] <= {}[{}+:{}];\n".format(reg_name,n*width,width,src1,n*width,width)
    raw += "  end\n"
    raw += "end\n"
    raw += "assign {} = {};\n".format(dest, reg_name)
    raw += "\n"
    return raw



#################################################################################
 # function name    : inst_sh
 # description      : do a pipeline register instance  by RTL level
 #                    to can get pipeline register
 #                    example: 
 #                             to do :
 #                                      inst_sh(dest, src, "", 1, 32) 
 #                             to get:
 #                                      
 # output           : @dest         : the assigned signals
 # input            : @src          : the source
 # input            : @i_vld        : the valid of register
 # parameter        : @shift        : the shift number of register, in unites of width
 # parameter        : @width        : the width of register
 # parameter        : @src_offset   : the start of src, in unites of 1 bit
 # input            : @en           : the enable of register
 # output           : @o_vld        : the output valid 
 # 
 # returns          : @raw          : the strings include instance statement
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
def inst_sh(dest, src, i_vld, shift, width, src_offset = 0, en = "", o_vld = ""):
    raw = ""
    vld_name = "shv_{}".format(dest)
    if i_vld != "":
        if shift == int(2):
            raw += "reg  {};\n".format(vld_name)
        else:
            raw += "reg  [{}:0] {};\n".format(shift-1,vld_name)
        raw += "always@(negedge rst_ni or posedge clk_i) begin\n"
        raw += "  if (~rst_ni)begin\n"
        if shift == int(2):
            raw += "    {} <= {}'d0;\n".format(vld_name,shift-1)
        else:
            raw += "    {} <= {}'d0;\n".format(vld_name,shift)
        if en == "":
            raw += "  end else begin\n"
        else:
            raw += "  end else if ({}) begin\n".format(en)
        raw += "    {} <= ".format(vld_name) + '{'
        if shift == int(2):
            raw += "{}".format(i_vld) + '};\n'
        else:
            raw += "{}[{}:0],{}".format(vld_name,shift-2,i_vld) + '};\n'
        raw += "  end\n"
        raw += "end\n"
    if o_vld != "":
        if shift == int(2):
            raw += "assign {} = {};\n".format(o_vld, vld_name)
        else:
            raw += "assign {} = {}[{}];\n".format(o_vld, vld_name, shift-1)
    raw += "\n"
    reg_name = "shd_{}".format(dest)
    if width <= int(0):
        raw += "reg  {} [{}:0];\n".format(reg_name,shift-1)    
    else:
        raw += "reg  [{}:0] {} [{}:0];\n".format(width-1,reg_name,shift-1)
    raw += "always@(negedge rst_ni or posedge clk_i) begin\n"
    raw += "  if (~rst_ni)begin\n"
    for n in range(0,shift):
        if width <= int(0):
            raw += "    {}[{}] <= 1'd0;\n".format(reg_name,n)
        else:
            raw += "    {}[{}] <= {}'d0;\n".format(reg_name,n,width)
    raw += "  end else begin\n"
    for n in range(0,shift):
        if i_vld != "":
            if n == int(0):
                if en == "":
                    raw += "    if ({}) begin\n".format(i_vld)
                else:
                    raw += "    if ({} && {}) begin\n".format(i_vld,en)
                if width <= int(0):
                    raw += "      {}[{}] <= {};\n".format(reg_name,n,src)
                else:
                    raw += "      {}[{}] <= {}[{}+:{}];\n".format(reg_name,n,src,src_offset,width)
            else:
                if shift == int(2):
                    if en == "":
                        raw += "    if ({}) begin\n".format(vld_name)
                    else:
                        raw += "    if ({} && {}) begin\n".format(vld_name, en)
                else:
                    if en == "":
                        raw += "    if ({}[{}]) begin\n".format(vld_name,n-1)
                    else:
                        raw += "    if ({}[{}] && {}) begin\n".format(vld_name,n-1,en)
                raw += "      {}[{}] <= {}[{}];\n".format(reg_name,(n),reg_name,(n-1))
            raw += "    end\n"
        else:
            if n == int(0):
                if en == "":
                    if width <= int(0):
                        raw += "    {}[{}] <= {};\n".format(reg_name,n,src)
                    else:
                        raw += "    {}[{}] <= {}[{}+:{}];\n".format(reg_name,n,src,src_offset,width)
                else:
                    raw += "    if ({}) begin\n".format(en)
                    if width <= int(0):
                        raw += "      {}[{}] <= {};\n".format(reg_name,n,src) 
                    else:
                        raw += "      {}[{}] <= {}[{}+:{}];\n".format(reg_name,n,src,src_offset,width)  
                    raw += "    end\n"                  
            else:
                if en == "":
                    raw += "    {}[{}] <= {}[{}];\n".format(reg_name,(n),reg_name,(n-1))
                else:
                    raw += "    if ({}) begin\n".format(en)
                    raw += "      {}[{}] <= {}[{}];\n".format(reg_name,(n),reg_name,(n-1))
                    raw += "    end\n"                                                            
    raw += "  end\n"
    raw += "end\n"
    if width <= int(0):
        raw += "assign {} = {}[{}];\n".format(dest,reg_name,(shift-1))
    else:
        raw += "assign {}[{}:0] = {}[{}];\n".format(dest,width-1,reg_name,(shift-1))
    raw += "\n"
    return raw



#################################################################################
 # function name    : gen_clock
 # description      : generate clock for test bench
 #                                      
 #                                      
 #                                      
 # output           : @name         : the clock name
 # 
 # parameter        : @period       : the clock period
 # 
 # returns          : @raw          : the strings include clock
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
def gen_clock(name, period):
    raw = "\n"
    raw += "initial\n"
    raw += "begin\n"
    raw += "  {} = 1'd0;\n".format(name)
    raw += "  forever #({}/2) {} = ~{};\n".format(period, name, name)
    raw += "end\n\n"
    return raw



#################################################################################
 # function name    : gen_reset
 # description      : generate reset for test bench
 #                                      
 #                                      
 #                                      
 # output           : @name         : the reset name
 # 
 # parameter        : @init_time    : the the reset span time in initial
 # parameter        : @active_level : the reset active level
 # 
 # returns          : @raw          : the strings include reset
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
def gen_reset(name, init_time, active_level = 0):
    if active_level == int(0):
        reset_state = int(0)
        release_state = int(1)
    else:
        reset_state = int(1)
        release_state = int(0)
    raw = "\n"
    raw += "initial\n"
    raw += "begin\n"
    raw += " {} = 1'd{};\n".format(name, reset_state)
    raw += " #{};\n".format(init_time)
    raw += " {} = 1'd{};\n".format(name, release_state)
    raw += "end\n\n"
    return raw



#################################################################################
 # function name    : init_signal
 # description      : initial signals for test bench
 #                                      
 #                                      
 #                                      
 # output           : @list         : the signal list
 # 
 # returns          : @raw          : the strings include initial statement
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
def init_signal(list):
    raw = "\n"
    raw += "initial\n"
    raw += "begin\n"
    for (n, w) in list:
        if w == int(0):
            raw +="  {} = {}'d0;\n".format(n, 1)
        else:
            raw +="  {} = {}'d0;\n".format(n, w)
    raw += "end\n\n"
    return raw



#################################################################################
 # function name    : gen_rand
 # description      : generate random value for sig for test bench
 #                                      
 #                                      
 #                                      
 # input            : @clock        : the clock
 # parameter        : @init_wait    : wait time in initial
 # output           : @sig          : the signals to which assign random value
 # parameter        : @shares       : the shares
 # parameter        : @width        : the width
 # parameter        : @is_rand      : if True, ramdom, else, zeros
 # 
 # returns          : @raw          : the strings include initial statement
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
def gen_rand(clock, init_wait, sig, shares, width, is_rand = True):
    raw = "\n"
    raw += "initial\n"
    raw += "begin\n"
    raw += "  {} = {}'d0;\n".format(sig, width*shares)
    raw += "  repeat ({}) @(posedge {});\n".format(init_wait, clock)
    raw += "  forever begin\n"
    raw += "    @(posedge {});\n".format(clock)
    raw += "    for(int i = 0 ; i < {} ; i++)begin\n".format(shares)
    if is_rand:
        if width < 33:
            if width <= int(1):
                raw += "      {}[i] = $random;\n".format(sig)
            else:
                raw += "      {}[i*{}+:{}] = $random;\n".format(sig, width, width)
        else:
            raw += "      {}[i*{}+:{}] = ".format(sig, width, width) 
            raw += """{$random,$random};\n"""            
    else:
        raw += "      {}[i*{}+:{}] = {}'d0;\n".format(sig, width, width, width)
    raw += "    end\n"
    raw += "  end\n"
    raw += "end\n\n"
    return raw



#################################################################################
 # function name    : gen_vld
 # description      : generate valid for sig for test bench
 #                                      
 #                                      
 #                                      
 # input            : @clock        : the clock
 # parameter        : @init_wait    : wait time in initial
 # output           : @sig          : the signals to which assign random value
 # parameter        : @vld_cnt      : the valid span
 # 
 # returns          : @raw          : the strings include initial statement
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
def gen_vld(clock, init_wait, sig, vld_cnt):
    raw = "\n"
    raw += "initial\n"
    raw += "begin\n"
    raw += "  {} = 1'd0;\n".format(sig)
    raw += "  repeat ({}) @(posedge {});\n".format(init_wait, clock)
    raw += "    {} = 1'd1;\n".format(sig)
    raw += "  repeat ({}) @(posedge {});\n".format(vld_cnt, clock)
    raw += "    {} = 1'd0;\n".format(sig)
    raw += "end\n\n"
    return raw   



#################################################################################
 # function name    : gen_fsdb
 # description      : generate dump fsdb code for test bench
 #                                      
 #                                      
 #                                      
 # input            : @name         : 
 # returns          : @raw          : the strings include dump fsdb code
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
def gen_fsdb(name):
    raw = "\n"
    raw += "initial\n"
    raw += "begin\n"
    raw += """  $fsdbDumpfile("wave.fsdb");\n"""
    raw += """  $fsdbDumpvars("+all");\n"""
    raw += "end\n\n"
    return raw



#################################################################################
 # function name    : gen_finish
 # description      : finish simulation for test bench
 #                                      
 #                                      
 #                                      
 # input            : @t            : the simulation time
 # returns          : @raw          : the strings finish simulation
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
def gen_finish(t):
    raw = "\n"
    raw += "initial\n"
    raw += "begin\n"
    raw += "  #{};\n".format(t)
    raw += "  $finish;\n"
    raw += "end\n\n"
    return raw   



#################################################################################
 # function name    : disp_result
 # description      : display simulation results
 #                                      
 #                                      
 #                                      
 # input            : @clock        : the clock
 # input            : @result       : the signal 
 #                                    which indicate the test is passed or failed
 # input            : @vld          : the valid of result
 # input            : @time         : the time to wait for result
 # returns          : @raw          : the strings display simulation results
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
def disp_result(clock, result, vld, time):
    raw = "\n"
    raw += "logic fail;\n"
    raw += "initial\n"
    raw += "begin\n"
    raw += "  fail = 1'd0;\n"
    raw += "  forever begin\n"
    raw += "    @(posedge {});\n".format(clock)
    raw += "    if ({} != 1'd1 && {} == 1'd1)begin\n".format(result, vld)
    raw += """       $display("Test_Failed");\n"""
    raw += "       fail = 1'd1;\n"
    raw += "    end\n"
    raw += "  end\n"
    raw += "end\n\n" 
    raw += "initial\n"
    raw += "begin\n"
    raw += "  #{};\n".format(time)
    raw += "  @(posedge {});\n".format(clock)
    raw += "  if (fail == 1'b0)begin\n"
    raw += """    $display("Test_Passed");\n"""
    raw += "  end\n"
    raw += "end\n\n"    

    return raw




