import json
import os

from globals import Wish_json


class WishJsonMgr:

    wishes = None

    def __init__(self):
        if not os.path.isfile(Wish_json.wanted_filename):
            with open(Wish_json.wanted_filename, 'w') as jsonFile:
                json.dump({}, jsonFile)

        with open(Wish_json.wanted_filename) as f:
            self.wishes = json.load(f)

    def print_json(self):
        print(json.dumps(self.wishes, indent=2, sort_keys=True))

    def getKeys(self):
        return self.wishes.keys()

    def removeMovieByName(self, name):
        del self.wishes[name]


if __name__ == '__main__':
    wishJson = WishJsonMgr()
    wishJson.print_json()
    print(wishJson.getKeys())
    wishJson.removeMovieByName(wishJson.getKeys()[0])
    wishJson.print_json()