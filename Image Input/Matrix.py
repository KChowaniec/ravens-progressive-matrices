"""
Title: Matrix 
BIA 662 : Assignment 1
Exercise 2.10
Authors: Team 4
Feb 28, 2018
"""

#class that represents one matrix in problem (i.e. A, B, C, etc)
class Matrix:

    def __init__(self, name):
        self.name=name
        self.objects={}

    def getName(self):
        return self.name

    def getObjects(self):
        return self.objects
