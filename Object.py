# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 17:14:02 2018

@author: Kathy
"""

#represents one object within matrix (i.e. X, Y, Z, etc.)
class Object:

    def __init__(self, name):
        self.name=name
        self.attributes={}

    def getName(self):
        return self.name

    def getAttributes(self):
        return self.attributes

