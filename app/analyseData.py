# script used to analyse how successful the approaches to extracting data are

from dataManager import parentManager
from TeiParser import Family
import os
import pprint

analysisFile = "analyse.txt"

# write to analysis file - analyse.txt
def writeToFile(_text, mode="a", pretty=None):
    # Append to file
    with open(analysisFile, mode, encoding="utf-8") as _file:
        if pretty:
            pprint.pprint(_text, _file)
        else:
            print(_text, file=_file)


# path to "_data/N" folder
path_N = os.path.join("_data", "N")
# create the parent manager
pm_N = parentManager(path_N)

# Initialise file
writeToFile("Data Analysis", mode="w")
writeToFile("File: {}".format(analysisFile))
writeToFile("Data: {}".format(path_N))

# Check all .xml files in directory
allFiles = []
for item in os.listdir(path_N):
    if os.path.splitext(item)[-1].lower() == ".xml":
        allFiles.append(item)

# Initialise
foundFiles = []
types = {}
dates = {"when": {}, "from": {}, "to": {}}
whenCount = 0
# For each parent
for i, parentFile in enumerate(pm_N.parents):
    # Print process to command line
    percent = str(int((100 * (i + 1) / len(pm_N.parents))))
    print(f"\r Progress:  {percent}% ", end="\r")

    # Initialize parent object
    parent = Family(os.path.join(path_N, parentFile))
    # append parent filename to foundFiles
    foundFiles.append(parent.filename)
    # if the parent has a type
    if parent.data.type:
        # if the type already exists in types
        if parent.data.type in types:
            # increment type
            types[parent.data.type] += 1
        else:
            # start counting type
            types[parent.data.type] = 1
    # for each child
    for child in parent.children:
        # append childname to foundfiles
        foundFiles.append(child.filename)
        # if child has date dict
        if child.date:
            # for each key in dates
            for item in dates:
                # if date key exists in child date
                if item in child.date:
                    # for each date in dates key
                    for date in child.date[item]:
                        # pick only the year number
                        if "-" in date:
                            date = date.split("-")[0]
                        # count when
                        if item == "when":
                            whenCount += 1
                        # increment date
                        if date in dates[item]:
                            dates[item][date] += 1
                        # start counting date
                        else:
                            dates[item][date] = 1
# Add the count to the dict
dates["whenCount"] = whenCount

# Build/Calculate Info
info = {
    "files": len(allFiles),
    "found": len(foundFiles),
    "notFound": len(allFiles) - len(foundFiles),
    "parents": len(pm_N.parents),
    "children": len(foundFiles) - len(pm_N.parents),
}
# Write Types
writeToFile("\nTYPES")
writeToFile(types, pretty=True)
# Write Dates
writeToFile("\nDATES")
writeToFile(dates, pretty=True)
# Write Info
writeToFile("\nINFO")
writeToFile(info, pretty=True)

# Which files are not found?
notFound = list(set(allFiles) - set(foundFiles))
# Write Output
writeToFile("\nFiles that are not found")
for i, item in enumerate(notFound):
    writeToFile("\t" + item)
