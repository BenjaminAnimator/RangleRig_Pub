"""
Module for creating fk/ik switch via blend colour node
"""
import maya.cmds as mc

def blendColour(fkJoint, ikJoint, drivenJoint, attribute, controller):
    
    """
    Creates FK Ik switch using a blendColours node and links it to a controller if true
    @param fkJoint: String, the name of the FK joint
    @param ikJoint: String, the name of the IK joint
    @param drivenJoint: String, the name of the joint to be driven
    @param attribute: String, the long hand (translate, rotate) or short hand (t, r) for the attribute
    @param controller: String, the full name of the controller object and attribute e.g leg_anim.FK_IK
    """
    
    axis =["X", "Y", "Z"]
    col = ["R", "G", "B"]
    blndNode = mc.shadingNode('blendColors', asUtility = True, name = drivenJoint + '_' + attribute + '_blndColours')
    mc.connectAttr(ikJoint + "."  + attribute, blndNode + ".color1")
    mc.connectAttr(fkJoint + "."  + attribute, blndNode + ".color2")
    
    for i in range(0,3) :
            
        mc.connectAttr(blndNode + ".output" + col[i], drivenJoint + "." + attribute + axis[i], force = True)
    
    if controller:
        mc.connectAttr(controller, blndNode + ".blender")
    
    else:None
    