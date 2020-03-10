from DiCompare import DicomCompare

dc = DicomCompare()
dc.compareFiles('source.dcm', 'target.dcm')

for tagList in dc.getAllComparisons():
    print(tagList.buildTagListRecursive())
    lastItem = tagList.getLastItem()
    print(lastItem.errorMessage)