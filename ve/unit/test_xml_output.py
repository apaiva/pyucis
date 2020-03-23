'''
Created on Mar 22, 2020

@author: ballance
'''
import os
from pyucis import UCIS_HISTORYNODE_TEST, UCIS_TESTSTATUS_OK, UCIS_OTHER, \
    UCIS_DU_MODULE, UCIS_ENABLED_STMT, UCIS_ENABLED_BRANCH, UCIS_ENABLED_COND, \
    UCIS_ENABLED_EXPR, UCIS_ENABLED_FSM, UCIS_ENABLED_TOGGLE, UCIS_INST_ONCE, \
    UCIS_SCOPE_UNDER_DU, UCIS_INSTANCE, UCIS_VLOG
from pyucis.mem.mem_factory import MemFactory
from pyucis.test_data import TestData
from unittest.case import TestCase

from pyucis import SourceInfo
from pyucis.xml.xml_writer import XmlWriter
from _io import StringIO
from pyucis.xml.xml_reader import XmlReader
from pyucis.xml.ucis_validator import UcisValidator
from pyucis.xml import validate_ucis_xml


class TestXmlOutput(TestCase):
    
    def test_simplest_create(self):
        print("-- test_simplest_create")
        
        ucisdb = "file.ucis"
        db = MemFactory.create()
        
        testnode = db.createHistoryNode(
            None, 
            "logicalName",
            ucisdb,
            UCIS_HISTORYNODE_TEST)
        td = TestData(
            teststatus=UCIS_TESTSTATUS_OK,
            toolcategory="UCIS:simulator",
            date="20200202020"
            )
        testnode.setTestData(td)
        
        file = db.createFileHandle("dummy", os.getcwd())

        srcinfo = SourceInfo(file, 0, 0)
        du = db.createScope(
            "foo.bar",
            srcinfo,
            1, # weight
            UCIS_OTHER,
            UCIS_DU_MODULE,
            UCIS_ENABLED_STMT | UCIS_ENABLED_BRANCH
            | UCIS_ENABLED_COND | UCIS_ENABLED_EXPR
            | UCIS_ENABLED_FSM | UCIS_ENABLED_TOGGLE
            | UCIS_INST_ONCE | UCIS_SCOPE_UNDER_DU
            )
        
        instance = db.createInstance(
            "dummy",
            None, # sourceinfo
            1, # weight
            UCIS_OTHER,
            UCIS_INSTANCE,
            du,
            UCIS_INST_ONCE)
        
        cg = instance.createCovergroup(
            "cg",
            SourceInfo(file, 3, 0),
            1, # weight
            UCIS_OTHER)
        
        cp = cg.createCoverpoint(
            "t",
            SourceInfo(file, 4, 0),
            1, # weight
            UCIS_VLOG
            )
        cp.setComment("Hello There")
        
        print("--> createBin")
        cp.createBin(
            "auto[a]",
            SourceInfo(file, 4, 0),
            1,
            4,
            "a")
        print("<-- createBin")

        out = StringIO()
        writer = XmlWriter()
        writer.write(out, db)
        
        print("XML Output:\n" + out.getvalue())
        input = StringIO(out.getvalue())
        validate_ucis_xml(input)
