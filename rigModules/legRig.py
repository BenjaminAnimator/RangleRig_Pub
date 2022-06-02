import maya.cmds as mc
from ranglerig2.rigTools  import blndColours
from ranglerig2.rigTools import selectHirearchy
from ranglerig2.rigTools import controlGen
from ranglerig2.rigTools  import assetColourer
from ranglerig2.rigTools  import attrLocker
from ranglerig2.rigTools  import objDefine
from ranglerig2.rigTools  import pvCalculator
from ranglerig2.rigTools  import setDvrKey

class legGen():
    
    def __init__ (self, setupControlGrp, characterName, rigGrp, settingsGrp, visGrp):
        
        setupCon =  selectHirearchy.jntHirearch(setupControlGrp, False, descendants = False, types = "transform")
        setupCon.reverse()

        jntList = []

        for i in setupCon:
            trans = mc.xform(i, q=True , ws = True , rp= True)
            jnt = mc.joint(position  = trans)
            jntList.append(jnt)

        

        print jntList
        
        
        ID  = "leg"
        
        '''
        rigJnts =  mc.duplicate(basejoint,  name = ID+'_01_Jnt', renameChildren = True)
        jnt1 = mc.rename(rigJnts[0], ID + '_01_Jnt')
        jnt2 = mc.rename(rigJnts[1], ID + '_02_Jnt')
        jnt3 = mc.rename(rigJnts[2], ID + '_03_Jnt')
        jnt4 = mc.rename(rigJnts[3], ID + '_04_Jnt')
        jnt5 = mc.rename(rigJnts[4], ID + '_05_Jnt')
       
        mc.setAttr(jnt1 + '.setUpJnt', lock= False)
        mc.setAttr(jnt1 + '.UniqueID', lock= False)
        mc.setAttr(jnt1 + '.characterName', lock= False)
        mc.deleteAttr(jnt1 + '.setUpJnt')
        mc.deleteAttr(jnt1 + '.characterName')
        mc.deleteAttr(jnt1 + '.UniqueID')
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
        
        

        #basic SetUp (Working as intended)
        
        baseJoints = selectHirearchy.jntHirearch(jntList[0],True, types = "joint")
        baseGrp = mc.group(jntList[0], name = prefix + 'LegBase_grp')
        print baseGrp
        fkGrp = mc.duplicate(baseGrp, name = prefix + 'Fk_joints', renameChildren = True)
        ikGrp = mc.duplicate(baseGrp, name = prefix +'Ik_joints', renameChildren = True)
        
        
        #Rename Base, IK and FK Joints
        legParts = ['Upleg', 'Loleg', 'Ankle', 'Ball', 'Toe']
        baseJnts = []
        ikJnts = []
        fkJnts = []
     

         
       
        count = 0
        for i in ikGrp[1:]:
            name = mc.rename(i, prefix + legParts[count] + '_ik_jnt' )
            ikJnts.append(name)
            count +=1
         
        count = 0   
        for i in fkGrp[1:]:
            name = mc.rename(i, prefix + legParts[count] + '_fk_Anim' )
            fkJnts.append(name)
            count +=1
            
        count = 0
        for i in baseJoints:
            name = mc.rename(i, prefix + legParts[count] + '_base_jnt' )
            baseJnts.append(name)
            count +=1
        
        leg_Ik_handle = mc.ikHandle( n= prefix + 'leg_ik_handle', sj=ikJnts[0], ee=ikJnts[2], solver = "ikRPsolver" )
        
        
        #Create Setting Attributes
        mc.select(settingsGrp)
        mc.addAttr( shortName= prefix + ID  +'_Fk_IK', longName=prefix + ID  +'_Fk_IK', attributeType = 'enum', enumName = 'FK:IK' , keyable = True, hidden = False )
        
       
        blndColours.blendColour(fkJnts[0], ikJnts[0], baseJnts[0],'rotate', settingsGrp +  '.' + prefix + ID  +'_Fk_IK')
        blndColours.blendColour(fkJnts[1], ikJnts[1], baseJnts[1],'rotate', settingsGrp +  '.' + prefix + ID  +'_Fk_IK')
        blndColours.blendColour(fkJnts[2], ikJnts[2], baseJnts[2],'rotate', settingsGrp +  '.' + prefix + ID  +'_Fk_IK')
        blndColours.blendColour(fkJnts[3], ikJnts[3], baseJnts[3],'rotate', settingsGrp +  '.' + prefix + ID  +'_Fk_IK')
        
        polVector = pvCalculator.pvCal(ikJnts[0], ikJnts[1], ikJnts[2], prefix + ID + 'leg_polvec')
        polVec = polVector.pvloc
        mc.poleVectorConstraint( polVec, leg_Ik_handle[0] )
        
        #Generate Controls for FK Rig (Working)
        fkCon = [] 
        for i in fkJnts[:4]:
            ctrl = controlGen.generateCircle(i + "point" , i, True, [1,0,0] )
            
            fkCon.append(ctrl)
            
        mc.setAttr(fkJnts[4] +'.drawStyle', 2)
        assetColourer.colourer(fkJnts, assetCol)
        mc.select(clear =True)
        

        #Create Ik Foot

        toe_ikhandle= mc.ikHandle(name = prefix + 'toe_ik_handle', startJoint = ikJnts[-2], endEffector = ikJnts[-1],solver = 'ikSCsolver')
        ball_ikhandle= mc.ikHandle(name = prefix + 'ball_ik_handle', startJoint = ikJnts[-3], endEffector = ikJnts[-2],solver = 'ikSCsolver')


        #IK Foot Set UP
        footAnim = controlGen.generateSquare(prefix + "foot_anim" ,ikJnts[2],False)
        assetColourer.colourer([footAnim], assetCol)
        mc.addAttr( shortName='heelRoll', longName='heelRoll', defaultValue= 0 , keyable = True, hidden = False )
        mc.addAttr( shortName='ballRoll', longName='ballRoll', defaultValue= 0 , keyable = True, hidden = False )
        mc.addAttr( shortName='toeRoll', longName='toeRoll', defaultValue= 0 , keyable = True, hidden = False )
        mc.addAttr( shortName='lean', longName='lean', defaultValue= 0 , keyable = True, hidden = False )
        mc.addAttr( shortName='side', longName='side', defaultValue= 0 , keyable = True, hidden = False )
        mc.addAttr( shortName='toeSpin', longName='toeSpin', defaultValue= 0 , keyable = True, hidden = False )
        mc.addAttr( shortName='toeWiggle', longName='toeWiggle', defaultValue= 0 , keyable = True, hidden = False )

        
        #Ik Anim Correction
        #mc.xform(footAnim,)
        
        #Foot Locators Query
        ankelPos =  mc.xform(ikJnts[-3], query =True, worldSpace = True, rotatePivot = True)
        ballPos =  mc.xform(ikJnts[-2], query =True, worldSpace = True, rotatePivot = True)
        toePos =  mc.xform(ikJnts[-1], query =True, worldSpace = True, rotatePivot = True)

        
        #Sets Up foot generate locators
        foot_loc = mc.spaceLocator(name = prefix + "foot_loc", position =[ankelPos[0], ankelPos[1] , ankelPos[2]])
        ball_loc = mc.spaceLocator(name = prefix +"ikBall_loc", position =[ballPos[0], ballPos[1] , ballPos[2]])
        toe_loc = mc.spaceLocator(name = prefix +"ikToe_loc", position =[toePos[0],toePos[1] , toePos[2]])
        mc.setAttr(toe_loc[0] +'.rotateOrder', 2)
        heel_loc = mc.spaceLocator(name = prefix +"ikHeel_loc", position =[ankelPos[0], 0 , ankelPos[2]])
        
        if prefix == 'L_': 
            inside_loc = mc.spaceLocator(name = prefix + "ikInside_loc", position =[ballPos[0] - 0.5, 0 , ballPos[2]])
            outside_loc = mc.spaceLocator(name = prefix + "ikOutside_loc", position =[ballPos[0] + 0.5, ballPos[1] , ballPos[2]])
            
        elif prefix == 'R_':
            inside_loc = mc.spaceLocator(name = prefix + "ikInside_loc", position =[ballPos[0] + 0.5, 0 , ballPos[2]])
            outside_loc = mc.spaceLocator(name = prefix + "ikOutside_loc", position =[ballPos[0] - 0.5, ballPos[1] , ballPos[2]])
            
        else:
            inside_loc = mc.spaceLocator(name = prefix + "ikInside_loc", position =[ballPos[0] - 0.5, 0 , ballPos[2]])
            outside_loc = mc.spaceLocator(name = prefix + "ikOutside_loc", position =[ballPos[0] + 0.5, ballPos[1] , ballPos[2]])
        
        toe_Wiggle_loc =  mc.spaceLocator(name = prefix + "ikWiggleToe_loc", position =[ballPos[0],ballPos[1] , ballPos[2]])
        
        #Clean Up locators
        feet_loc = [ball_loc, inside_loc, outside_loc, heel_loc, toe_loc, toe_Wiggle_loc,foot_loc]
        
        for i in feet_loc:
            mc.xform(i, centerPivots = True)
        
        #Parent Locators
        mc.parent(heel_loc, footAnim)
        mc.parent(outside_loc, toe_loc)
        mc.parent(inside_loc ,outside_loc)
        mc.parent(toe_loc, heel_loc)
        mc.parent(ball_loc, inside_loc)
        mc.parent(foot_loc, ball_loc)
        mc.parent(toe_Wiggle_loc, inside_loc)
        mc.parent(toe_ikhandle[0] , toe_Wiggle_loc)
        mc.parent(ball_ikhandle[0], inside_loc)
        mc.parent(leg_Ik_handle[0],foot_loc  )

        #Create Foot Anim Connections
        mc.connectAttr(footAnim +'.heelRoll', heel_loc[0] + '.rotateX')
        mc.connectAttr(footAnim +'.ballRoll', ball_loc[0] + '.rotateX')
        mc.connectAttr(footAnim +'.toeRoll', toe_loc[0] + '.rotateX')
        mc.connectAttr(footAnim +'.lean', toe_loc[0] + '.rotateZ')
        mc.connectAttr(footAnim +'.toeSpin', toe_loc[0] + '.rotateY')
        mc.connectAttr(footAnim +'.toeWiggle', toe_Wiggle_loc[0] + '.rotateX')
        
        if prefix == 'L_': 
            mc.expression(name = prefix +'footLean_expr', string ='''
            $side = %s.side;
            \n%s.rotateZ = min($side, 0);
            \n%s.rotateZ =  max(0,$side);
            ''' %(footAnim, outside_loc[0], inside_loc[0]))
            
        elif prefix == 'R_':
            mc.expression(name = prefix +'footLean_expr', string ='''
            $side = -%s.side;
            \n%s.rotateZ = min($side, 0);
            \n%s.rotateZ =  max(0,$side);
            ''' %(footAnim, inside_loc[0], outside_loc[0]))
        else:
            print 'None'

        
        #Create PV Control
        pvAnim = controlGen.generateSphere( prefix +'ik_PVLeg_anim', polVec, False)
        assetColourer.colourer([pvAnim] , assetCol)
        mc.parent(polVec,pvAnim)
        
        ikCon = [footAnim , pvAnim]
        
        #Clean Up Ik Locators
        print feet_loc

        for i in feet_loc:
            mc.setAttr( i[0] + '.visibility' , 0 )
            attrLocker.lockCommon(i[0], ['X','Y','Z'], ['X','Y','Z'], ['X','Y','Z'], True, True)

        mc.setAttr( polVec + '.visibility' , 0 )
        attrLocker.lockCommon(polVec, ['X','Y','Z'], ['X','Y','Z'], ['X','Y','Z'], True, True)
        
        #Clean Up IK Controls
        attrLocker.lockCommon(footAnim, [], [], ['X','Y','Z'], False, True)
        attrLocker.lockCommon(pvAnim, [], ['X','Y','Z'], ['X','Y','Z'], False, True)

        #Group Up
        self.legGrp= mc.group(baseGrp,fkGrp[0], ikGrp[0], name = prefix + 'Leg_grp')
        self.ikLegAnimGrp = mc.group(footAnim, pvAnim, name = prefix + 'Leg_ik_grp')
        
       #Clean Up (Non Joint)
        
        attrLocker.lockCommon(baseGrp, ['X','Y','Z'], ['X','Y','Z'], ['X','Y','Z'], True, True)
        attrLocker.lockCommon(ikGrp[0], ['X','Y','Z'], ['X','Y','Z'], ['X','Y','Z'], True, True)
        attrLocker.lockCommon(fkGrp[0], ['X','Y','Z'], ['X','Y','Z'], ['X','Y','Z'], True, True)
        
        #Clean Up (Joints)
        for i in baseJnts:
            #smc.setAttr(i +'.drawStyle', 2)
            attrLocker.lockCommon(i,['X','Y','Z'], ['X','Y','Z'], ['X','Y','Z'], True, True)
            
        for i in ikJnts:
            mc.setAttr(i +'.drawStyle', 2)
            
        for i in fkJnts:
            mc.setAttr(i +'.drawStyle', 2)
            attrLocker.lockCommon(i,['X','Y','Z'], [], ['X','Y','Z'], True, True)
             
       
        
        
        
        #Define Ik Controls for visibility setting

        #Define Controls
        
        objDefine.definer('characterName', fkJnts[:5], characterName)
        objDefine.definer('controlArea', fkJnts[:5], prefix + "leg")
        objDefine.definer('controlType', fkJnts[:5], "FK")
        
        objDefine.definer('characterName', ikCon , characterName)
        objDefine.definer('controlArea', ikCon , prefix + "leg")
        objDefine.definer('controlType', ikCon , "IK")
        
        #Define Bind Bones
        objDefine.definer('characterName', baseJnts[:-1] , characterName)
        objDefine.definer('bodyArea', baseJnts[:-1] , prefix + "leg")
        objDefine.definer('BoneType',baseJnts[:-1],'Bind')
        
        #Define Ik Bones
        objDefine.definer('characterName', ikJnts , characterName)
        objDefine.definer('bodyArea', ikJnts , prefix + "leg")
        objDefine.definer('BoneType',ikJnts,'IK')
        
        #Define Root Node
        objDefine.definer("Connection", [self.legGrp], "root")
        objDefine.definer("Connection", [self.ikLegAnimGrp], "rig")
        

        
        #Create Vis Control
        mc.select(visGrp)
        mc.addAttr( shortName=prefix + '_LegVis', longName= prefix + '_LegVis', attributeType = 'enum', enumName = 'FK:IK:Both:None' , keyable = True, hidden = False )
        
        #Set Visibility Keys Left Legs
        for i in fkCon:
            setDvrKey.setDvrK(visGrp +  '.' + prefix + '_LegVis', i + 'Shape.visibility', 0, 1)
            setDvrKey.setDvrK(visGrp +  '.' + prefix + '_LegVis', i + 'Shape.visibility', 1, 0)
            setDvrKey.setDvrK(visGrp +  '.' + prefix + '_LegVis', i + 'Shape.visibility', 2, 1)
            setDvrKey.setDvrK(visGrp +  '.' + prefix + '_LegVis', i + 'Shape.visibility', 3, 0)
        
        for i in ikCon:
            setDvrKey.setDvrK(visGrp +  '.' + prefix + '_LegVis', i + '.visibility', 0, 0)
            setDvrKey.setDvrK(visGrp +  '.' + prefix + '_LegVis', i + '.visibility', 1, 1)
            setDvrKey.setDvrK(visGrp +  '.' + prefix + '_LegVis', i + '.visibility', 2, 1)
            setDvrKey.setDvrK(visGrp +  '.' + prefix + '_LegVis', i + '.visibility', 3, 0)
            attrLocker.lockCommon(i,[],[],[],True,True)

        mc.select(clear = True)



        
        
            
            
                        
        

    
        

