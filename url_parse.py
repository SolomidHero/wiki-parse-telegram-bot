import urllib.request
from bs4 import BeautifulSoup
from collections import defaultdict

class url_parse:
  def __init__(self):
    self.url_list = defaultdict(lambda: 0) # key: url - value: depth
    self.checked_list = defaultdict(lambda: False)
    self.set_depth()

  def set_link(self, link):
    self._link = link
    self.url_list[link] = 1
    self.find_urls()
    print("DONE")

  def set_depth(self, depth=1):
    self._depth = int(depth) + 1

  def reset(self):
    self.set_depth()
    self.url_list.clear()
    self.checked_list.clear()

  def find_urls(self):
    approved = True
    while(approved):
      approved = False
      for url, depth in self.url_list.items():
        if not self.checked_list[url] and self.url_list[url] < self._depth:
          approved = True
          self.update_urls(url)
          break

  def update_urls(self, link):
    page = urllib.request.urlopen(link)
    soup = BeautifulSoup(page, "html.parser")
    self.checked_list[link] = True
    print(link)

    for site in soup.find_all('a'):
      url = site.get('href')
      if url != None and url[:5] == '/wiki' and self.checked_list[url] == False:
        self.url_list["https://en.wikipedia.org" + url] = self.url_list[link] + 1

  def get_pages_text(self):
    self.page_text_list = defaultdict(lambda: "")
    for url in self.url_list:
      if not self.checked_list[url]:
        continue
      page_text = ""
      soup = BeautifulSoup(urllib.request.urlopen(url), "html.parser")
      for p in soup.find_all('p'):
        page_text += p.text
      self.page_text_list[url] = page_text
    return self.page_text_list
