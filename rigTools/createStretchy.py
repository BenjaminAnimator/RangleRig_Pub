"""
Module for creating fk/ik stretchyness
"""
import maya.cmds as mc

def stretchyIK(Joints, iKSplineCurve,descript):
    
    """
    Creates Stretchy IK
    @param Joints: List, List of the joints to apply stretch to
    @param iKSplineCurve: String, the name of the curve used to calculate stretch
    @param descript: String, define name of nodes
    """


    curveInfo = mc.arclen(iKSplineCurve, constructionHistory = True)
    curveInfo = mc.rename('curveInfo1', descript+'_Curve_info')
    curveBase = mc.getAttr(curveInfo + '.arcLength')
    
    node_M_D = mc.shadingNode('multiplyDivide' ,name = descript + '_str_multDiv', asUtility = True)
    mc.connectAttr(curveInfo + '.arcLength', node_M_D + '.input1X', force = True)
    mc.setAttr(node_M_D + '.operation', 2)
    mc.setAttr(node_M_D + '.input2X', curveBase)
    
    for i in Joints:
        mc.connectAttr(node_M_D + '.outputX', str(i) + '.scaleX' )
    mc.select(clear = True)
            

def stretchyFK(joint, control):
    
    subJnt = mc.listRelatives(joint, children = True)
    jntVal = mc.getAttr(subJnt[0] + '.translateX')
    stretchCtrl= mc.addAttr(control ,shortName = 'stretchy',longName = 'stretchy', attributeType = 'float', keyable = True, hidden = False )
    addNode = mc.shadingNode('plusMinusAverage', asUtility = True, name = control +'_str_addSub')
    mc.setAttr( addNode + '.input1D[0]', jntVal)
    mc.connectAttr(control + '.stretchy', addNode +'.input1D[1]', force = True)
    mc.connectAttr(addNode + '.output1D', subJnt[0] +'.translateX', force = True)
    mc.select(clear = True)
    
    
def skinningFKIKstretch(topJoint,endJoint):
    topTrans = mc.xform(topJoint,query = True, translation = True, worldSpace = True)
    endTrans =  mc.xform(endJoint,query = True, translation = True, worldSpace = True)
    
    ikCurve = mc.curve(degree =1, point = [topTrans,endTrans])
