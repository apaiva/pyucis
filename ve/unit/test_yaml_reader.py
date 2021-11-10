'''
Created on Nov 10, 2021

@author: mballance
'''
from unittest.case import TestCase
from ucis.yaml.yaml_reader import YamlReader
from _io import StringIO
from ucis.report.coverage_report_builder import CoverageReportBuilder

class TestYamlReader(TestCase):
    
    def test_type_cvg_cvp(self):
        text = """
        coverage:
            covergroups:
                - type-name: cvg
                
                  coverpoints:
                    - name: cp1
                      bins:
                        - name: b0
                          count: 1
                        - name: b1
                          count: 0
        """
        
        db = YamlReader().loads(StringIO(text))
        rpt = CoverageReportBuilder.build(db)
        
        self.assertEqual(len(rpt.covergroups), 1)
        self.assertEqual(rpt.covergroups[0].name, "cvg")
        self.assertEqual(len(rpt.covergroups[0].coverpoints), 1)
        self.assertEqual(len(rpt.covergroups[0].coverpoints[0].bins), 2)
        self.assertEqual(rpt.covergroups[0].coverpoints[0].coverage, 50.0)

    def test_type_cvg_2_cvp(self):
        text = """
        coverage:
            covergroups:
                - type-name: cvg
                
                  coverpoints:
                    - name: cp1
                      bins:
                        - name: b0
                          count: 1
                        - name: b1
                          count: 0
                    - name: cp2
                      bins:
                        - name: b0
                          count: 1
                        - name: b1
                          count: 1
        """
        
        db = YamlReader().loads(StringIO(text))
        rpt = CoverageReportBuilder.build(db)
        
        self.assertEqual(len(rpt.covergroups), 1)
        self.assertEqual(rpt.covergroups[0].name, "cvg")
        self.assertEqual(len(rpt.covergroups[0].coverpoints), 2)
        self.assertEqual(len(rpt.covergroups[0].coverpoints[0].bins), 2)
        self.assertEqual(len(rpt.covergroups[0].coverpoints[1].bins), 2)
        self.assertEqual(rpt.covergroups[0].coverage, 75.0)
        