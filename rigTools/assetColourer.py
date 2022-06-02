"""
Module for setting colour overide
"""
import maya.cmds as mc

def colourer(obj, colour):
    
    """
    Overrides the Colour of an object
    @param obj: List, name of objects to override the colour of
    @param colour:Float, number of colour. Yellow 22, Blue 6 , Red 13 ,
    """
        
    for i in obj:
        mc.setAttr(str(i) + '.overrideEnabled', 1)
        mc.setAttr(str(i) + '.overrideColor', colour)