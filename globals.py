
class Globals:
    moridim_main = "https://www.moridim.biz"
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


class Wish_json:
    wishJsonMgr = None
    wanted_filename = "wanted.json"

    class Keys:
        type = "type"
        series = "series"
        movies = "movies"
        name = "name"
