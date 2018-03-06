"""
Title: Object
BIA 662 : Assignment 1
Exercise 2.10
Authors: Team 4
Feb 28, 2018
"""

#class that represents one object within matrix (i.e. X, Y, Z, etc.)
class Object:

    def __init__(self, name):
        self.name=name
        self.attributes={}

    def getName(self):
        return self.name

    def getAttributes(self):
        return self.attributes

