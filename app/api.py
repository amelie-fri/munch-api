from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from TeiParser import Family
from dataManager import parentManager
import os

# path to "_data/N" folder
path_N = os.path.join("_data", "N")
# create the parent manager
pm_N = parentManager(path_N)

# create the Flask application
app = Flask(__name__)
api = Api(app)

# returns array of parent filenames
class MunchParents(Resource):
    def get(self):
        return {"data": pm_N.parents}


# returns content of the parents
class MunchFamily(Resource):
    def get(self, _file):
        if _file in pm_N.parents:
            family = Family(os.path.join(path_N, _file))
            resp = {
                "title": family.data.title,
                "type_text": family.data.type,
                "date": {"when": [], "from": [], "to": []},
                "text": "",
            }
            _text = []
            for child in family.children:

                for item in child.date:
                    # item when, to, or from
                    if child.date[item]:
                        resp["date"][item].append(child.date[item])

                _text.append(child.text)
            # access text key in python dictionary
            # join items from list _text with new lines
            resp["text"] = "\n\n".join(_text)
            # print(resp["text"])
            return resp, 200
        else:
            # If file is not found
            return {"notFound": _file}, 404


api.add_resource(MunchParents, "/N")
api.add_resource(MunchFamily, "/N/<_file>")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
