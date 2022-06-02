"""
Module for creating the base rig structure
"""
import maya.cmds as mc
from ranglerig2.rigTools import controlGen
from ranglerig2.rigTools import assetColourer
from ranglerig2.rigTools import attrLocker
from ranglerig2.rigTools import objDefine



class baseGen():
    
    def __init__(self, characterName):
        characterName = characterName
        sceneObjectType = 'Rig'
        
        #Generates Groups
        self.settingGrp = mc.group(name = 'settings_grp', empty = True)
        self.visibilityGrp = mc.group(name = 'visibility_grp', empty = True)
        self.animGrp = mc.group(name = 'anim_grp', empty = True)
        self.geoGrp = mc.group(name = 'geo_grp', empty = True)
        self.rigGrp =  mc.group(self.animGrp, self.settingGrp ,name = characterName + "_rig", empty = True) 
        mc.parent(self.settingGrp, self.visibilityGrp, self.animGrp, self.geoGrp, self.rigGrp)
        
        #Turns off inherit Transforms on  geoGrp
        mc.setAttr(self.geoGrp + ".inheritsTransform", 0)
        
        
        #Creates Global Scale Attribute
        mc.connectAttr(self.rigGrp +'.scaleY', self.rigGrp +'.scaleX', force = True)
        mc.connectAttr(self.rigGrp +'.scaleY', self.rigGrp +'.scaleZ', force = True)
        self.globScale = mc.aliasAttr('globalScale' ,self.rigGrp +'.scaleY')
        
        # Creates Shape for rigGrp
        controlGen.generate4Arrow('arrow', self.rigGrp, True, False)
        assetColourer.colourer([self.rigGrp], 22)
        
        
        #Clean Up Attributes
        attrLocker.lockCommon(self.rigGrp,[],[],["X","Z"], False,True)
        attrLocker.lockCommon(self.animGrp,["X","Y","Z"],["X","Y","Z"],["X","Y","Z"], False,True)
        attrLocker.lockCommon(self.settingGrp,["X","Y","Z"],["X","Y","Z"],["X","Y","Z"], False,True)
        attrLocker.lockCommon(self.visibilityGrp,["X","Y","Z"],["X","Y","Z"],["X","Y","Z"], False,True)
        
        '''
        #Add Attributes to settings_grp
        mc.select(self.settingGrp)
        mc.addAttr( shortName='HeadTrans', longName='HeadTrans', attributeType = 'enum', enumName = 'World:Chest:Neck' , keyable = True, hidden = False )
        mc.addAttr( shortName='HeadOri', longName='HeadOri', attributeType = 'enum', enumName = 'World:Chest:Neck' , keyable = True, hidden = False )
        
        mc.addAttr( shortName='LeftHandTrans', longName='LeftHandTrans', attributeType = 'enum', enumName = 'World:Hips:Chest:Head' , keyable = True, hidden = False )
        mc.addAttr( shortName='LeftHandOri', longName='LeftHandOri', attributeType = 'enum', enumName = 'World:Hips:Chest:Head' , keyable = True, hidden = False )

        mc.addAttr( shortName='RightHandTrans', longName='RightHandTrans', attributeType = 'enum', enumName = 'World:Hips:Chest:Head' , keyable = True, hidden = False )
        mc.addAttr( shortName='RightHandOri', longName='RightHandOri', attributeType = 'enum', enumName = 'World:Hips:Chest:Head' , keyable = True, hidden = False )
        
        mc.addAttr( shortName='L_leg_Fk_IK', longName='L_leg_Fk_IK', attributeType = 'enum', enumName = 'FK:IK' , keyable = True, hidden = False )
        mc.addAttr( shortName='R_leg_Fk_IK', longName='R_leg_Fk_IK', attributeType = 'enum', enumName = 'FK:IK' , keyable = True, hidden = False )
        mc.addAttr( shortName='L_arm_Fk_IK', longName='L_arm_Fk_IK', attributeType = 'enum', enumName = 'FK:IK' , keyable = True, hidden = False )
        mc.addAttr( shortName='R_arm_Fk_IK', longName='R_arm_Fk_IK', attributeType = 'enum', enumName = 'FK:IK' , keyable = True, hidden = False )
        
        #Add Attributes to visibility_grp
        
        mc.select(self.visibilityGrp)
        mc.addAttr( shortName='Head', longName='Head', attributeType = 'enum', enumName = 'Head:Head&Neck:Off' , keyable = True, hidden = False )
        mc.addAttr( shortName='Torso', longName='Torso', attributeType = 'enum', enumName = 'FK:IK:Both:None' , keyable = True, hidden = False )
        mc.addAttr( shortName='R_leg', longName='R_leg', attributeType = 'enum', enumName = 'FK:IK:Both:None' , keyable = True, hidden = False )
        mc.addAttr( shortName='L_leg', longName='L_leg', attributeType = 'enum', enumName = 'FK:IK:Both:None' , keyable = True, hidden = False )
        mc.addAttr( shortName='R_Clav', longName='R_Clav', attributeType = 'enum', enumName = 'On:Off' , keyable = True, hidden = False )
        mc.addAttr( shortName='L_Clav', longName='L_Clav', attributeType = 'enum', enumName = 'On:Off' , keyable = True, hidden = False )
        mc.addAttr( shortName='R_arm', longName='R_arm', attributeType = 'enum', enumName = 'FK:IK:Both:None' , keyable = True, hidden = False )
        mc.addAttr( shortName='L_arm', longName='L_arm', attributeType = 'enum', enumName = 'FK:IK:Both:None' , keyable = True, hidden = False )
        mc.addAttr( shortName='L_hand', longName='L_hand', attributeType = 'enum', enumName = 'On:Off' , keyable = True, hidden = False )
        mc.addAttr( shortName='R_hand', longName='R_hand', attributeType = 'enum', enumName = 'On:Off' , keyable = True, hidden = False )
        '''
        
        #Define settings_grp, visibility_grp and rigGrp
        objDefine.definer('characterName', [self.visibilityGrp], characterName)
        objDefine.definer('controlArea', [self.visibilityGrp], "master")
        objDefine.definer('controlType', [self.visibilityGrp], "visibility")
        
        objDefine.definer('characterName', [self.settingGrp], characterName)
        objDefine.definer('controlArea', [self.settingGrp], "master")
        objDefine.definer('controlType', [self.settingGrp], "settings")
        
        objDefine.definer('characterName', [self.rigGrp], characterName)
        objDefine.definer('sceneObjectType', [self.rigGrp], "rig")
        objDefine.definer('controlType', [self.rigGrp], "master")