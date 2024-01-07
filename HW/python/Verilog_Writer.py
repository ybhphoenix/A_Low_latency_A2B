import datetime
import os



#################################################################################
 # class name       : Signal
 # description      : 
 #                    
 # returns          : this class
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
class Signal(object):
    def __init__(self, name, width=0, low=0, asc=False, vec=0):
        self.name = name
        self.width=width
        self.low = low
        self.asc = asc
    def get_name(self,index = -1):
        if index < int(0):
            return self.name
        else:
            return "{}[{}]".format(self.name,index)
    def range(self):
        if self.width > 0:
            l = self.width+self.low-1
            r = self.low
            if self.asc:
                return '['+str(r)+':'+str(l)+']'
            else:
                return '['+str(l)+':'+str(r)+']'
        return ''



#################################################################################
 # class name       : Wire
 # description      : 
 #                    
 # returns          : this class
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
class Wire(Signal):
    def write(self, width):
        return 'wire  {range} {name};\n'.format(range=self.range().rjust(width), name=self.name)



#################################################################################
 # class name       : Logic
 # description      : 
 #                    
 # returns          : this class
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
class Logic(Signal):
    def write(self, width):
        return 'logic {range} {name};\n'.format(range=self.range().rjust(width), name=self.name)



#################################################################################
 # class name       : Port
 # description      : 
 #                    
 # returns          : this class
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
class Port:
    def __init__(self, name, value):
        self.name = name
        self.value = value



#################################################################################
 # class name       : ModulePort
 # description      : 
 #                    
 # returns          : this class
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
class ModulePort(Signal):
    def __init__(self, name, dir, width=0, low=0, asc=False):
        super(ModulePort, self).__init__(name, width, low, asc)
        self.dir = dir

    def write(self, range_width=0):
        return '{dir} wire {range} {name}'.format(dir=self.dir.ljust(6), range=self.range().rjust(range_width), name=self.name)



#################################################################################
 # class name       : Parameter
 # description      : 
 #                    
 # returns          : this class
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
class Parameter:
    def __init__(self, name, value):
        self.name = name
        self.value = value



#################################################################################
 # class name       : ModuleParameter
 # description      : 
 #                    
 # returns          : this class
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
class ModuleParameter(Signal):
    def __init__(self, name, value, width=0, low=0, asc=False):
        super(ModuleParameter, self).__init__(name, width, low, asc)
        self.value = value

    def write(self, range_width=0):
        return 'parameter {range} {name} = {value}'.format(range=self.range().rjust(range_width), name=self.name,value=self.value)



#################################################################################
 # class name       : Raw
 # description      : 
 #                    
 # returns          : this class
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
class Raw:
    def __init__(self, raw):
        self.raw = raw

    def write(self):
        return '{}'.format(self.raw)




#################################################################################
 # class name       : Instance
 # description      : 
 #                    
 # returns          : this class
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
class Instance:
    def __init__(self, module, name, parameters, ports, front_raw = "", post_raw = ""):
        self.module = module
        self.name = name
        self.parameters = parameters
        self.ports = ports
        self.fraw = front_raw
        self.praw = post_raw
    


    def add_front_raw(self, raw):
        self.fraw = raw



    def add_post_raw(self, raw):
        self.praw = raw



    def write(self):
        s = self.fraw
        #s += "\n"
        s += self.module
        if self.parameters:
            max_len = max([len(p.name) for p in self.parameters])
            s += '\n  #('
            s += ',\n    '.join(['.' + p.name.ljust(max_len) +' (' + str(p.value) + ')' for p in self.parameters])
            s += ')'
        s += '\n  ' + self.name
        
        if self.ports:
            s += '\n   ('
            max_len = max([len(p.name) for p in self.ports])
            s += ',\n    '.join(['.' + p.name.ljust(max_len) +' (' + str(p.value) + ')' for p in self.ports])
            s += ')'
        s += ';\n\n'
        s += self.praw
        return s



