from DiCompare import DicomCompare
import sys

dc = DicomCompare()
dc.compareFiles(sys.argv[1], sys.argv[2])

for tagList in dc.getAllComparisons():
    tagListString = tagList.buildTagListRecursive()
    lastItem = tagList.getLastItem()
    print("%s | %s | \"%s\" | \"%s\"" % (tagListString, lastItem.errorMessage, lastItem.sourceVal, lastItem.targetVal))