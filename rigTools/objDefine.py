"""
Module for adding a custom attribute that defines the role of a joint
"""
import maya.cmds as mc

def definer( objType ,objectList, definition):
    
    """
    @param objType: String, attribute name common ones include BoneType and ControlType
    @param objList: List, the joints you want to define
    @param definition: String, the definition of the object common ones are FK, IK and Bind
    """
    
    for i in objectList:
        mc.addAttr(i, longName = objType, dt ='string')
        mc.setAttr(str(i) + "." + objType , definition , type = "string", lock = 1)
        
    