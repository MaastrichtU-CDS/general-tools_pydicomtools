from DiCompare import DicomCompare

dc = DicomCompare()
dc.compareFiles('source.dcm', 'target.dcm')

for tagList in dc.getAllComparisons():
    tagListString = tagList.buildTagListRecursive()
    lastItem = tagList.getLastItem()
    print("%s | %s | \"%s\" | \"%s\"" % (tagListString, lastItem.errorMessage, lastItem.sourceVal, lastItem.targetVal))