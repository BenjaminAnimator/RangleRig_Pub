import maya.cmds as mc
from ranglerig2.rigTools import controlGen
from ranglerig2.rigTools import assetColourer


class SetUpArms:
    
    def __init__(self,prefix = "R", *args ):

        
        if prefix == "L":
            assetColour = 13
            xValue = -1

        elif prefix == "R":
            assetColour = 6
            xValue = 1

        #Check Instance Number
        instance = 0
        for i in range(0,100):
            if mc.objExists(prefix +'_arm_setUp_module_' + str(instance)):
                print "Object Exists"
                instance +=1
            else:
                print "Object Doesn't Exist"
                print instance
                break

        else:
            mc.error("Invalid Prefix Please Use R or L.")
        #Create Joints get translates
        
        baseClavJnt = mc.joint(name = prefix + '_clavBase', position =[xValue*1,10,0])
        mc.select(clear = True)
        
        endClavJnt = mc.joint(name = prefix + '_clavEnd', position =[xValue*2,10,0])
        mc.select(clear = True)
        
        armAJnt = mc.joint(name = prefix + '_armA', position =[xValue*6,10,0])
        mc.select(clear = True)
        
        armBJnt = mc.joint(name = prefix + '_armB', position =[xValue*10,10,0])
        mc.select(clear = True)
        
        
        jntList = [baseClavJnt, endClavJnt, armAJnt, armBJnt]
        
        #Create Nurbs controls
        ctrlList = []
        for i in jntList:
            con = controlGen.generateSphere(i + 'setUp_ctrl_' + str(instance), i, False )
            assetColourer.colourer([con], assetColour)
            mc.addAttr(con, longName = "Control_Type", dataType = 'string' )
            mc.setAttr(con+".Control_Type", "setup", type = 'string', keyable = False, lock = True, channelBox = False)
            ctrlList.append(con)
            mc.delete(i)
            
        
        #Create link up curves
        
        clavCurve = mc.curve( name = prefix + '_clav_cur_setUp_'+ str(instance), degree = 2, point = [( xValue*1, 10, 0),(xValue*1.5, 10, 0), (xValue*2, 10, 0)])
        
        upCurve = mc.curve(name = prefix + '_armUp_cur_setUp_'+ str(instance), degree = 2, point = [( xValue*2, 10, 0),(xValue*4, 10, 0), (xValue*6, 10, 0)])

        loCurve = mc.curve(name = prefix + '_armLo_cur_setUp_'+ str(instance), degree = 2, point = [(xValue* 6, 10, 0),(xValue*8, 10, 0), (xValue*10, 10, 0)])
            

        curveList = [clavCurve, upCurve, loCurve]
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
        
            
        self.ctrlGrp = mc.group(ctrlList, name = prefix +'_arm_self.ctrlGrp_' + str(instance))
        curGrp = mc.group(curveList, name = prefix +'_arm_curGrp_' + str(instance))
        print loneclst
        floatClstGrp = mc.group(loneclst, name = prefix +'_arm_floatClstGrp_' + str(instance))
        utilGrp = mc.group(curGrp, floatClstGrp, name = prefix +'_arm_utilGrp_' + str(instance))
        mc.setAttr(utilGrp + ".inheritsTransform",0)
        
        self.moduleGrp = mc.group(self.ctrlGrp,utilGrp, name = prefix + '_arm_setUp_module_'+ str(instance))
        mc.xform(self.moduleGrp, rotatePivot = [xValue*1,10,0], scalePivot = [xValue*1,10,0])
                
        #Add Module Definition
        mc.addAttr(self.moduleGrp, longName = "Module_Type", dataType = 'string' )
        mc.setAttr(self.moduleGrp+".Module_Type", "setUp", type = 'string', keyable = False, lock = True, channelBox = False)

        mc.addAttr(self.moduleGrp, longName = "Body_Part", dataType = 'string' )
        mc.setAttr(self.moduleGrp+".Body_Part", "arm",type = 'string', keyable = False, lock = True, channelBox = False)

        mc.addAttr(self.moduleGrp, longName = "Side", dataType = 'string' )
        mc.setAttr(self.moduleGrp+".Side", prefix, type = 'string', keyable = False, lock = True, channelBox = False)

        mc.addAttr(self.moduleGrp, longName = "Instance", dataType = 'string' )
        mc.setAttr(self.moduleGrp+".Instance", str(instance),type = 'string', keyable = False, lock = True, channelBox = False)
