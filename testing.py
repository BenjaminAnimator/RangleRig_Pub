import maya.cmds as mc
#import ranglerig2.UserInterfaces
import ranglerig2.rigGeneration.setUpRig
import ranglerig2.rigModules

def start():
	print "Welcome to Rangle Rig 2"
	
	#Create Setup
	spineSU = ranglerig2.rigGeneration.setUpRig.spineSetup.SetUpSpines()
	headSU = ranglerig2.rigGeneration.setUpRig.headSetup.SetUpHead()
	armSUR = ranglerig2.rigGeneration.setUpRig.armSetup.SetUpArms(prefix = 'R')
	legSUR = ranglerig2.rigGeneration.setUpRig.legSetup.SetUpLegs(prefix = 'R')
	armSUL = ranglerig2.rigGeneration.setUpRig.armSetup.SetUpArms(prefix = 'L')
	legSUL = ranglerig2.rigGeneration.setUpRig.legSetup.SetUpLegs(prefix = 'L')

	#Hide Setup
	setup = mc.group(spineSU.moduleGrp,armSUR.moduleGrp,armSUL.moduleGrp, legSUL.moduleGrp,legSUR.moduleGrp, headSU.moduleGrp, name = "setup_grp")
	mc.setAttr(setup + ".visibility",0)
	
	#Create Rig
	base = ranglerig2.rigModules.baseRig.baseGen("Test")
	spine = ranglerig2.rigModules.spineRig.spineGen(spineSU.loControl, spineSU.upControl, 5,3,"Test", base.rigGrp, base.visibilityGrp)
	legL =  ranglerig2.rigModules.legRig.legGen(legSUL.ctrlGrp, "Test", base.rigGrp, base.settingGrp , base.visibilityGrp )
	legR =  ranglerig2.rigModules.legRig.legGen(legSUR.ctrlGrp, "Test", base.rigGrp, base.settingGrp ,base.visibilityGrp )
	armR = ranglerig2.rigModules.armRig.armGen(armSUR.ctrlGrp, "Test", base.rigGrp, base.settingGrp , base.visibilityGrp )
	armL = ranglerig2.rigModules.armRig.armGen(armSUL.ctrlGrp, "Test", base.rigGrp, base.settingGrp , base.visibilityGrp )




start()

#ranglerig2.UserInterfaces.SetUpInterface.SetUpGUI()