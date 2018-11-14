
class Globals:
    log_filename = "mDownloader.log"


class Conf_ini:
    conf = None
    conf_filename = "mDownloader.ini"

    class Keys:
        general = "General"
        loggingLevel = "loggingLevel"
        rss = "RSS"
        lastUpdateTime = "lastUpdateTime"
        checkInterval = "checkInterval"


class Wish_json:
    wishJsonMgr = None
    wanted_filename = "wanted.json"

    class Keys:
        movies = "Movies"
        name = "name"
