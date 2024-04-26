import datetime
import os



#################################################################################
 # class name       : port
 # description      : the ports for SDC
 #                    
 # input            : @name     : the name
 # input            : @dir      : the direct of this port
 # input            : @width    : the width of this port
 # input            : @clock    : the clock index of this port in clock class list
 # returns          : no
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
class port:
    def __init__(self, name, dir, width, clock):
        self.name           = name
        self.width          = width
        self.dir            = dir
        self.clock          = clock



#################################################################################
 # class name       : clock
 # description      : the clock for SDC
 #                    
 # input            : @name     : the name
 # input            : @period   : the its period
 # returns          : no
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
class clock:
    def __init__(self, name, period):
        self.name           = name
        self.period         = period



#################################################################################
 # class name       : reset
 # description      : the reset for SDC
 #                    
 # input            : @name           : the name
 # input            : @active_level   : the acitve level
 # returns          : no
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
class reset:
    def __init__(self, name, active_level):
        self.name           = name
        self.active_level   = active_level



#################################################################################
 # class name       : SdcWriter
 # description      : generate the SDC constraints file
 #                    
 # input            : @name     : the SDC name
 # 
 # function         : @add_port : add port
 # function         : @add_clock: add clock
 # function         : @add_reset: add reset
 # function         : @write    : write SDC file
 #
 # returns          : no
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
class SdcWriter:
    def __init__(self, name):
        self.name               = name
        self.ports              = []  
        self.clocks             = []
        self.resets             = []
        self.input_delay_ratio  = 0.5
        self.output_delay_ratio = 0.2
        self.uncertainty_ratio  = 0.1



    def add_port(self, name, dir, width, clock):
        prefix = 'o' if int(1) == dir else 'i'
        pin_name = "{}_{}".format(prefix, name)        
        self.ports.append(port(pin_name, dir, width, clock))



    def add_clock(self, name, period):
        self.clocks.append(clock(name, period))



    def add_reset(self, name, active_level):
        self.resets.append(reset(name, active_level))



    def write(self):
        file = "{}.sdc".format(self.name)
        s = ""
        for i in range(0, len(self.clocks)):
            s = "set CLK_PERIOD {:.3f}\n".format(self.clocks[i].period)
            s += "create_clock -period $CLK_PERIOD [get_ports {}] -name clock{}\n".format(self.clocks[i].name, i)
            s += "set_clock_uncertainty -setup [expr $CLK_PERIOD*{:.3f}] [get_clocks clock{}]\n".format(self.uncertainty_ratio, i)

        s += "\n"
        for i in range(0, len(self.ports)):
            if self.ports[i].dir == int(0):
                s += "set_input_delay -max {:.3f} -clock clock{} [get_ports {}]\n".format(self.input_delay_ratio*self.clocks[self.ports[i].clock].period, self.ports[i].clock, self.ports[i].name)
                s += "set_input_delay -min {:.3f} -clock clock{} [get_ports {}]\n".format(self.input_delay_ratio*self.clocks[self.ports[i].clock].period, self.ports[i].clock, self.ports[i].name)
            else:
                s += "set_output_delay -max {:.3f} -clock clock{} [get_ports {}]\n".format(self.output_delay_ratio*self.clocks[self.ports[i].clock].period, self.ports[i].clock, self.ports[i].name)
                s += "set_output_delay -min {:.3f} -clock clock{} [get_ports {}]\n".format(self.output_delay_ratio*self.clocks[self.ports[i].clock].period, self.ports[i].clock, self.ports[i].name)
        
        if file is None:
            return s
        else:
            fname = os.getcwd()
            fname += "/sdc/" + file
            if not os.path.exists('sdc'):
                os.mkdir('sdc')
            f = open(fname,'w')
            f.write(s)
