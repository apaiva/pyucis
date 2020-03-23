from pyucis.history_node_kind import HistoryNodeKind
from typing import Dict, Iterator
from pyucis.scope import Scope
from pyucis.scope_type_t import ScopeTypeT
from pyucis.covergroup import Covergroup

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

'''
Created on Jan 5, 2020

@author: ballance
'''

from lxml import etree as et
from pyucis.ucis import UCIS
from lxml.etree import QName, tounicode, SubElement
from pyucis.statement_id import StatementId
from datetime import datetime

class XmlWriter():
    
    UCIS = "http://www.w3.org/2001/XMLSchema-instance"
    
    def __init__(self):
        self.db = None
        self.root = None
        self.file_id_m : Dict[str,int] = {}
        pass
    
    def write(self, file, db : UCIS):
        self.db = db

        # Map each of the source files to a unique identifier
        self.file_id_m = {
            "__null__file__" : 1}
        self.find_all_files(db.scopes(ScopeTypeT.ALL)) # TODO: need to handle mask
        
        self.root = et.Element(QName(XmlWriter.UCIS, "UCIS"), nsmap={
#        self.root = et.Element("UCIS", nsmap={
            "ucis" : XmlWriter.UCIS
            })
        self.setAttr(self.root, "writtenBy", db.getWrittenBy())
        self.setAttrDateTime(self.root, "writtenTime", db.getWrittenTime())
        
        self.setAttr(self.root, "ucisVersion", db.getAPIVersion())
        
        # TODO: collect source files
        self.write_source_files()
        self.write_history_nodes()
        self.write_instance_coverages()

#        file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
#        file.write("<?xml version=\"1.0\"?>\n")
        file.write(tounicode(self.root, pretty_print=True))
        
    def write_source_files(self):

        for filename,id in self.file_id_m.items():
            fileN = self.mkElem(self.root, "sourceFiles")
            self.setAttr(fileN, "fileName", filename)
            self.setAttr(fileN, "id", str(id))
        
    def write_history_nodes(self):
        
#        histNodes = self.root.SubElement(self.root, "historyNodes")

        for i,h in enumerate(self.db.getHistoryNodes(HistoryNodeKind.ALL)):
            print("i=" + str(i))
            histN = self.mkElem(self.root, "historyNodes")
            histN.set("historyNodeId", str(i))
            
            # TODO: parent
            histN.set("logicalName", h.getLogicalName())
            self.setIfNonNull(histN, "physicalName", h.getPhysicalName())
            self.setIfNonNull(histN, "kind", h.getKind())
            self.setAttrBool(histN, "testStatus", h.getTestStatus())
            self.setIfNonNeg(histN, "simtime", h.getSimTime())
            self.setIfNonNull(histN, "timeunit", h.getTimeUnit())
            self.setIfNonNull(histN, "runCwd", h.getRunCwd())
            self.setIfNonNeg(histN, "cpuTime", h.getCpuTime())
            self.setIfNonNull(histN, "seed", h.getSeed())
            self.setIfNonNull(histN, "cmd", h.getCmd())
            self.setIfNonNull(histN, "args", h.getArgs())
            self.setIfNonNull(histN, "compulsory", h.getCompulsory())
            self.setAttrDateTime(histN, "date", h.getDate())
            self.setIfNonNull(histN, "userName", h.getUserName())
            self.setIfNonNeg(histN, "cost", h.getCost())
            self.setAttr(histN, "toolCategory", h.getToolCategory())
            self.setAttr(histN, "ucisVersion", h.getUCISVersion())
            self.setAttr(histN, "vendorId", h.getVendorId())
            self.setAttr(histN, "vendorTool", h.getVendorTool())
            self.setAttr(histN, "vendorToolVersion", h.getVendorToolVersion())
            self.setIfNonNeg(histN, "sameTests", h.getSameTests())
            self.setIfNonNull(histN, "comment", h.getComment())
            
            # TODO: userAttr
            
    def write_instance_coverages(self):
        print("write_instance_coverages")
        inst = self.mkElem(self.root, "instanceCoverages")
        inst.set("name", "my_scope") # TODO:
        inst.set("key", "AABBCCDD") # TODO:
        self.addId(inst, None)
        
        for s in self.db.scopes(ScopeTypeT.INSTANCE):
            self.write_covergroups(inst, s)
        
