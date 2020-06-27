#!/usr/bin/env python
# coding: utf-8

# In[2]:

class Search(object):
    # Constructor 
    def __init__(self):
        var_inp = input('Hola! Please enter an item you want to search: ')
        self.name = var_inp
    
    # Methods
    def getName(self):
        return self.name
