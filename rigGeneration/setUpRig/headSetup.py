import maya.cmds as mc
from ranglerig2.rigTools import controlGen
from ranglerig2.rigTools import assetColourer

class SetUpHead:
    
    def __init__(self, *args):
        #Create Joints get translates
        
        headTopJnt = mc.joint(name = 'C_headUp', position =[0,12,0])
        mc.select(clear = True)
        
        headLoJnt = mc.joint(name = 'C_headLo', position =[0,10,0])
        mc.select(clear = True)
        
        
        
        
        jntList = [headTopJnt,headLoJnt]
        
        #Create Nurbs controls
        ctrlList = []
        for i in jntList:
            con = controlGen.generateSphere(i + '_setUp_ctl', i, False )
            assetColourer.colourer([con], 22)
            mc.addAttr(con, longName = "Control_Type", dataType = 'string' )
            mc.setAttr(con+".Control_Type", "setup", type = 'string', keyable = False, lock = True, channelBox = False)
            ctrlList.append(con)
            mc.delete(i)
            
        print ctrlList
        
        #Create link up curves
        
        upHeadCurve = mc.curve( name = 'C_headTop_cur_setUp_0', degree = 2, point = [( 0, 12, 0),(0, 11, 0), (0, 10, 0)])
        
        
        
        curveList = [upHeadCurve]
        loneclst = []
        
        #Generate clusters
        count = 0
        for i in curveList:
            
            assetColourer.colourer([i], 22)
            
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
        
            
        ctrlGrp = mc.group(ctrlList[1],ctrlList[0], name = 'ctrlGrp')
        curGrp = mc.group(curveList, name = 'curveGrp')
        print loneclst
        floatClstGrp = mc.group(loneclst, name = 'clsGrp')
        utilGrp = mc.group(curGrp, floatClstGrp, name = 'utilGrp')
        mc.setAttr(utilGrp + ".inheritsTransform",0)
        
        self.moduleGrp = mc.group(ctrlGrp,utilGrp, name = 'C_head_setUp_module_0')
        mc.xform(self.moduleGrp, rotatePivot = [0,10,0], scalePivot = [0,10,0])

        #Add Module Definition
        mc.addAttr(self.moduleGrp, longName = "Module_Type", dataType = 'string' )
        mc.setAttr(self.moduleGrp+".Module_Type", "setup", type = 'string', keyable = False, lock = True, channelBox = False)

        mc.addAttr(self.moduleGrp, longName = "Body_Part", dataType = 'string' )
        mc.setAttr(self.moduleGrp+".Body_Part", "Head",type = 'string', keyable = False, lock = True, channelBox = False)



                
        
            
        
                
            