#         for i,c in enumerate(self.db.getCoverInstances()):
#             coverI = self.mkElem(self.root, "instanceCoverages")
#             self.setAttr(coverI, "name", c.getName())
#             self.setAttr(coverI, "key", c.getKey())
#             
#             self.write_statement_id(c.getId(), coverI)
            
    def write_covergroups(self, inst, scope):
        print("write_covergroups: " + str(scope))
        
        for cg in scope.scopes(ScopeTypeT.COVERGROUP):
            cgElem = self.mkElem(inst, "covergroupCoverage")
#            self.setAttr(cgElem, "weight", str(scope.getWeight()))
                
            print("cg=" + str(cg))
            self.write_coverinstance(cgElem, cg.getScopeName(), cg)
            
            for ci in cg.scopes(ScopeTypeT.COVERINSTANCE):
                self.write_coverinstance(cgElem, cg.getScopeName(), ci)
    
    def write_coverinstance(self, cgElem, cgName, cg : Covergroup):
        cgInstElem = self.mkElem(cgElem, "cgInstance")
        self.setAttr(cgInstElem, "name", cg.getScopeName())
        self.setAttr(cgInstElem, "key", "1")
        
        self.write_options(cgInstElem, cg)
        
        cgIdElem = self.mkElem(cgInstElem, "cgId")
        self.setAttr(cgIdElem, "cgName", cgName)
        self.setAttr(cgIdElem, "moduleName", cgName)
        
        # Instance source information
        cgSourceIdElem = self.mkElem(cgIdElem, "cginstSourceId")
        self.setAttr(cgSourceIdElem, "file", "1")
        self.setAttr(cgSourceIdElem, "line", "1")
        self.setAttr(cgSourceIdElem, "inlineCount", "1")
        
        # Declaration source information
        cgSourceIdElem = self.mkElem(cgIdElem, "cgSourceId")
        self.setAttr(cgSourceIdElem, "file", "1")
        self.setAttr(cgSourceIdElem, "line", "1")
        self.setAttr(cgSourceIdElem, "inlineCount", "1")
        
        for cp in cg.scopes(ScopeTypeT.COVERPOINT):
            print("cp=" + str(cp))
            self.write_coverpoint(cgInstElem, cp)
            
    def write_coverpoint(self, cgInstElem, cp):
        self.write_options(cgInstElem, cp)
        
    
    def write_options(self, parent, opts_item):
        self.mkElem(parent, "options")
        

    def write_statement_id(self, stmt_id : StatementId, p, name="id"):
        stmtN = self.mkElem(p, name)
        # TODO: 
        file_id = self.file_id_m[stmt_id.getFile()]+1
        self.setAttr(stmtN, "file", str(file_id))
        self.setAttr(stmtN, "line", str(stmt_id.getLine()))
        self.setAttr(stmtN, "inlineCount", str(stmt_id.getItem()))
        
            
    def mkElem(self, p, name):
        # Creates a UCIS-qualified node
        return SubElement(p, QName(XmlWriter.UCIS, name))
        
    def setAttr(self, e, name, val):
#        e.set(QName(XmlWriter.UCIS, name), val)
        e.set(name, val)
        
    def setAttrBool(self, e, name, val):
        if val:
            e.set(name, "true")
        else:
            e.set(name, "false")

    def setAttrDateTime(self, e, name, val):
        val_i = int(val)
        self.setAttr(e, name, datetime.fromtimestamp(val_i).isoformat())
            
    def setIfNonNull(self, n, attr, val):
        if val is not None:
            self.setAttr(n, attr, str(val))
            
    def setIfNonNeg(self, n, attr, val):
        if val >= 0:
            self.setAttr(n, attr, str(val))
            
    def addId(self, ctxt, srcinfo):
        idElem = self.mkElem(ctxt, "id")
        if srcinfo is None or srcinfo.file is None:
            fileid = 1
        else:
            fileid = self.file_id_m[srcinfo.file.getFileName()]
        self.setAttr(idElem, "file", str(fileid))
            
        self.setAttr(idElem, "line",
                     str(srcinfo.line) if srcinfo is not None else str(1))
        
        self.setAttr(idElem, "inlineCount", 
            str(srcinfo.token) if srcinfo is not None else str(1))
        

    def find_all_files(self, scope_i : Iterator[Scope]):
        for s in scope_i:
            srcinfo = s.getSourceInfo()
            
            if srcinfo.file is not None:
                filename = srcinfo.file.getFileName()
                if filename not in self.file_id_m.keys():
                    id = len(self.file_id_m)+1
                    self.file_id_m[filename] = id
                    
            self.find_all_files(s.scopes(ScopeTypeT.ALL))
            