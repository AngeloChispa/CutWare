class Contours:
    
    def __init__(self, contour, hierarchy):
        self.contour = contour;
        self.hierarchy = hierarchy;
        self.sons = [];
        
    def setPosition(self, list):
        #print(list[self.hierarchy[0]].getHierarchy()[1])
        self.position = list[self.hierarchy[0]].getHierarchy()[1]
    
    def getPosition(self):
        return self.position    
        
    def setSons(self, list):
        for i in list:
            if i.getHierarchy()[3] == self.position:
                self.sons.append(i)
    
    def getSons(self):
        return self.sons;    
        
    def getContour(self):
        return self.contour;
    
    def getHierarchy(self):
        return self.hierarchy;