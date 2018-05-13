from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import CommandHandler
import cmd_description
import logging


class parse_bot:
  def __init__(self):
    logging.basicConfig(
      format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
      level=logging.INFO
    )
    token = '557754452:AAFuMjFF2O80b7B8s7_5n_0ljMeGcYDeHYM'
    self.updater = Updater(token=token)
    self.dispatcher = self.updater.dispatcher
    self.deploy_handlers()

  def deploy_handlers(self):
    start_handler = CommandHandler('start', self.start)
    self.dispatcher.add_handler(start_handler)
    
    stop_handler = CommandHandler('stop', self.stop)
    self.dispatcher.add_handler(stop_handler)

    help_handler = CommandHandler('help', self.help)
    self.dispatcher.add_handler(help_handler)

    echo_handler = MessageHandler(Filters.text, self.echo)
    self.dispatcher.add_handler(echo_handler)

    self.dispatcher.add_error_handler(self.error)

    unknown_handler = MessageHandler(Filters.command, self.unknown)
    self.dispatcher.add_handler(unknown_handler)

  def start(self, bot, update):
    """start this bot and use its features"""
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

  def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

  def stop(self, bot, update):
    print('stop')
    self.updater.idle()
    self.updater.stop()
  
  def help(self, bot, update):
    update.message.reply_text(cmd_description.HELP)

  def echo(self, bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

  def launch(self):
    self.updater.start_polling()

  def unknown(self, bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")
