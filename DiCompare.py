import pydicom

class LinkedTagList():
    def __init__(self):
        self.nextTagList = None
        self.tag = None
        self.itemIndex = None
        self.errorMessage = None
        self.sourceVal = None
        self.targetVal = None
    
    def buildTagListRecursive(self, tagList=None, stringList=""):
        stringListNew = stringList
        if tagList is None:
            tagList = self

        if tagList.tag is not None:
            stringListNew += str(tagList.tag)
        
        if tagList.itemIndex is not None:
            stringListNew += "[" + str(tagList.itemIndex) + "] "
        
        if tagList.nextTagList is not None:
            stringListNew = self.buildTagListRecursive(tagList.nextTagList, stringListNew)
        
        return stringListNew
    
    def getLastItem(self, curItem):
        if curItem.nextTagList is not None:
            return self.getLastItem(curItem.nextTagList)
        else:
            return curItem

    def listContainsError(self):
        return self.getLastItem(self).errorMessage is not None


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
    
    def __compareHeaderRecursive(self, headerSource, headerTarget, tagListItem = None, levelZero=True):
        for item in headerSource:
            itemTarget = headerTarget[item.tag]

            if levelZero:
                tagListItem = LinkedTagList()
                self.__diffTags.append(tagListItem)
            tagListItem.tag = item.tag
            
            if item.VR != "SQ":
                # print(levelListStringNew)
                ## Check value and VR
                if item.value!=itemTarget.value:
                    tagListItem.error = "Value mismatch"
                    tagListItem.sourceVal = item.value
                    tagListItem.targetVal = itemTarget.value
            
            if item.VR=="SQ":
                for i, subSet in enumerate(item.value):
                    tagListItem.itemIndex = i
                    newItem = LinkedTagList()
                    tagListItem.nextTagList = newItem
                    self.__compareHeaderRecursive(subSet, itemTarget[i], newItem, levelZero=False)
    
    def getAllComparisons(self):
        return self.__diffTags
    
    def subsetErrorOnly(self):
        newDiffTags = list()

        for item in self.__diffTags:
            if item.listContainsError():
                newDiffTags.append(item)
        
        self.__diffTags = newDiffTags