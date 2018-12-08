import json
import os
from json import JSONDecodeError
import logging


from globals import Wish_json


class WishJsonMgr:
    logger = logging.getLogger(__name__)
    wishes = None

    def __init__(self):
        try:
            if not os.path.isfile(Wish_json.wanted_filename):
                with open(Wish_json.wanted_filename, 'w') as jsonFile:
                    json.dump({}, jsonFile)

            with open(Wish_json.wanted_filename) as jsonFile:
                self.wishes = json.load(jsonFile)

        except JSONDecodeError as jSONDecodeError:
            self.logger.error("JSONDecodeError was raised for " + Wish_json.wanted_filename + " with msg \"" + str(jSONDecodeError)+"\"")
            raise Exception(Wish_json.wanted_filename + " decoding failed")

    def print_json(self):
        print(json.dumps(self.wishes, indent=2, sort_keys=True))

    def getKeys(self):
        return self.wishes.keys()

    def getType(self, name):
            return self.wishes[name]["type"]

    def getSeason(self, name):
            return self.wishes[name]["season"]

    def getEpisode(self, name):
            return self.wishes[name]["episode"]

    def setNextSeason(self, name):
        self.wishes[name]["season"] += 1
        self.wishes[name]["episode"] = 1

    def setNextEpisode(self, name):
        self.wishes[name]["episode"] += 1

    def removeMovieByName(self, name):
        del self.wishes[name]

    def getWantedQuality(self, name):
        return self.wishes[name]["quality"]

    def writeToFile(self):
        with open(Wish_json.wanted_filename, 'w') as jsonFile:
            json.dump(self.wishes, jsonFile)


if __name__ == '__main__':
    wishJson = WishJsonMgr()
    wishJson.print_json()
    print(wishJson.getKeys())
    wishJson.removeMovieByName(wishJson.getKeys()[0])
    wishJson.print_json()