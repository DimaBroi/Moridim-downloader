
class Globals:
    moridim_main = "https://www.moridim.co"
    moridim_rss = moridim_main + "/rss"
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
        download = "DOWNLOAD"
        downloadPath = "path"

class Wish_json:
    wishJsonMgr = None
    wanted_filename = "wanted.json"

    class Keys:
        type = "type"
        series = "series"
        movie = "movie"
        name = "name"
