#!/usr/bin/env python3
import math
import sys
import re
import os


class KeyWord:
    def __init__(self, keyword):
        self.keyword        = keyword
        self.Resultlist     = []



#################################################################################
 # class name       : Log_parse
 # description      : find file out including the keywords 
 #                    and wirte the files name to a log file
 # input            : @root     : the work directory which is searched
 # returns          : no
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
class Log_parse:
    def __init__(self, root = "."):
        self.root           = root
        self.keywordlist    = []
        self.suffixlist     = []



    def add_keyword(self, keyword):
        self.keywordlist.append(KeyWord(keyword))



    def add_exclude_suffix(self, suffix):
        self.suffixlist.append(suffix)



    def find_keyword(self, keyword, directory):
        result = []
        pattern = keyword + '.*'
        print(pattern)
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.islink(file_path):
                    break
                k = len(file_path.split("."))
                if (k < 2):
                    break
                filetype = file_path.split(".")[k-1]
                bypass = int(0)
                for i in range(0, len(self.suffixlist)):
                    if filetype == self.suffixlist[i]:
                        bypass = int(1)
                if bypass == int(0):
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if re.search(pattern, content):
                            result.append(file_path)
        return result



    def search(self):
        for i in range(0, len(self.keywordlist)):
            keyword = self.keywordlist[i].keyword
            results = self.find_keyword(keyword, self.root)
            if len(results) > int(0):
                self.keywordlist[i].Resultlist = self.keywordlist[i].Resultlist + results



    def write(self):
        if not os.path.exists('sim/checklog'):
            os.mkdir('sim/checklog')        
        for i in range(0, len(self.keywordlist)):
            keyword = self.keywordlist[i].keyword
            output_file = "check_{}.log".format(keyword)
            s = "{} {} are found\n".format(len(self.keywordlist[i].Resultlist), keyword)
            for j in range(0, len(self.keywordlist[i].Resultlist)):
                s += "{}\n".format(self.keywordlist[i].Resultlist[j])
            fname = os.getcwd()
            fname += "/sim/checklog/" + output_file
            f = open(fname,'w')
            f.write(s)




#################################################################################
 # function name    : main proc
 # description      : main proc for Log_parse 
 #                    
 # input            : @root     : the work directory which is searched
 # input            : @keyword0 : the keyword to be searched in the files
 # input            : @keyword1 : the keyword to be searched in the files
 # returns          : no
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise Exception("Invalid parameters!\n example: python Log_parse.py path keyword1 keyword2 ...")

    root = sys.argv[1]
    keyword = []
    for i  in range(2,len(sys.argv)):
        keyword.append(sys.argv[i])

    g = Log_parse(root)
    for i in range(0, len(keyword)):
        g.add_keyword(keyword[i])
    
    g.add_keyword("Warning")
    g.add_keyword("Warn")
    g.add_keyword("error")
    g.add_keyword("Error")    
    g.add_keyword("FATAL")
    g.add_keyword("ERROR")
    g.add_keyword("WARNING")


    g.add_exclude_suffix("sv")
    g.add_exclude_suffix("v")
    g.add_exclude_suffix("py")
    g.add_exclude_suffix("sdb")
    g.add_exclude_suffix("flist")
    g.add_exclude_suffix("c")
    g.add_exclude_suffix("h")
    g.add_exclude_suffix("cpp")
    g.add_exclude_suffix("so")
    g.add_exclude_suffix("db")
    g.add_exclude_suffix("lib")
    g.add_exclude_suffix("etc/_oharch")
    g.add_exclude_suffix("a")
    g.add_exclude_suffix("swp")

    g.search()
    g.write()


