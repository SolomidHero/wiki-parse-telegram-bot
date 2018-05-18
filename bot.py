from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import CommandHandler
import matplotlib.pyplot as plt

from statistic import statistic
import describe
import models.cmd_description as cmd
import logging
from url_parse import url_parse

class parse_bot:
  def __init__(self):
    logging.basicConfig(
      format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
      level=logging.INFO
    )
    self.logger = logging.getLogger(__name__)
    _token = '557754452:AAFuMjFF2O80b7B8s7_5n_0ljMeGcYDeHYM'
    _request_kwargs = {
      'proxy_url': 'socks5://78.155.206.64:2016',
      'urllib3_proxy_kwargs': {
        'username': 'telegaproxy',
        'password': 'proxytelega',
      }
    }

    # self.updater = Updater(token=_token, request_kwargs=_request_kwargs)
    self.updater = Updater(token=_token)
    self.dispatcher = self.updater.dispatcher
    self.parser = url_parse()
    self.stat = statistic()

    self.parser.set_depth()
    self.deploy_handlers()

  def deploy_handlers(self):
    start_handler = CommandHandler('start', self.start)
    help_handler = CommandHandler('help', self.help)
    parse_handler = CommandHandler('link', self.link, pass_args=True)
    depth_handler = CommandHandler('depth', self.depth, pass_args=True)
    reset_handler = CommandHandler('reset', self.reset)
    top_handler = CommandHandler('top', self.top, pass_args=True)
    stop_words_handler = CommandHandler('stop_words', self.stop_words)
    describe_handler = CommandHandler('describe', self.describe)
    wordcloud_handler = CommandHandler('cloud', self.wordcloud)
    stop_handler = CommandHandler('stop', self.stop)
    echo_handler = MessageHandler(Filters.text, self.echo)
    unknown_handler = MessageHandler(Filters.command, self.unknown)

    self.dispatcher.add_handler(start_handler)
    self.dispatcher.add_handler(help_handler)
    self.dispatcher.add_handler(parse_handler)
    self.dispatcher.add_handler(depth_handler)
    self.dispatcher.add_handler(reset_handler)
    self.dispatcher.add_handler(top_handler)
    self.dispatcher.add_handler(echo_handler)
    self.dispatcher.add_handler(stop_words_handler)
    self.dispatcher.add_handler(describe_handler)
    self.dispatcher.add_handler(wordcloud_handler)
    self.dispatcher.add_handler(echo_handler)
    self.dispatcher.add_error_handler(self.error)
    self.dispatcher.add_handler(unknown_handler)

  def start(self, bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

  def error(self, bot, update, error):
    self.logger.warning('Update "%s" caused error "%s"', update, error)

  def help(self, bot, update):
    update.message.reply_text(cmd.HELP)

  def link(self, bot, update, args):
    self.parser.set_link(*args)
    self.parser.find_urls()
    self.stat.built_model(self.parser.get_pages_text())
    update.message.reply_text('Success. Link set. /help')

  def depth(self, bot, update, args):
    self.parser.set_depth(*args)
    update.message.reply_text('Success. Depth value changed. /help')

  def reset(self, bot, update):
    self.parser.reset()
    update.message.reply_text('Success. Depth, link and stats reset to default. /help')

  def top(self, bot, update, args):
    if len(args) > 1:
      self.stat.set_top_words_num(int(args[0]))
    if len(args) > 0 and args[-1] == 'desc':
      update.message.reply_text('Success. Here is the bot words. /help\n' +
                                '\n'.join([f'{key}, {value}' for
                                  key, value in self.stat.top_desc().items()]))
    else:
      update.message.reply_text('Success. Here is the top words. /help\n' +
                                '\n'.join([f'{key}, {value}' for
                                  key, value in self.stat.top_asc().items()]))

  def stop_words(self, bot, update):
    update.message.reply_text('Success. Here is stop words. /help\n' +
                              '\n'.join(self.stat.stop_words()))

  def describe(self, bot, update):
    describe.draw_words_freq(self.stat.get_model())
    describe.draw_words_length(self.stat.get_model())
    update.message.reply_text('Success. Graphics saved. /help')
    bot.sendPhoto(chat_id=update.message.chat_id, photo=open(cmd.WORDS_FREQ_IMG, 'rb'))
    bot.sendPhoto(chat_id=update.message.chat_id, photo=open(cmd.WORDS_LENGTH_IMG, 'rb'))

  def wordcloud(self, bot, update):
    describe.draw_wordcloud(self.stat.get_model())
    update.message.reply_text('Success. Wordcloud generated. /help')
    bot.sendPhoto(chat_id=update.message.chat_id, photo=open(cmd.WORDCLOUD_IMG, 'rb'))

  def echo(self, bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

  def stop(self, bot, update):
    print('stop')
    self.updater.idle()
    self.updater.stop()

  def launch(self):
    self.updater.start_polling()

  def unknown(self, bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")
