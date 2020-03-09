import pydicom

class DicomCompare():
    def __init__(self):
        self.__diffTags = list()
    
    def compareFiles(self, filePathSource, filePathTarget):
        headerSource = pydicom.dcmread(filePathSource)
        headerTarget = pydicom.dcmread(filePathTarget)
        return self.compareHeaders(headerSource, headerTarget)
    
    def compareHeaders(self, headerSource, headerTarget):
        self.__compareHeaderRecursive(headerSource, headerTarget)
        return self.__diffTags
    
    def __compareHeaderRecursive(self, headerSource, headerTarget, levelListString = "", levelZero=True):
        for item in headerSource:
            itemTarget = headerTarget[item.tag]

            if levelZero:
                levelListStringNew = str(item.tag)
            else:
                levelListStringNew = levelListString + " | " + str(item.tag)
            
            if item.VR != "SQ":
                # print(levelListStringNew)
                ## Check value and VR
                if item.value!=itemTarget.value | item.VR!=itemTarget.VR | item.VM!=itemTarget.VM:
                    self.__diffTags.append(levelListStringNew)
            
            if item.VR=="SQ":
                for i, subSet in enumerate(item.value):
                    levelListStringNewIndex = levelListStringNew + " | " + str(i) + ":"
                    self.__compareHeaderRecursive(subSet, itemTarget[i], levelListStringNewIndex, levelZero=False)