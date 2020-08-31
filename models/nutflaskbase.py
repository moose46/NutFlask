__author__ = 'Robert W. Curtiss'
__project__ = 'NutFlask'

from datetime import datetime

"""
====================================================
Author: Robert W. Curtiss
    Project: NutFlask
    File: base
    Created: Aug, 30, 2020
    
    Description:
    
===================================================
"""
class NutFlaskBase():
    def __init__(self,date_created=None,date_updated=None):
        self.today = datetime.today().isoformat()
        self.date_created = self.today if date_created is None else date_created
        self.date_updated = self.today if date_updated is None else date_updated