#################################################################################
 # class name       : VerilogWriter
 # description      : write verilog or system verilog file
 #                    
 # returns          : this class
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
class VerilogWriter:
    def __init__(self, name, is_rtl = True, is_dont_touch = False, is_keep_hier = False, description = ""):
        self.name           = name
        self.parameters     = []  
        self.ports          = []  
        self.insts          = []
        self.is_rtl         = is_rtl
        self.is_dont_touch  = is_dont_touch 
        self.is_keep_hier   = is_keep_hier
        self.description    = description



    def gen_head(self):
        desp = self.description.split('\n')
        s =  "//////////////////////////////////////////////////////////////////////////////////"+"\n"
        s += "// Company       : TSU"+"\n"
        s += "// Engineer      : "+"\n"
        s += "// "+"\n"
        s += "// Create Date   : {date}\n".format(date=datetime.date.today())
        s += "// File Name     : {mname}.v\n".format(mname=self.name)
        s += "// Project Name  : "+"\n"
        s += "// Design Name   : "+"\n"
        s += "// Description   : "+"\n"
        for str in desp:
            s += "//                {}\n".format(str)
        s += "// "+"\n"
        s += "// Dependencies  : "+"\n"
        s += "// "+"\n"
        s += "// Revision      : "+"\n"
        s += "//                 - V1.0 File Created"+"\n"
        s += "// Additional Comments:"+"\n"
        s += "// "+"\n"
        s += "//////////////////////////////////////////////////////////////////////////////////"+"\n"
        s += "// "+"\n"
        return s



    def add(self, obj):
        if isinstance(obj, Instance):
            self.insts += [obj]
        elif isinstance(obj, ModuleParameter):
            self.parameters += [obj]
        elif isinstance(obj, ModulePort):
            self.ports += [obj]
        elif isinstance(obj, Wire):
            self.insts += [obj]
        elif isinstance(obj, Logic):
            self.insts += [obj]
        elif isinstance(obj, Raw):
            self.insts += [obj]
        else:
            raise Exception("Invalid type!" + str(obj))



    def write(self, file=None):
        s = self.gen_head()
        s += ("// WARNING: THIS FILE IS AUTOGENERATED\n"
             "// ANY MANUAL CHANGES WILL BE LOST\n"
             "\n")
        #s += "`default_nettype none\n"
        s += "`timescale 1ns/1ps\n"
        if self.is_dont_touch == True:
            s += """(*DONT_TOUCH="YES"*)"""
        if self.is_keep_hier  == True:
            s += "(* KEEP_HIERARCHY=\"TRUE\" *)"
        s += "module {name}".format(name=self.name)        
        if self.ports:
            if self.parameters:
                max_par_len = max([len(p.range()) for p in self.parameters])
                s += '   #(\n    '   
                s += ',\n    '.join([p.write(max_par_len) for p in self.parameters])  
                s += '\n  )'
            max_len = max([len(p.range()) for p in self.ports])
            s += '(\n    '
            s += ',\n    '.join([p.write(max_len) for p in self.ports])
            s += ')'
        s += ';\n\n'
        
        len_insts = len(self.insts)
        max_len = 8
        for j in range(0, len_insts):
            obj = self.insts[j]
            if isinstance(obj, Wire):
                _tmp = len(obj.range())
                if (max_len < _tmp):
                    max_len = _tmp
            if isinstance(obj, Logic):
                _tmp = len(obj.range())
                if (max_len < _tmp):
                    max_len = _tmp

        for j in range(0, len_insts):
            obj = self.insts[j]
            if isinstance(obj, Instance):
                s += obj.write()
                s += '\n' 
            if isinstance(obj, Wire):
                s += obj.write(max_len + 1)
            if isinstance(obj, Logic):
                s += obj.write(max_len + 1)
            if isinstance(obj, Raw):
                s += obj.write()

        s += 'endmodule\n'
        if file is None:
            return s
        else:
            fname = os.getcwd()
            if self.is_rtl:
                fname += "/src/" + file
                if not os.path.exists('src'):
                    os.mkdir('src')
            else:
                fname += "/tb/" + file
                if not os.path.exists('tb'):
                    os.mkdir('tb')                
            f = open(fname,'w')
            f.write(s)
