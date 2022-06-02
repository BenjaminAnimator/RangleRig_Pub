import maya.cmds as mc
from ranglerig2.rigTools import controlGen
from ranglerig2.rigTools import assetColourer



class SetUpSpines:
    
    def __init__(self, *args):
        #Create Joints get translates
        
        spineTopJnt = mc.joint(name = 'C_spineUp', position =[0,10,0])
        mc.select(clear = True)
        
        spineLoJnt = mc.joint(name = 'C_spineLo', position =[0,6,0])
        mc.select(clear = True)
        
        
        
        
        jntList = [spineTopJnt,spineLoJnt]
        
        #Create Nurbs controls
        ctrlList = []
        for i in jntList:
            con = controlGen.generateSphere(i + '_setUp_ctl', i, False )
            mc.addAttr(con, longName = "Control_Type", dataType = 'string' )
            mc.setAttr(con+".Control_Type", "setup", type = 'string', keyable = False, lock = True, channelBox = False)
            assetColourer.colourer([con], 22)
            ctrlList.append(con)
            mc.delete(i)
            
        print ctrlList
        
        #mc.parent(ctrlList[0],ctrlList[1])
        #Create link up curves
        
        upSpineCurve = mc.curve( name = 'C_spineTop_cur_setUp_0', degree = 2, point = [( 0, 10, 0),(0, 8, 0), (0, 6, 0)])
        
        
        
        curveList = [upSpineCurve]
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
        
        self.moduleGrp = mc.group(ctrlGrp,utilGrp, name = 'C_spine_setUp_module_0')
        mc.xform(self.moduleGrp, rotatePivot = [0,6,0], scalePivot = [0,6,0])

        #Define Self Variables
        self.upControl = ctrlList[0]
        self.loControl = ctrlList[1]

        #Add Module Definition
        mc.addAttr(self.moduleGrp, longName = "Module_Type", dataType = 'string' )
        mc.setAttr(self.moduleGrp+".Module_Type", "setup", type = 'string', keyable = False, lock = True, channelBox = False)

        mc.addAttr(self.moduleGrp, longName = "Body_Part", dataType = 'string' )
        mc.setAttr(self.moduleGrp+".Body_Part", "spine",type = 'string', keyable = False, lock = True, channelBox = False)
    
            
        
                
            