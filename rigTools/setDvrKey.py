"""
Module for Setting Driven Keys
"""
import maya.cmds as mc

def setDvrK(Driver, Driven, DriverVal, DrivenVal):
    """
    Locks Common attributes
    @param Driver: Str, name of Driver Object AND Attribute eg 'cube1.translate' 
    @param Driven: Str, name of Driven Object AND Attribute eg 'cube1.rotate' 
    @param DriverVal: Float, the value to set the driver to
    @param DrivenVal: Float, the value to set the driven to
    """
    
    mc.setDrivenKeyframe(Driven, currentDriver = Driver, driverValue =DriverVal, value = DrivenVal)