import urllib.parse
from threading import Event, Thread


def encodeUrl(url):
    # this func encode HEB to be able to usr as url
    url = list(urllib.parse.urlsplit(url))
    url[2] = urllib.parse.quote(url[2])
    url = urllib.parse.urlunsplit(url)
    return url


# def call_repeatedly(interval, func, *args):
#     stopped = Event()
#     def loop():
#         while not stopped.wait(interval): # the first call is in `interval` secs
#             func(*args)
#     Thread(target=loop).start()
#     return stopped.set
