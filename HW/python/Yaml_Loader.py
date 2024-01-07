#!/usr/bin/env python3

import sys
import yaml

from collections import OrderedDict, defaultdict



#################################################################################
 # class name       : yaml_load
 # description      : This is the loader of the YAML file
 #                    
 # returns          : this class
 # algorithm        : 
 #                    no 
 #                    
 # 
#################################################################################
def yaml_load(file, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))



    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)


    
    return yaml.load(open(file), OrderedLoader)



