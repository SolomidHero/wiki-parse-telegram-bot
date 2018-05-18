import matplotlib.pyplot as plt

def draw_words_freq(model):
  freqs = [i for i in model.values()]

  plt.title('Words with same frequency relation')
  plt.hist(freqs, bins=range(100), range=(0, 100), histtype='stepfilled', color='red')
  plt.ylabel('Number of words')
  plt.xlabel('Frequence')
  plt.grid(True)
  plt.savefig('./graphics/words_freq.png')
  plt.clf()

def draw_words_length(model):
  length = [len(key) for key in model.keys()]

  plt.hist(length, bins=range(15), histtype='stepfilled',color='blue')
  plt.ylabel('Number of words')
  plt.xlabel('Word length')
  plt.grid(True)
  plt.savefig('./graphics/words_length.png')
  plt.clf()
