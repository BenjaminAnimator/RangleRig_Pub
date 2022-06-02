"""
Module for Creating various shapes for Animation Controllers
"""
import maya.cmds as mc

#Generates Square Shape
def generateSquare(name, target, parentShape ):
    """
    Generates a Square Nurbs Curve
    
    @param name:String, Names the shape
    @param target:String, if True will move the curve to the target object
    @param parentShape:Boolean, if True will parent the shape node under target object
    """
    
    genSquare = mc.curve( degree = 1, point = [(-0.75, 0, -0.75), (-0.75, 0, 0.75), (0.75, 0, 0.75), (0.75, 0, -0.75), (-0.75, 0, -0.75)], knot =[0,1,2,3,4])
    genSquare = mc.rename(genSquare, name)
    target = target
    
    if target:
    
        if parentShape:
            mc.delete(mc.parentConstraint(target,genSquare))
            shape = mc.parent(genSquare + "Shape", target, shape = True, relative = True)
            mc.rename(shape, target + "Shape")
            mc.delete(genSquare)
            name = target
            genSquare = mc.rename(target, name )
            mc.makeIdentity(genSquare, apply = True)
            return genSquare
        

            
        else: 
            mc.delete(mc.pointConstraint(target, genSquare))
            mc.makeIdentity(genSquare, apply = True)
            return genSquare
               
    else:
        print "Done"
        





#Generates Circle Shape 
def generateCircle(name, target, parentShape, worldDir ):
    """
    Generates a Circle Nurbs Curve
    
    @param name:String, Names the shape
    @param target:String, if True will move the curve to the target object
    @param parentShape:Boolean, if True will parent the shape node under target object
    @param worldDir:List, presented as [1,0,0] for x , [0,1,0] for y and [0,0,1] for z
    """
    
    genCircle = mc.circle(constructionHistory = False, normal = worldDir)
    genCircle = mc.rename(genCircle, name)
    parentShape = parentShape
    target = target
    
    if target:
    
        if parentShape:
            mc.delete(mc.parentConstraint(target,genCircle))
            shape = mc.parent(genCircle + "Shape", target, shape = True, relative = True)
            mc.rename(shape, target + "Shape")
            mc.delete(genCircle)
            name = target
            genCircle = mc.rename(target, name )
            return genCircle
           
            
        else: 
            mc.delete(mc.parentConstraint(target, genCircle))
            mc.makeIdentity(genCircle, apply = True)
            return genCircle
               
    else:
        print "Done"
        
        
        
        
        
        
        
#Generates 4 Arrow cross
def generate4Arrow(name, target, parentShape,  xOrient ):
    """
    Generates a Four Arrowed Nurbs Curve
    
    @param name:String, Names the shape
    @param target:String, if True will move the curve to the target object
    @param parentShape:Boolean, if True will parent the shape node under target object
    @param xOrient: Boolean, If True will orient object to follow target's x axis
    """
    
    gen4Arrows = mc.curve(degree =  1, point = [(0, 0, -5), (-2, 0, -3), (-1, 0, -3), (-1, 0, -1), (-3, 0, -1), (-3, 0, -2), (-5, 0, 0), (-3, 0, 2), (-3, 0, 1), (-1, 0, 1), (-1, 0, 3),  (-2, 0, 3), (0, 0, 5), (2, 0, 3), (1, 0, 3), (1, 0, 1), (3, 0, 1), (3, 0, 2), (5, 0, 0),  (3, 0, -2), (3, 0, -1), (1, 0, -1), (1, 0, -3), (2, 0, -3), (0, 0, -5)], knot =[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24])
    gen4Arrows = mc.rename(gen4Arrows, name)
    parentShape = parentShape
    target = target
    
    
    if xOrient:
        mc.setAttr(gen4Arrows + '.rotateZ', 90)
        mc.makeIdentity(gen4Arrows, apply = True)
    else:
        None
    
    if target:
    
        if parentShape:
            mc.delete(mc.parentConstraint(target,gen4Arrows))
            shape = mc.parent(gen4Arrows + "Shape", target, shape = True, relative = True)
            mc.rename(shape, target + "Shape")
            mc.delete(gen4Arrows)
            name = target
            gen4Arrows = mc.rename(target, name )
            return gen4Arrows
           
            
        else: 
            mc.delete(mc.parentConstraint(target, gen4Arrows))
            mc.makeIdentity(gen4Arrows, apply = True)
            return gen4Arrows 
               
    else:
        print "Done"
        
    
        
        
    

#Generates Cube Shape
def generateCube(name, target, parentShape ):
    """
    Generates a Cube Nurbs Curve
    
    @param name:String, Names the shape
    @param target:String, if True will move the curve to the target object
    @param parentShape:Boolean, if True will parent the shape node under target object
    """
    
    genCube = mc.curve(degree =  1, point = [(-1, -1, -1), (-1, -1, 1), (-1, 1, 1), (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, 1, 1), (1, 1, 1), (1, 1, -1), (1, -1, -1), (1, -1, 1), (1, 1, 1), (-1, 1, 1), (-1, -1, 1), (1, -1, 1)], knot = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16 ])
    genCube = mc.rename(genCube, name)
    parentShape = parentShape
    target = target
    
    if target:
    
        if parentShape:
            mc.delete(mc.parentConstraint(target,genCube))
            shape = mc.parent(genCube + "Shape", target, shape = True, relative = True)
            mc.rename(shape, target + "Shape")
            mc.delete(genCube)
            name = target
            genCube = mc.rename(target, name )
            return genCube
            
           
            
        else: 
            mc.delete(mc.parentConstraint(target, genCube))
            mc.makeIdentity(genCube, apply = True)
            return genCube
               
    else:
        print "Done"


#Generates Pyramid Shape
def generateSphere(name, target, parentShape ):
    """
    Generates a Pyramid Nurbs Curve
    
    @param name:String, Names the shape
    @param target:String, if True will move the curve to the target object
    @param parentShape:Boolean, if True will parent the shape node under target object
    """
    


    circ_1= genCircle = mc.circle(constructionHistory = False, normal = [1,0,0])
    circ_2= genCircle = mc.circle(constructionHistory = False, normal = [0,1,0])
    circ_3= genCircle = mc.circle(constructionHistory = False, normal = [0,0,1])
    
    circ_1S= 'nurbsCircleShape1'
    circ_2S= 'nurbsCircleShape2'
    circ_3S= 'nurbsCircleShape3'
    genSphere = mc.group(circ_1, circ_2,circ_3)
    mc.parent( circ_1S, genSphere, shape = True, relative = True)
    mc.parent( circ_2S, genSphere, shape = True, relative = True)
    mc.parent( circ_3S, genSphere, shape = True, relative = True)
    
    mc.delete(circ_1)
    mc.delete(circ_2)
    mc.delete(circ_3)
    
    mc.rename(circ_1S, name+'Shape'+'1')
    mc.rename(circ_2S, name+'Shape'+'2')
    mc.rename(circ_3S, name+'Shape'+'3')
    
    genSphere = mc.rename(genSphere, name)
    parentShape = parentShape
    target = target
    
    if target:
    
        if parentShape:
            mc.delete(mc.parentConstraint(target,genSphere))
            shape = mc.parent(genSphere + "Shape", target, shape = True, relative = True)
            mc.rename(shape, target + "Shape")
            mc.delete(genSphere)
            name = target
            genSphere = mc.rename(target, name )
            return genSphere
            
           
            
        else: 
            mc.delete(mc.parentConstraint(target,genSphere))
            mc.makeIdentity(genSphere, apply = True)
            return genSphere
               
    else:
        print "Done"
    