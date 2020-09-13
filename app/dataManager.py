import os
import re


class parentManager:
    def __init__(self, path):
        self.path = path
        self._parents = []

    # Finds all parents
    @property
    def parents(self):
        if not self._parents:
            parentList = []
            for item in os.listdir(self.path):
                item_path = os.path.join(self.path, item)
                if os.path.isfile(item_path):
                    temp_name = os.path.splitext(item)[0]
                    temp_name = temp_name.split("MM_N")[1]
                    if not "-" in temp_name:
                        parentList.append(item)
            self._parents = parentList
        return self._parents


# Does the child file with the children filename from a parent
# really exist in the directory with the data?


def validateChild(child, extension, path):
    """The function recieves two arguments. child contains a filename from a parent file. 
    path contains the full path to the actual children file with that name in the directory.
    The function recieves a child filename, as is appears in parent files, and checks if
    a file with name does exist in the data directory. If it does, the child is vaild and
    the full path to the child file is returned. Otherwise the name of the child that could
    not be validated is returned.
    """
    # split the extension from the filename - some children are named "xxx.xml.xml"
    _child = os.path.splitext(child)[0]
    # combining filename and extension again
    _child = f"{_child}{extension}"
    # creating a hypothetical path, where to look for the child
    # where it should be located
    # combining the path with the child filename+extension
    # does automatically add the perfect slash
    _childPath = os.path.join(path, _child)
    # does that path to a child file really exist in the data directory?
    if os.path.exists(_childPath):
        return _childPath
    #
    # some children filenames are mentioned in a parent file contain
    # "No-" in their names, the respective files do not appear with "No-"
    # in the data directory
    if "No-" in child:
        _child = os.path.splitext(child)[0]
        _child = f"{_child}{extension}"
        # split child filename at hyphen, take "pure" filename
        _child = _child.split("No-", 1)[1]
        _childPath = os.path.join(path, _child)
        if os.path.exists(_childPath):
            return _childPath
    #
    # check if child string is in directory somehow, return path of
    # the string part found joined with path
    # (takes care of possible extra whietspace in filename in directory)
    for item in os.listdir(path):
        if os.path.splitext(_child)[0] in item:
            return os.path.join(path, item)

    # Whitespace occured in children filename from parent - whitespace removed
    _child = re.sub(r"\s+", "", _child)
    _childPath = os.path.join(path, _child)
    if os.path.exists(_childPath):
        return _childPath

    print(f"Hei! Didnt find this child!: {child}")
    return ""
