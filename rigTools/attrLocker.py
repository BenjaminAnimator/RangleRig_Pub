"""
Module for locking common attributes on Objects
"""
import maya.cmds as mc

def lockCommon(object, translate, rotate, scale, visibility, hide):
    """
    Locks Common attributes
    @param object: String, the object you wish to lock attributes
    @param translate: List, the axis you wish to lock eg ['X','Y','Z']
    @param rotate: List, the axis you wish to lock eg ['X','Y','Z']
    @param scale: List, the axis you wish to lock eg ['X','Y','Z']
    @param visibility: Boolean
    @param hide:Boolean, if True will hide locked attr 
    """
    '''axis = [[]
            ['X'],
            ['Y'],
            ['Z'],
            ['X','Y']
            ['X','Z']
            ['Y','Z']
            ['X','Y', 'Z']
            ]
    '''
    
    if translate:
        if hide == True:
            for i in translate:
                mc.setAttr(object + '.translate' + i ,lock = True, channelBox = False, keyable = False)
        
        else:    
            for i in translate:
                mc.setAttr(object + '.translate' + i ,lock = True)
    else: None
       
        
    if rotate:
        if hide == True:
            for i in rotate:
                mc.setAttr(object + '.rotate' + i ,lock = True, channelBox = False,keyable = False)
        else:
            for i in rotate:
                mc.setAttr(object + '.rotate' + i ,lock = True)
    else: None
    
    
            
    if scale:
        if hide == True:
          for i in scale:
                mc.setAttr(object + '.scale' + i ,lock = True, channelBox = False,keyable = False)      
        else:
            for i in scale:
                mc.setAttr(object + '.scale' + i ,lock = True)
    else: None
        
            
    if visibility:
        if hide == True:
            mc.setAttr(object + '.visibility' ,lock = True, channelBox = False,keyable = False)
        
            
        else:
            mc.setAttr(object + '.visibility' ,lock = True)
        
    else: None