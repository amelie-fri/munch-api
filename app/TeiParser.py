from bs4 import BeautifulSoup
from dataManager import validateChild
import os
import re

# Might be important to have Brevutkast before brev...
knownTypes = ["Brevutkast", "Blandet", "Brev", "Notat", "Varia", "Bildeliste"]


def read_tei(tei_file):
    # is the path - filename really an existing file in the directory
    if not os.path.isfile(tei_file):
        raise RuntimeError("This is not a file {}".format(tei_file))
    # open file
    with open(tei_file, "r", encoding="utf-8") as tei:
        try:
            # create soup
            soup = BeautifulSoup(tei, "lxml")
        except:
            raise RuntimeError(
                "Cannot generate a soup from the input for file: {}".format(tei_file)
            )
        finally:
            return soup
    raise RuntimeError("Cannot generate a soup from the input")


# -------------------------------------------------------------
# parses files to extract specific parts of the data
# --------------------------------------------------------------
class soupFisher(object):
    def __init__(self, _file):
        self.filename = os.path.basename(_file)
        self.soup = read_tei(_file)
        self._children = []
        self._title = ""
        self._text = None
        self._date = {}
        self._type = ""

    # extracts child filenames from a parent file
    @property
    def children(self):
        if self._children:
            return self._children
        else:
            childArr = []
            # Look for children in the body
            # For every div in the body
            for element in self.soup.body.find_all("div"):
                # Get the value of the xml:id attribute, if the element has one
                # for every attribute, if the attribute is xml:id, store value of attribute in list
                value = [element.get(i).strip() for i in element.attrs if i == "xml:id"]
                if value:
                    # list always contains one item, append it to array for children fileames
                    childArr.append(value[0])
            # sometimes xml:id does not contain a child filename, instead it is in the xpointer
            if not self.soup.body.find_all("div"):
                for element in self.soup.body.find_all("include"):
                    value = [
                        element.get(i).strip() for i in element.attrs if i == "xpointer"
                    ]
                    if value:
                        childArr.append(value[0])
            self._children = childArr
            return self._children

    # extract title from a file
    @property
    def title(self):
        if not self._title:
            self._title = self.soup.title.getText()
        return self._title

    # extract text content from files
    @property
    def text(self):
        if not self._text:
            divs_text = []
            for div in self.soup.body.find_all("div"):
                # text might appear multiple times still, can be filtered with div.attrs
                if div:
                    div_text = div.get_text(separator=" ", strip=True)
                    divs_text.append(div_text)
            # turn list into a set - items are unique then (text does not occur twice anymore)
            # turn set back into a list
            plain_text = " ".join(list(set(divs_text)))
            self._text = plain_text
        return self._text

    # extract temporal information
    @property
    def date(self):
        if not self._date:
            _when = []
            _from = []
            _to = []
            # find the dateline tag
            for dateline in self.soup.body.find_all("dateline"):
                for element in dateline.find_all("date"):
                    _when = [
                        element.get(i).strip()
                        for i in element.attrs
                        if i.lower() == "when"
                    ]
                    _from = [
                        element.get(i).strip()
                        for i in element.attrs
                        if i.lower() == "from"
                    ]
                    _to = [
                        element.get(i).strip()
                        for i in element.attrs
                        if i.lower() == "to"
                    ]
            # Specifc cases
            for i, item in enumerate(_when):
                # double hyphen, where hyphen is added where some part of the date is not available
                # if a year number (4 digits long) is contained, only store that in the _when list
                # if no year number exists, store an empty string instead
                if "--" in item:
                    if len(item.split("--")[0]) == 4:
                        _when[i] = item.split("--")[0]
                    else:
                        _when[i] = ""
                # if the format of the date offers only one digit for the day - add a 0 before the digit
                if re.match(r"^\d{4}-\d{2}-\d{1}$", item):
                    _when[i] = (
                        item.split("-")[0]
                        + "-"
                        + item.split("-")[1]
                        + "-"
                        + "0"
                        + item.split("-")[2]
                    )
                # check if the order of yyyy-mm-dd exists
                # in case mm and dd are swapped, turn tehm around
                if re.match(r"^\d{4}-\d{2}-\d{2}$", item):
                    if int(item.split("-")[1]) > 12:
                        _when[i] = (
                            item.split("-")[0]
                            + "-"
                            + item.split("-")[2]
                            + "-"
                            + item.split("-")[1]
                        )
                # fix e.g. "1907-1908"
                # <date when="1907---/1908-"> for the first child
                # only kept 1907, lost 1908 --> regarded as fine :)
                if re.match(r"^\d{4}-\d{4}$", item):
                    # exchange the date with the first year
                    _when[i] = item.split("-")[0]
                    # append second year to list - (both years are still available)
                    _when.append(item.split("-")[1])

            # filters _when for e.g. empty strigns "", hence,
            # if no year is available an empty list is available
            _when = list(filter(None, _when))

            # the lists are stored as an object in the _date class variable
            self._date = {
                "when": _when,
                "from": _from,
                "to": _to,
            }

        return self._date

    # extract the text type
    @property
    def type(self):
        if not self._type:
            for knowType in knownTypes:
                # lower case - finding all types, also if the type is not spelled with a capital letter
                # if one of the known types can be found in the extracted title
                if knowType.lower() in self.title.lower():
                    # store the type, but witha cpitalised letter in the beginning
                    self._type = knowType.lower().capitalize()
                    break
            if not self._type:
                self._type = "Not Found"
        return self._type


# -------------------------------------------------------------
# finds children based on parents, validation of the files,
# combines parents with its children in one object
# -------------------------------------------------------------


class Family(object):
    def __init__(self, _file):
        self.filename = os.path.basename(_file)
        self.path = _file
        self.rootPath = os.path.dirname(self.path)
        if not self.rootPath:
            self.rootPath = "."
        self.data = soupFisher(self.path)
        self.file_extension = os.path.splitext(self.filename)[1]
        self._children = []

    @property
    def children(self):
        if not self._children:
            for child in self.data.children:
                # does the child really exist
                _child = validateChild(child, self.file_extension, self.rootPath)
                if _child:
                    self._children.append(soupFisher(_child))
                else:
                    print("Amelie Debug this, child not found!!!!")
                    print(child)

        return self._children
