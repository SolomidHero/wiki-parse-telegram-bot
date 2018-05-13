import urllib
import urllib.request

class url_parse:
  def __init__(self, link):
    self._link = link
    file = urllib.request.urlopen(self._link)
    page = file.read().decode("utf-8")
    print(page)