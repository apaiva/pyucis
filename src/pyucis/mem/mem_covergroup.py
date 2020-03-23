'''
Created on Jan 12, 2020

@author: ballance
'''
from pyucis import UCIS_COVERGROUP
from pyucis.cover_type import CoverType
from pyucis.covergroup import Covergroup
from pyucis.mem.mem_cvg_scope import MemCvgScope

from vsc.model.source_info import SourceInfo


class MemCovergroup(MemCvgScope,Covergroup):
    
    def __init__(self,
                 parent,
                 name,
                 srcinfo,
                 weight,
                 source):
        MemCvgScope.__init__(self, parent, name, srcinfo, weight, source, 
                         UCIS_COVERGROUP, 0)
        Covergroup.__init__(self)
        self.at_least = 0
        self.auto_bin_max
        self.m_per_instance = True
        self.m_merge_instances = True
        
    def getAtLeast(self)->int:
        return self.at_least
    
    def setAtLeast(self, atleast):
        self.at_least = atleast
        
    def getAutoBinMax(self)->int:
        return self.auto_bin_max
    
    def setAutoBinMax(self, auto_max):
        self.auto_bin_max = auto_max
        
    def getPerInstance(self)->bool:
        return self.m_per_instance
    
    def setPerInstance(self, perinst):
        self.m_per_instance = perinst
    
    def getMergeInstances(self)->bool:
        return self.m_merge_instances
    
    def setMergeInstances(self, m:bool):
        self.m_merge_instances = m
        
    def createCoverpoint(self, 
        name:str, 
        srcinfo:SourceInfo, 
        weight:int, 
        source)->CoverType:
        from .mem_coverpoint import MemCoverpoint
        ret = MemCoverpoint(self, name, srcinfo, weight, source)
        self.m_children.append(ret)
        return ret
    
    