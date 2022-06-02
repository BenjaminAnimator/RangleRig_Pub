import maya.cmds as mc
from ranglerig2.rigTools import controlGen
from ranglerig2.rigTools import assetColourer


def createOffset(mainControl, noOffsets):
    subList =  mc.listRelatives(mainControl, children = True, allDescendents = False)
    print subList
    del subList[0]
    print subList
    
    trueOffset = noOffsets -1
    if trueOffset == 0:
        count = ["A"]
        
    else:
        iteration = ["A","B", "C", 'D', 'E']
        count = iteration[0:trueOffset]
    print "NUMBER OF ITS:" + str(count)
    
    dictGrp = {}
    dictControl = {}
    
    
    for i in count:
        #create OffsetGrp
        groupName = mainControl.split('_')
        print groupName
        offGrp= mc.group(empty = True, name = groupName[0] + 'Offset' + i +'_grp')
        
        #ZeroGrp
        trans = mc.xform(mainControl, q=True , ws = True , rp= True)
        print trans
        mc.xform(offGrp, translation =  trans, ws = True)
        mc.makeIdentity(offGrp, apply = True , translate = True)
        
        #make Control
        control = controlGen.generateCircle(groupName[0] + 'Offset' + i +'_anim', offGrp, False,[0,1,0])
        assetColourer.colourer([control], 21) 
        mc.parent(control, offGrp)
        
        dictGrp.update({i:offGrp})
        dictControl.update({i:control})
        
    
    print "--DEBUG--"
    print dictGrp
    print dictControl
    
    if  len(dictGrp) > 1:
		print "Only 1"

		countControl = list(count)
		countGrp = list(count)
		countGrp.pop(0)
		countControl.pop(-1)

		print countControl
		print countGrp

		for x,y in zip(countControl,countGrp):
			print "--DEBUG--"
			print y,x
			mc.parent(dictGrp[y], dictControl[x])
			

		topCon = dictControl[count[-1]]
		 
    else:
        print 'Done'
        topCon = dictControl[(count[-1])]

    print "DEBUG"
    print dictGrp['A']
    print mainControl
    print subList
    print topCon

    lastCon  = dictControl[(count[-1])]
    

    
    mc.parent(dictGrp['A'], mainControl)
    for x in subList:
    	print x
        mc.parent(topCon,x)

    return lastCon

    
        
    
    
 