import maya.cmds as mc
from ranglerig2.rigTools  import blndColours
from ranglerig2.rigTools import selectHirearchy
from ranglerig2.rigTools import controlGen
from ranglerig2.rigTools  import assetColourer
from ranglerig2.rigTools  import attrLocker
from ranglerig2.rigTools  import objDefine
from ranglerig2.rigTools  import pvCalculator
from ranglerig2.rigTools  import setDvrKey

class armGen():
    def __init__(self, setupControlGrp, characterName, rigGrp, settingsGrp, visGrp):

        setupCon =  selectHirearchy.jntHirearch(setupControlGrp, False, descendants = False, types = "transform")
        setupCon.reverse()

        jntList = []

        for i in setupCon:
            trans = mc.xform(i, q=True , ws = True , rp= True)
            jnt = mc.joint(position  = trans)
            jntList.append(jnt)

        

        print jntList
        
        
        ID  = "arm"

        '''
        ID  = mc.getAttr(topjoint +'.UniqueID')
        self.setupJnt = topjoint
        
        rigJnts =  mc.duplicate(topjoint,  name = ID+'_01_Jnt', renameChildren = True)
        jnt1 = mc.rename(rigJnts[0], ID + '_01_Jnt')
        jnt2 = mc.rename(rigJnts[1], ID + '_02_Jnt')
        jnt3 = mc.rename(rigJnts[2], ID + '_03_Jnt')

       
        mc.setAttr(jnt1 + '.setUpJnt', lock= False)
        mc.setAttr(jnt1 + '.UniqueID', lock= False)
        mc.setAttr(jnt1 + '.characterName', lock= False)
        mc.setAttr(jnt1 + '.Connect_to', lock= False)
        mc.setAttr(jnt1 + '.Connection_type', lock= False)
        mc.deleteAttr(jnt1 + '.setUpJnt')
        mc.deleteAttr(jnt1 + '.characterName')
        mc.deleteAttr(jnt1 + '.UniqueID')
        mc.deleteAttr(jnt1 + '.Connect_to')
        mc.deleteAttr(jnt1 + '.Connection_type')
        
        locX = mc.getAttr(jnt1  + ".translateX")
        '''
        locX = mc.getAttr(jntList[0] + ".translateX")

        if locX > 0:
            assetCol = 6
            prefix = "L_"
            mc.joint(jntList[0] ,edit = True, orientJoint =  'xyz', secondaryAxisOrient = 'ydown', children = True,  zeroScaleOrient = True)

        
        elif locX < 0:
            assetCol = 13
            prefix = "R_"
            mc.joint(jntList[0] ,edit = True, orientJoint =  'xyz', secondaryAxisOrient = 'ydown', children = True,  zeroScaleOrient = True)

        else:
            assetCol = 22
            prefix = "M_"
        

        
        
        fkGrp = mc.duplicate(jntList[0],name = 'Fkjnt', renameChildren = True)
        ikGrp = mc.duplicate(jntList[0],name = 'ikjnt', renameChildren = True)
        
        armParts = ['Clav','Uparm', 'Loarm', 'Hand']
        
        count = 0
        fkJnts=[]
        for i in fkGrp:
            name =mc.rename(i, prefix + armParts[count] + '_fk_anim')
            fkJnts.append(name)
            count += 1
        
        count =0
        ikJnts=[]
        for i in ikGrp:
            name = mc.rename(i, prefix + armParts[count] + '_ik_jnt')
            ikJnts.append(name)
            count += 1
            
        count = 0
        baseJnts=[]
        for i in jntList:
            name =mc.rename(i, prefix + armParts[count] + '_base_jnt')
            baseJnts.append(name)
            count += 1

       
        armIkHandle= mc.ikHandle(name = prefix +'arm_ik_handle', startJoint = ikJnts[1] , endEffector =ikJnts[3], solver = 'ikRPsolver' )
        
        polVector = pvCalculator.pvCal(ikJnts[1], ikJnts[2], ikJnts[3], prefix + ID + 'arn_polvec')
        polVec = polVector.pvloc
        mc.poleVectorConstraint( polVec, armIkHandle[0] )
        
        mc.select(settingsGrp)
        mc.addAttr( shortName= prefix + ID  +'_Fk_IK', longName=prefix + ID  +'_Fk_IK', attributeType = 'enum', enumName = 'FK:IK' , keyable = True, hidden = False )
                    
       
        blndColours.blendColour(fkJnts[0], ikJnts[0], baseJnts[0],'rotate', settingsGrp + '.' + prefix + ID  +'_Fk_IK')
        blndColours.blendColour(fkJnts[1], ikJnts[1], baseJnts[1],'rotate', settingsGrp + '.' + prefix + ID  +'_Fk_IK')
        
        mc.poleVectorConstraint(polVec, armIkHandle[0])
        
        #Create Fk Controls
        fkCon =[]
        for i in fkJnts:
            ctrl = controlGen.generateCircle(prefix + i + "point" , i, True, [1,0,0] )
            fkCon.append(ctrl)
        assetColourer.colourer(fkCon, assetCol)
        
        #Create Ik Controls
        pvControl= controlGen.generateSphere(prefix +'Arm_Pv_Anim', polVec, False)
        assetColourer.colourer([pvControl], assetCol)
        mc.parent(polVec, pvControl)
        TEMPIK = controlGen.generateCircle(prefix +'handIk_Anim', baseJnts[2], False,[1,0,0])
        assetColourer.colourer([TEMPIK], assetCol)
        ikCon = [TEMPIK, pvControl]
        
        #Temp Ik Control
        mc.parent(armIkHandle[0], TEMPIK)
        
        #Grouping
        baseGrp = mc.group(baseJnts[0], name = prefix + 'baseJnt_grp')
        fkGrp = mc.group(fkJnts[0], name =  prefix + 'fkJnt_grp')
        ikGrp = mc.group(ikJnts[0], name = prefix + 'ikJnt_grp')
        self.armOri = mc.group(empty=True,name =  prefix + 'ArmOri_grp')
        self.armGrp = mc.group(empty = True,name = prefix +'Arm_grp')
        mc.delete(mc.parentConstraint(baseJnts[0], self.armGrp))
        mc.delete(mc.parentConstraint(baseJnts[0], self.armOri))
        mc.parent(baseGrp,fkGrp,ikGrp,self.armOri)
        mc.parent(self.armOri,self.armGrp)
        self.ikAnimGrp = mc.group(empty = True, name = prefix + 'Arm_ik_grp')
        mc.delete(mc.parentConstraint(baseJnts[0], self.ikAnimGrp))
        self.ikOffesetgrp = mc.group(empty = True, name = prefix +'ikhand_offset_grp')
        mc.delete(mc.parentConstraint(self.ikOffesetgrp, self.ikAnimGrp))
        mc.parent(self.ikOffesetgrp, pvControl, self.ikAnimGrp)
        mc.parent(TEMPIK,self.ikOffesetgrp)
        mc.makeIdentity(TEMPIK, apply =  True)
        mc.makeIdentity(pvControl, apply = True)
        
        #Clean Up Non Joint
        attrLocker.lockCommon(TEMPIK,[], [], ['X','Y','Z'], False, True)
        attrLocker.lockCommon(pvControl,[], [], ['X','Y','Z'], False, True)
        attrLocker.lockCommon(baseGrp,['X','Y','Z'], ['X','Y','Z'], ['X','Y','Z'], True, True)
        attrLocker.lockCommon(fkGrp,['X','Y','Z'], ['X','Y','Z'], ['X','Y','Z'], True, True)
        attrLocker.lockCommon(ikGrp,['X','Y','Z'], ['X','Y','Z'], ['X','Y','Z'], True, True)
        mc.setAttr(armIkHandle[0] + '.visibility',0)
        mc.setAttr(polVec + '.visibility',0)
        attrLocker.lockCommon(polVec,['X','Y','Z'], ['X','Y','Z'], ['X','Y','Z'], True, True)
        attrLocker.lockCommon(self.armOri,['X','Y','Z'], ['X','Y'], ['X','Y','Z'], True, True)
        
        
        
        #Clean Up Joints
        for i in fkCon:
            mc.setAttr(i +'.drawStyle', 2)
            attrLocker.lockCommon(i,['X','Y','Z'], [], ['X','Y','Z'], True, True)

        #for i in baseJnts:
            #mc.setAttr(i +'.drawStyle', 2)
            
        for i in ikJnts:
            mc.setAttr(i +'.drawStyle', 2)  
            
        
        #Create Vis Control
        mc.select(visGrp)
        mc.addAttr( shortName=prefix +ID + '_ArmVis', longName=prefix + ID + '_ArmVis', attributeType = 'enum', enumName = 'FK:IK:Both:None' , keyable = True, hidden = False )
        
        #Set Visibility Keys Left Legs
        for i in fkCon:
            setDvrKey.setDvrK(visGrp +  '.' + prefix + ID + '_ArmVis', i + 'Shape.visibility', 0, 1)
            setDvrKey.setDvrK(visGrp +  '.' + prefix + ID + '_ArmVis', i + 'Shape.visibility', 1, 0)
            setDvrKey.setDvrK(visGrp +  '.' + prefix + ID + '_ArmVis', i + 'Shape.visibility', 2, 1)
            setDvrKey.setDvrK(visGrp +  '.' + prefix + ID +'_ArmVis', i + 'Shape.visibility', 3, 0)
        
        for i in ikCon:
            setDvrKey.setDvrK(visGrp +  '.' + prefix + ID + '_ArmVis', i + '.visibility', 0, 0)
            setDvrKey.setDvrK(visGrp +  '.' + prefix + ID + '_ArmVis', i + '.visibility', 1, 1)
            setDvrKey.setDvrK(visGrp +  '.' + prefix + ID + '_ArmVis', i + '.visibility', 2, 1)
            setDvrKey.setDvrK(visGrp +  '.' + prefix + ID + '_ArmVis', i + '.visibility', 3, 0)
            attrLocker.lockCommon(i,[],[],[],True,True)
        
        
        #Define Controls
        
        objDefine.definer('characterName', fkCon, characterName)
        objDefine.definer('controlArea', fkCon, prefix + "arm")
        objDefine.definer('controlType', fkCon, "FK")
        
        objDefine.definer('characterName', ikCon , characterName)
        objDefine.definer('controlArea', ikCon , prefix + "arm")
        objDefine.definer('controlType', ikCon , "IK")
        
        #Define Bind Bones
        objDefine.definer('characterName', baseJnts[:-1] , characterName)
        objDefine.definer('bodyArea', baseJnts[:-1] , prefix + "leg")
        objDefine.definer('BoneType',baseJnts[:-1],'Bind')
        
        #Define Ik Bones
        objDefine.definer('characterName', ikJnts , characterName)
        objDefine.definer('bodyArea', ikJnts , prefix + "leg")
        objDefine.definer('BoneType',ikJnts,'IK')
        
        #Define Root and Connector Nodes
        objDefine.definer("Connection", [self.armGrp], "root")
        objDefine.definer("Connection", [self.ikAnimGrp], "rig")
        
                 
        
         

