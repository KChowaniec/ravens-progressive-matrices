# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 17:13:30 2018

@author: Kathy
"""

#represents one matrix in problem (i.e. A, B, C, etc)
class Matrix:

    def __init__(self, name):
        self.name=name
        self.objects=[]

    def getName(self):
        return self.name

    def getObjects(self):
        return self.objects
