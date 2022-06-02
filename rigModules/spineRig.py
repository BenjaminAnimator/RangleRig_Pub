"""
Module For creating character spine
"""
import maya.cmds as mc

from ranglerig2.rigTools import createStretchy
from ranglerig2.rigTools import jntSegmenter
from ranglerig2.rigTools import assetColourer
from ranglerig2.rigTools import controlGen
from ranglerig2.rigTools import attrLocker
from ranglerig2.rigTools import objDefine
from ranglerig2.rigTools import setDvrKey
from ranglerig2.rigTools import offsetCreator
#from RangleRig.toolkit import selectHirearchy


class spineGen(): 
    
    
    def __init__(self, basejoint, topjoint, ikSegments, fkSegments,characterName, rigGrp, visGrp):
        
        #Gets Spine's Unique ID
        ID  = "spine"
        
        #Gets xforms from setup joints

        print "WTFFF"
        print basejoint
        print topjoint
        bjTrans = mc.xform(basejoint, q=True , ws = True , rp= True)
        tjTrans = mc.xform(topjoint, q=True , ws = True , rp= True)

        print bjTrans
        print tjTrans
        


        #Segments adds X amount joints between a  parent joint and it's child joints
        noJoints = ikSegments
        rigJnts =  mc.duplicate(basejoint,  name = ID+'_01_Jnt', renameChildren = True)
        jnt1 = mc.joint(position  = bjTrans, name = ID + '_01_Jnt')
        jnt2 = mc.joint (position  = tjTrans, name = ID + '_02_Jnt')

        mc.joint(jnt1 ,edit = True, orientJoint =  'xyz', secondaryAxisOrient = 'ydown', children = True,  zeroScaleOrient = True)
        
       
        '''
        mc.Attr(jnt1 + '.setUpJnt', lock= False)
        mc.setAttr(jnt1 + '.UniqueID', lock= False)
        mc.setAttr(jnt1 + '.characterName', lock= False)
        mc.deleteAttr(jnt1 + '.setUpJnt')
        mc.deleteAttr(jnt1 + '.characterName')
        mc.deleteAttr(jnt1 + '.UniqueID')
		''' 
        ikBack = jntSegmenter.jointSegment(jnt1, noJoints  , 'ik'+ID, axis = 'x')
        
        
        #Creates curve Skinning joints
        self.hipJnt = mc.duplicate(ikBack[ikSegments], parentOnly = True, name = 'hip_joint')
        print "Test"
        self.chestJnt = mc.duplicate(ikBack[0], parentOnly = True, name = 'chest_joint')
        mc.parent(self.chestJnt, world = True)
        
        #Creates Ik Spline 
        spineIK = mc.ikHandle(startJoint = ikBack[ikSegments], endEffector = ikBack[0],
                               solver = 'ikSplineSolver', createCurve = True,
                                name  = ID +'_spline_ikhandle', numSpans = 3,
                                simplifyCurve = True)
        
        backCurve = mc.rename(spineIK[2], ID +'_ik_curve')
        mc.rename(spineIK[1], 'spine_ik_effector')
        
        
        #Skins backCurve to self.hipJnt and self.chestJnt
        mc.skinCluster(self.hipJnt, self.chestJnt, backCurve,
                        bindMethod = 0, maximumInfluences = 2,
                        obeyMaxInfluences = True,
                        dropoffRate = 4.0 )
        
        #Creates Stretch
        createStretchy.stretchyIK(ikBack,backCurve, ID)
        
        #Presever Volume
        node_Sqrt = mc.shadingNode('multiplyDivide' ,name = ID +'_sqrt_multDiv', asUtility = True)
        mc.setAttr(node_Sqrt + '.operation', 3)
        mc.setAttr(node_Sqrt + '.input2X', 0)
        mc.connectAttr( ID + '_str_multDiv.outputX', node_Sqrt + '.input1X', force = True)
        
        print rigGrp + 'THIS ONE'
        
        node_worldDiv = mc.shadingNode('multiplyDivide' ,name = ID + '_worlDiv_multDiv', asUtility = True)
        mc.setAttr(node_worldDiv + '.operation', 2)
        mc.connectAttr(node_Sqrt +'.outputX', node_worldDiv + '.input2X', force = True)
        mc.connectAttr(rigGrp +'.globalScale', node_worldDiv + '.input1X', force = True)
        
        for i in ikBack:
            mc.connectAttr(node_worldDiv +'.outputX', i + '.scaleY', force = True)
            mc.connectAttr(node_worldDiv +'.outputX', i + '.scaleZ', force = True)
                    
        #Turns off curve Inherit transform.
        mc.setAttr( backCurve  + ".inheritsTransform", 0)
         
        #Enable Twisting
        mc.setAttr(spineIK[0] + '.dTwistControlEnable', 1)
        mc.setAttr(spineIK[0] + '.dWorldUpType', 4 )
        mc.connectAttr(self.hipJnt[0] +'.worldMatrix[0]', spineIK[0] + '.dWorldUpMatrix', force = True )
        mc.connectAttr(self.chestJnt[0] +'.worldMatrix[0]', spineIK[0] + '.dWorldUpMatrixEnd', force = True )
        mc.setAttr(spineIK[0] + '.dWorldUpVectorY', 0)
        mc.setAttr(spineIK[0] + '.dWorldUpVectorEndY', 0)
        mc.setAttr(spineIK[0] + '.dWorldUpVectorZ', -1)
        mc.setAttr(spineIK[0] + '.dWorldUpVectorEndZ', -1)
        mc.setAttr(spineIK[0] + '.dWorldUpAxis', 4)
        mc.setAttr(spineIK[0] + '.dForwardAxis', 0)
        
        #Create FK chain
        fkHips = mc.duplicate(self.hipJnt[0], name = 'hips_fk_joint')[0]
        fkChest = mc.duplicate(self.chestJnt[0], name = 'chest_fk_joint')[0]
        mc.parent(fkChest,fkHips)
        
        #Segments
        noJoints = fkSegments
        fkBack = jntSegmenter.jointSegment(fkHips, noJoints  , 'fk'+ ID, axis = 'x')
        
        print fkBack   
        
        
        
        fkBack.reverse()
        for singleJoint in fkBack:
            mc.joint(singleJoint, edit =True, orientJoint = 'none', zeroScaleOrient = True )
            
        fkStart= fkBack.pop(0)
        fkEnd = fkBack.pop(-1)       
                
        
        
        #Creates Controls
        self.ctrlChest = controlGen.generateCube(ID + 'Chest_anim', self.chestJnt, False )
        self.ctrlHip = controlGen.generate4Arrow(ID + 'Hip_anim', self.hipJnt, False, True)

        chestOff = offsetCreator.createOffset(self.ctrlChest, 4)
        hipOff = offsetCreator.createOffset(self.ctrlHip, 4)
        

        counter = 1
        fkBackCtrl = []
        
        for i in fkBack:
            mc.setAttr(i +'.drawStyle', 2)
            rename = mc.rename(i, 'Back%s_Fk_anim' %counter)
            ctrl = controlGen.generateCircle('holder', rename, True, [0,1,0])
            #offsetCreator.createOffset(ctrl, 1)
            counter += 1
            fkBackCtrl.append(ctrl)
        
        
        
        #Colors joints
        assetColourer.colourer([self.ctrlChest, self.ctrlHip], 22)
        assetColourer.colourer(fkBackCtrl, 22)
        
        
        #Lock Attributes
        attrLocker.lockCommon(self.ctrlChest,[],[],["X","Y","Z"],True,True)
        attrLocker.lockCommon(self.ctrlHip, [],[],["X","Y","Z"],True,True)
        
        for i in fkBackCtrl:
            attrLocker.lockCommon(i ,["X","Y","Z"],[],["X","Y","Z"],True,True)
        
        
        
        #Set up
        mc.parent(self.hipJnt,hipOff)
        mc.parent(fkStart , self.ctrlHip)
        mc.parent(self.ctrlChest, fkEnd)
        mc.makeIdentity(self.ctrlChest, apply = True, rotate = True, translate =True)
        mc.parent(self.chestJnt,chestOff)
        DntGrp =  mc.group(spineIK[0], backCurve,ikBack[ikSegments], name = 'DoNotTouch_' + ID + '_grp')
        mc.setAttr( DntGrp+'.inheritsTransform', 0)
        self.allSpineGrp = mc.group(self.ctrlHip , DntGrp, name = ID + 'Spine_grp' )
        
        #Lock Groups
        attrLocker.lockCommon( DntGrp,["X","Y","Z"],["X","Y","Z"],["X","Y","Z"],True,True)
        attrLocker.lockCommon( self.allSpineGrp,["X","Y","Z"],["X","Y","Z"],["X","Y","Z"],True,True)
        
        #Define Controls
        self.spineCon = [self.ctrlChest]
        self.spineCon.extend(fkBackCtrl)
        print self.spineCon
        
        objDefine.definer('characterName', [self.ctrlHip], characterName)
        objDefine.definer('characterName', [self.ctrlChest], characterName)
        objDefine.definer('characterName', fkBackCtrl, characterName)
        objDefine.definer("controlArea", [self.ctrlHip], ID)
        objDefine.definer("controlArea", [self.ctrlChest], ID)
        objDefine.definer("controlArea", fkBackCtrl, ID)              
        objDefine.definer("controlType", [self.ctrlHip], 'master')
        objDefine.definer("controlType", [self.ctrlChest], 'IK')
        objDefine.definer("controlType", fkBackCtrl, "FK")
        #objDefine.definer("Connection", [self.allSpineGrp], "root")
        #objDefine.definer("Connection", self.chestJnt, chestSetup )
        #objDefine.definer("Connection", self.hipJnt, basejoint)
        
        #Create spine visibilty Attribute
        mc.select(visGrp)
        mc.addAttr( shortName=ID + '_SpineVis', longName=ID + '_SpineVis', attributeType = 'enum', enumName = 'FK:IK:Both:None' , keyable = True, hidden = False )
        
        #Set Visibility Keys Spine
        setDvrKey.setDvrK(visGrp + '.' + ID + '_SpineVis', self.spineCon[0] + 'Shape.visibility', 0, 0)
        setDvrKey.setDvrK(visGrp + '.' + ID + '_SpineVis', self.spineCon[0] + 'Shape.visibility', 1, 1)
        setDvrKey.setDvrK(visGrp + '.' + ID + '_SpineVis', self.spineCon[0] + 'Shape.visibility', 2, 1)
        setDvrKey.setDvrK(visGrp + '.' + ID + '_SpineVis', self.spineCon[0] + 'Shape.visibility', 3, 0)
        
        setDvrKey.setDvrK(visGrp + '.' + ID + '_SpineVis', self.spineCon[1] + 'Shape.visibility', 0, 1)
        setDvrKey.setDvrK(visGrp + '.' + ID + '_SpineVis', self.spineCon[1] + 'Shape.visibility', 1, 0)
        setDvrKey.setDvrK(visGrp + '.' + ID + '_SpineVis', self.spineCon[1] + 'Shape.visibility', 2, 1)
        setDvrKey.setDvrK(visGrp + '.' + ID + '_SpineVis', self.spineCon[1] + 'Shape.visibility', 3, 0)
        
        setDvrKey.setDvrK(visGrp + '.' + ID + '_SpineVis', self.spineCon[2] + 'Shape.visibility', 0, 1)
        setDvrKey.setDvrK(visGrp + '.' + ID + '_SpineVis', self.spineCon[2] + 'Shape.visibility', 1, 0)
        setDvrKey.setDvrK(visGrp + '.' + ID + '_SpineVis', self.spineCon[2] + 'Shape.visibility', 2, 1)
        setDvrKey.setDvrK(visGrp + '.' + ID + '_SpineVis', self.spineCon[2] + 'Shape.visibility', 3, 0)
        
        #Clean Up(Lock Down)
        attrLocker.lockCommon(self.hipJnt[0],["X","Y","Z"],["X","Y","Z"],["X","Y","Z"],True,True)
        attrLocker.lockCommon(fkStart, ["X","Y","Z"],["X","Y","Z"],["X","Y","Z"],True,True)
        attrLocker.lockCommon(fkEnd, ["X","Y","Z"],["X","Y","Z"],["X","Y","Z"],True,True)
        attrLocker.lockCommon(self.chestJnt[0],["X","Y","Z"],["X","Y","Z"],["X","Y","Z"],True,True)
        
        for i in ikBack:
            attrLocker.lockCommon(i,[],[],["X","Y","Z"],True,True)
            
            
        #Set Visibility (Non Driven Non Joint)
        #mc.setAttr(spineIK[0]+'.visibility', 0)
        mc.setAttr(backCurve+'.visibility', 0)
        

        #Set joint Visibility (Draw Style)
        #for i in ikBack:
            #mc.setAttr(i +'.drawStyle', 2)
        
        for i in fkBackCtrl:
            mc.setAttr(i +'.drawStyle', 2)
        
        mc.setAttr(fkStart +'.drawStyle', 2)  
        mc.setAttr(fkEnd +'.drawStyle', 2) 
        mc.setAttr(self.hipJnt[0] +'.drawStyle', 2)
        mc.setAttr(self.chestJnt[0] +'.drawStyle', 2)

        mc.select(clear = True)
    
        
            
        
        '''
        #Make skinning joints
        spineSkinJnt = []
        
        for i in ikBack:
            spineSkinJnt.append(i)




        spineSkinJnt.pop(0)
        spineSkinJnt.pop(-1)
        spineSkinJnt.append(self.chestJnt[0])
        spineSkinJnt.append(self.hipJnt[0])
        print spineSkinJnt
        
        objDefine.definer("BoneType" ,spineSkinJnt, "Bind")
        '''
        
        

            
