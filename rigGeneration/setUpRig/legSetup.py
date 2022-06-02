import maya.cmds as mc
from ranglerig2.rigTools import controlGen
from ranglerig2.rigTools import assetColourer

class SetUpLegs:
    
    def __init__(self,prefix = "R", *args ):

        #Set Prefix Attributes
        if prefix == "L":
            assetColour = 13
            xValue = -1

        elif prefix == "R":
            assetColour = 6
            xValue = 1

        else:
            mc.error("Invalid Prefix Please Use R or L.")

        #Check Instance Number
        instance = 0
        for i in range(0,100):
            if mc.objExists(prefix +'_leg_setUp_module_' + str(instance)):
                print "Object Exists"
                instance +=1
            else:
                print "Object Doesn't Exist"
                print instance
                break

        #Create Joints get translates

        upLegJnt = mc.joint(name = prefix +'_legUp', position =[xValue*1,6,0])
        upLegJntPos = mc.xform( upLegJnt , query = True , translation = True, worldSpace = True)
        mc.select(clear = True)
        
        loLegJnt = mc.joint(name = prefix + '_legLo', position =[xValue*1,3,0])
        lopLegJntPos = mc.xform( loLegJnt , query = True , translation  = True, worldSpace = True)
        mc.select(clear = True)
        
        ankleJnt = mc.joint(name = prefix +'_legAnkle', position =[xValue*1,1,0])
        loLegJntPos = mc.xform( ankleJnt , query = True , translation  = True, worldSpace = True)
        mc.select(clear = True)
        
        footAJnt = mc.joint(name = prefix +'_footA', position =[xValue*1,0,2])
        loLegJntPos = mc.xform( footAJnt , query = True , translation= True, worldSpace = True)
        mc.select(clear = True)
        
        footBJnt = mc.joint(name = prefix +'_footB', position =[xValue*1,0,3])
        loLegJntPos = mc.xform( footAJnt , query = True , translation  = True, worldSpace = True)
        mc.select(clear = True)
        
        jntList = [upLegJnt, loLegJnt, ankleJnt, footAJnt,footBJnt]
        
        #Create Nurbs controls
        ctrlList = []
        for i in jntList:
            con = controlGen.generateSphere(i + 'setUp_ctl_' + str(instance), i, False )
            assetColourer.colourer([con], assetColour)
            mc.addAttr(con, longName = "Control_Type", dataType = 'string' )
            mc.setAttr(con+".Control_Type", "setup", type = 'string', keyable = False, lock = True, channelBox = False)
            ctrlList.append(con)
            mc.delete(i)
            
        
        #Create link up curves
        
        upCurve = mc.curve( name = prefix +'_legUp_cur_setUp_' + str(instance), degree = 2, point = [( xValue*1, 6, 0),(xValue*1, 4.5, 0), (xValue*1, 3, 0)])
        
        loCurve = mc.curve(name = prefix +'_legLo_cur_setUp_' + str(instance), degree = 2, point = [( xValue*1, 3, 0),(xValue*1, 2, 0), (xValue*1, 1, 0)])
        
        ankleCurve = mc.curve(name = prefix +'_legAnkle_cur_setUp_' + str(instance), degree = 2, point = [( xValue*1, 1, 0),(xValue*1, 0.5, 1), (xValue*1, 0, 2)])
        
        footCurve = mc.curve(name = prefix +'_legFoot_cur_setUp_' + str(instance), degree = 2, point = [( xValue*1, 0, 2),(xValue*1, 0, 2.5), (xValue*1, 0, 3)])
        
        
        
        curveList = [upCurve, loCurve,ankleCurve,footCurve]
        loneclst = []
        
        #Generate clusters
        count = 0
        for i in curveList:
            
            assetColourer.colourer([i], assetColour)
            
            curveCVs = mc.ls(i + ".cv[0:]",fl=True)
            
            iteration = 0
            
            clstList = []
        
            for x, cv in enumerate(curveCVs):
                    
            
                clst = mc.cluster(cv, cv, name = i + "_clst_" + str(iteration) )
                mc.setAttr(clst[0] + "Handle.visibility", 0)
                
                clstList.append(clst)
                
                iteration =+ 1
                
            mc.parent(clstList[0],ctrlList[count])
            floatClst = str(clstList[1][1])
            print floatClst
            loneclst.append(floatClst)
        
            mc.parentConstraint(clstList[0], clstList[2],clstList[1], maintainOffset = True)
            count += 1
            mc.parent(clstList[2],ctrlList[count])
            
            mc.setAttr(i + '.overrideEnabled', 1)
            mc.setAttr(i + '.overrideDisplayType', 2)
        
        #Clean Up Outliner    
        self.ctrlGrp = mc.group(ctrlList, name = prefix +'_leg_self.ctrlGrp_' + str(instance))
        curGrp = mc.group(curveList, name = prefix +'_leg_curlGrp_' + str(instance))
        print loneclst
        floatClstGrp = mc.group(loneclst, name = prefix +'_leg_floatClstGrp_' + str(instance))
        utilGrp = mc.group(curGrp, floatClstGrp, name = prefix +'_leg_utilGrp_' + str(instance))
        mc.setAttr(utilGrp + ".inheritsTransform",0)
        
        self.moduleGrp = mc.group(self.ctrlGrp,utilGrp, name = prefix +'_leg_setUp_module_' + str(instance))
        
        #Set Module Pivot to base joint
        mc.xform(self.moduleGrp, rotatePivot = [xValue*1,6,0], scalePivot = [xValue*1,6,0])

        #Add Module Definition
        mc.addAttr(self.moduleGrp, longName = "Module_Type", dataType = 'string' )
        mc.setAttr(self.moduleGrp+".Module_Type", "setUp", type = 'string', keyable = False, lock = True, channelBox = False)

        mc.addAttr(self.moduleGrp, longName = "Body_Part", dataType = 'string' )
        mc.setAttr(self.moduleGrp+".Body_Part", "leg",type = 'string', keyable = False, lock = True, channelBox = False)

        mc.addAttr(self.moduleGrp, longName = "Side", dataType = 'string' )
        mc.setAttr(self.moduleGrp+".Side", prefix, type = 'string', keyable = False, lock = True, channelBox = False)

        mc.addAttr(self.moduleGrp, longName = "Instance", dataType = 'string' )
        mc.setAttr(self.moduleGrp+".Instance", str(instance),type = 'string', keyable = False, lock = True, channelBox = False)

    

        
    