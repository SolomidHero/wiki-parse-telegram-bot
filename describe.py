import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from collections import defaultdict
import models.cmd_description as cmd

def draw_words_freq(model):
  freqs = [i for i in model.values()]

  plt.title('Words with same frequency relation')
  plt.hist(freqs, bins=range(100), range=(0, 100), histtype='stepfilled', color='red')
  plt.ylabel('Number of words')
  plt.xlabel('Frequence')
  plt.grid(True)
  plt.savefig(cmd.WORDS_FREQ_IMG)
  plt.clf()

def draw_words_length(model):
  length = [len(key) for key in model.keys()]

  plt.hist(length, bins=range(15), histtype='stepfilled',color='blue')
  plt.ylabel('Number of words')
  plt.xlabel('Word length')
  plt.grid(True)
  plt.savefig(cmd.WORDS_LENGTH_IMG)
  plt.clf()

def draw_wordcloud(model):
  model = defaultdict(lambda: 0, model)
  for key in STOPWORDS:
    if model[key] > 0:
      model[key] = 0

  wordcloud = WordCloud(
    max_font_size=100,
    background_color=None,
    mode='RGBA',
    width=800,
    height=600,
    colormap=cmd.WORDCLOUD_COLOR
  ).generate_from_frequencies(model)
  plt.figure()
  plt.imshow(wordcloud, interpolation="mitchell")
  plt.axis("off")
  plt.savefig(cmd.WORDCLOUD_IMG)
  plt.clf()


def get_word_stat(model, key):
  print(key)
  model = defaultdict(lambda: 0, model)
  place = 1
  freq = model[key]
  for word, value in model.items():
    if value > freq:
      place += 1
  print(f"This word {key!r} is repeated in site for {freq} and got {place} for popularity")
  return f"This word {key!r} is repeated in site for {freq} and got {place} for popularity."