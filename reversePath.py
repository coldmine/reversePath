import maya.cmds as mc

class reversePath():
    
    def __init__(self):
        ################################# UI
        self.win = 'reversePath'
        self.firstColumnWidth = 100
        self.secondColumnWidth = 80
        #################################
                        
        ################################# For bake simulation & copyKey
        self.startTime = mc.playbackOptions(q = True, min = True)
        self.endTime = mc.playbackOptions(q = True, max = True)
        #################################
        
        ################################# Camera and Locator/Object info
        self.selCam_Name = 'Select Camera'
        self.dupCam_Name = ''  
        self.selObject_Name = 'Select Object'
        #################################
        
        ################################# ETC        
        self.pointConstraintName = ''
        self.orientConstraintName = ''                
        self.reversePathGrp = 'reversePathGrp'        
        #################################
                        
        self.display()        
        
    def display(self):
        
        if mc.window(self.win,exists = True):
            mc.deleteUI(self.win)
        
        mc.window(self.win, sizeable = False, resizeToFitChildren = True)
        
        mc.rowColumnLayout(nc = 1)
        
        mc.separator(height = 15, style = 'out') #############################
        
        mc.text(label = 'Reverse Path')
        
        mc.separator(height = 15, style = 'out') #############################
        
        mc.rowColumnLayout(nc = 2, columnWidth = [(1,self.firstColumnWidth),(2,self.secondColumnWidth)])        
        mc.text('selCam_Name', label = self.selCam_Name)
        mc.button(label = 'Get Camera', command = self.get_selCam_button)
        mc.setParent('..')
        
        mc.separator(height = 15, style = 'out') #############################

        mc.rowColumnLayout(nc = 2, columnWidth = [(1,self.firstColumnWidth),(2,self.secondColumnWidth)])        
        mc.text('selObject_Name', label = self.selObject_Name)
        mc.button(label = 'Get Object', command = self.get_selObject_button)
        mc.setParent('..')        
        
        mc.separator(height = 15, style = 'out') #############################  
        
        mc.button(label = 'Reverse Path', height = 40, command = self.reversePath_button)
             
        mc.separator(height = 15, style = 'out') #############################  
                   
        mc.showWindow(self.win)

        
    def get_selCam_button(self,a):
        
        selCam_Name = mc.ls(selection = True)[0]
        self.selCam_Name = selCam_Name
        
        mc.text('selCam_Name',edit = True, label = self.selCam_Name)
        return

    def get_selObject_button(self,a):
        
        selObject_Name = mc.ls(selection = True)[0]
        self.selObject_Name = selObject_Name
        
        mc.text('selObject_Name',edit = True, label = self.selObject_Name)
        return
        
    def reversePath_button(self,a):
        
        self.dupCam_Name = mc.duplicate(self.selCam_Name) ### Duplicate Render Camera / Just for constraint uses...
        mc.duplicate(self.selObject_Name) ### Duplicate Object
        
        mc.group(self.selCam_Name, name = self.reversePathGrp) ### Group Render Cam
        
        mc.parent(self.reversePathGrp, self.selObject_Name) ### Parent reversePathGrp to Object
    
        self.pointConstraintName = mc.pointConstraint(self.dupCam_Name, self.selCam_Name, maintainOffset = False)     
        self.orientConstraintName = mc.orientConstraint(self.dupCam_Name, self.selCam_Name, maintainOffset = False)
        
        mc.bakeResults(self.selCam_Name, time = (self.startTime,self.endTime), at=['tx','ty','tz','rx','ry','rz'])
        mc.delete(self.pointConstraintName)
        mc.delete(self.orientConstraintName)
        
        mc.ungroup(self.reversePathGrp, world = True)
      
        mc.hide(self.selObject_Name)
        mc.hide(self.dupCam_Name)
        return
        
if __name__ == '__main__':
    reversePath().display()