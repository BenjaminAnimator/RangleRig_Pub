"""
Script for mirroring the setup up rig pose
"""

import maya.cmds as mc

def setupMirroring(baseModule):
	print 'working'

	#Sanity Checks

	#Get Data
	query = mc.attributeQuery("Module_Type", node = baseModule,exists = True)

	
	if query == True:
		mType = mc.getAttr(baseModule+".Module_Type")
	else:
		mc.error("Selection is not a module group.")

	if mType != "setUp":
		mc.error("Selection is not a setup module group.")
	else:
		print "a"

	bpType = mc.getAttr(baseModule+".Body_Part")

	sType = mc.getAttr(baseModule+".Side")

	iType = mc.getAttr(baseModule+".Instance")



	#Get Mirrored Side
	if sType == "L":
		msType = "R"

	elif sType =="R":
		msType = "L"

	else:
		mc.error("This module is not mirrorable")


	#Get Module to be Mirrored
	mirroredModule = msType+"_"+ bpType+"_"+ mType+"_"+ "module"+"_"+ iType


	exists = mc.objExists(mirroredModule)

	if exists == True:
		print "Object is mirrorable"
	else:
		mc.error("There is no Mirrorable module")
	print "Done"

	#Filter Non control modules For Main Controls

	moduleComponents = mc.listRelatives(baseModule, type = "transform", allDescendents = True)
	print moduleComponents

	controlsA = []
	for x in moduleComponents:
		conQuery = mc.attributeQuery("Control_Type", node = x, exists = True)
		print x
		print conQuery

		if conQuery  == True:
			conVal = mc.getAttr(x + ".Control_Type")
			if conVal ==  'setup':
				controlsA.append(x)
			else:
				print "Not Setup Joint"

		else:
			print "Node has no Control_Type Attribute"

	print controlsA

	
	#Filter Non control modules For Mirrored Controls

	mirroredComponents = mc.listRelatives(mirroredModule, type = "transform", allDescendents = True)
	print mirroredComponents


	controlsB = []
	for x in mirroredComponents:
		conQuery = mc.attributeQuery("Control_Type", node = x, exists = True)
		print x
		print conQuery

		if conQuery  == True:
			conVal = mc.getAttr(x + ".Control_Type")
			if conVal ==  'setup':
				controlsB.append(x)
			else:
				print "Not Setup Joint"

		else:
			print "Node has no Control_Type Attribute"

	print controlsB
	

	#Mirror Pose

	for a,b in zip(controlsA,controlsB):
		locA = mc.spaceLocator()
		mc.delete(mc.parentConstraint(a, locA))

		aValues = mc.xform(locA, query = True, translation = True, worldSpace =True)
		print  aValues

		bValues = [-1*aValues[0], aValues[1], aValues[2] ]

		locB= mc.spaceLocator()
		mc.xform(locB, translation = bValues, worldSpace = True)
		mc.delete(mc.parentConstraint(locB,b))
		mc.delete(locA,locB)



