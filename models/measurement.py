__author__ = 'Robert W. Curtiss'
__project__ = 'NutFlask'

from models.nutflaskbase import NutFlaskBase

"""
====================================================
Author: Robert W. Curtiss
    Project: NutFlask
    File: measurement
    Created: Aug, 31, 2020
    
    Description:
    
===================================================
"""
class MeasurementBase(NutFlaskBase):
    def __init__(self,name):
        super().__init__()
        self.name = name

