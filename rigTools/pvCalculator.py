'''
Calculates the correct pole vector location for ik chains using a Rotate Plane Solver
'''
import maya.api.OpenMaya as om
import maya.cmds as mc

class pvCal():
    def __init__(self,topJnt,midJnt,endJnt,name):
        topJntPos = mc.xform(topJnt, query = True, translation = True, worldSpace = True)
        midJntPos = mc.xform(midJnt, query = True, translation = True, worldSpace = True)
        endJntPos = mc.xform(endJnt, query = True,translation = True, worldSpace = True)
        
        startV = om.MVector(topJntPos[0] ,topJntPos[1],topJntPos[2])
        midV = om.MVector(midJntPos[0] ,midJntPos[1],midJntPos[2])
        endV = om.MVector(endJntPos[0] ,endJntPos[1],endJntPos[2])
        startEnd = endV - startV
        startMid = midV - startV
        dotP = startMid * startEnd
        proj = float(dotP) / float(startEnd.length())
        startEndN = startEnd.normal()
        projV = startEndN * proj
        arrowV = startMid - projV
        arrowV*= 0 
        finalV = arrowV + midV
        self.pvloc = mc.spaceLocator(name = name)[0]
        mc.xform(self.pvloc , ws =1 , t= (finalV.x , finalV.y ,finalV.z))