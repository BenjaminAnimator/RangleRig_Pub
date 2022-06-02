import maya.cmds as mc
from ranglerig2.rigTools import controlGen
from ranglerig2.rigTools import assetColourer

class SetUpTail:
    
    def __init__(self, *args):

        #Create Joints get translates
        
        baseClavJnt = mc.joint(name = 'C_tailTop', position =[0,0,0])
        mc.select(clear = True)
        
        endClavJnt = mc.joint(name = 'C_tailMid1', position =[0,0,2])
        mc.select(clear = True)
        
        armAJnt = mc.joint(name = 'C_tailMid2', position =[0,0,4])
        mc.select(clear = True)
        
        armBJnt = mc.joint(name = 'C_tailEnd', position =[0,0,6])
        mc.select(clear = True)
        
        
        jntList = [baseJnt, mid1Jnt, mid2Jnt , endJnt]
        
        #Create Nurbs controls
        ctrlList = []
        for i in jntList:
            con = controlGen.generateSphere(i + 'setUp_ctl', i, False )
            assetColourer.colourer([con], 22)
            ctrlList.append(con)
            mc.delete(i)
            
        
        #Create link up curves
        
        upCurve = mc.curve( name = 'C_armUp_cur_setUp_0', degree = 2, point = [( 0, 6, 0),(0, 4.5, 0), (0, 3, 0)])
        
        loCurve = mc.curve(name = 'C_armLo_cur_setUp_0', degree = 2, point = [( 0, 3, 0),(0, 2, 0), (0, 1, 0)])
            
        
        curveList = [upCurve, loCurve]
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
            mc.setAttr(i + '.hiddenInOutliner', 1)
        
            
        ctrlGrp = mc.group(ctrlList, name = 'ctrlGrp')
        curGrp = mc.group(curveList)
        print loneclst
        floatClstGrp = mc.group(loneclst)
        utilGrp = mc.group(curGrp, floatClstGrp, name = 'utilGrp')
        
        moduleGrp = mc.group(ctrlGrp,utilGrp, name = 'C_arm_setUp_module_0')
                
