import numpy
import url_parse
import re
import json
from collections import defaultdict

def built_model(page_text_list):
  model = defaultdict(lambda: 0)
  for url, text in page_text_list.items():
    for word in re.findall('\w+', text.lower()):
      model[word] += 1

  with open('models/model.json', 'w') as f:
    json.dump(model, f, indent=4)
