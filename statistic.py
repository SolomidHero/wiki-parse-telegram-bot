import numpy
import url_parse
import re
import json
import models.cmd_description as cmd_description
from collections import defaultdict

class statistic:
  def __init__(self):
    self.top_words_num = cmd_description.TOP_WORDS_NUMBER
    with open('models/model.json', 'r') as f:
      self.model = json.load(f)

    values = [i for i in self.model.values()]
    self.std_deviation = numpy.std(values)
    self.avg_value = numpy.mean(values)

  def built_model(self, page_text_list):
    self.model = defaultdict(lambda: 0)
    for url, text in page_text_list.items():
      for word in re.findall('\w+', text.lower()):
        self.model[word] += 1

    values = list()
    for value in self.model.values():
      values.append(value)

    self.std_deviation = numpy.std(values)
    self.avg_value = numpy.mean(values)

    with open('models/model.json', 'w') as f:
      json.dump(self.model, f, indent=4)

  def stop_words(self):
    stop_word = list()
    for key, value in self.model.items():
      if value < self.avg_value - 3 * self.std_deviation or\
          value > self.avg_value + 3 * self.std_deviation:
        stop_word.append(key)
    return stop_word

  def top_desc(self):
    top = dict()
    for key, value in self.model.items():
      if (value < self.avg_value + 3 * self.std_deviation and
          value > self.avg_value - 3 * self.std_deviation):
        if len(top) < self.top_words_num:
          top[key] = value
        else:
          max_key = iter(top.keys()).__next__()
          for k in top.keys():
            if top[k] > top[max_key]:
              max_key = k
          if top[max_key] > value:
            del top[max_key]
            top[key] = value
    return top

  def top_asc(self):
    top = dict()
    for key, value in self.model.items():
      if (value < self.avg_value + 3 * self.std_deviation and
          value > self.avg_value - 3 * self.std_deviation):
        if len(top) < self.top_words_num:
          top[key] = value
        else:
          min_key = iter(top.keys()).__next__()
          for k in top.keys():
            if top[k] < top[min_key]:
              min_key = k
          if top[min_key] < value:
            del top[min_key]
            top[key] = value
    return top