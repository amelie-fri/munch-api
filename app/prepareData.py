# script used to move the files from the different directories to the N directory
import shutil
import os

# function now available for any kind of folder in the directory
source_folder = os.path.join("_data", "N")
destination_folder = source_folder


def moveXmlFilesInFolder(_folder):
    # for all the files in the different folders (located via the folderpaths)
    filesMoved = 0
    for _file in os.listdir(_folder):
        # if the file has the extension ".xml"
        if os.path.splitext(_file)[1] == ".xml":
            # a path to the file is created (combination folderpath and filename)
            _path = os.path.join(_folder, _file)
            # try to move the file from the source (_path) to the destination folder
            try:
                shutil.move(_path, destination_folder)
                filesMoved += 1
                # print(f"Moved {_path} to {destination_folder} ")
            except:
                print(f"Did not manage to move file: {_path}")
    print(f"Moved: {filesMoved} files")


# looping through all items in N, in order to find all folders and
# to provide the full path to these folders - the folderpath :)
for item in os.listdir(source_folder):
    # creates full path, out of path to N and item names (filenames/ foldernames)
    fullpath = os.path.join(source_folder, item)
    # check if the fullpath leads to a folder
    if os.path.isdir(fullpath):
        # if it does, the fullpath is a folderpath, which will be passed to the function
        folderpath = fullpath
        print(f"Moving content from: {folderpath}")
        moveXmlFilesInFolder(folderpath)
