"""
Module for selecting a joint Hirearchy
"""

import maya.cmds as mc

def jntHirearch(baseJnt,listBase, types = 'joint', descendants = True):
    
    """
    Lists all descendants under selected joint
    @param baseJnt:String, the joint from which all descendent will be listed from. If String = false the currently selected joint will be used
    @param listBase: Boolean, whether the base joint is included in the list
    @return: List of all 
    """
    
    baseJoint = baseJnt
    print baseJoint

    
    jntList =  mc.listRelatives(baseJoint, allDescendents = descendants, type = types)
    
    if listBase:    
        jntList.append(baseJoint)
        jntList.reverse()
        
    
    else:
        jntList.reverse()
    
    
    return jntList