#!/usr/bin/python
# -*- coding: utf-8 -*-
# require https://github.com/python-telegram-bot/python-telegram-bot
from telegram import Updater
import os


class NullLogger(object):
    def __init__(self):
        pass

    def push(self, string, flush=True):
        return self

    def flush(self):
        return self


# bot_url = "telegram.me/uranlogger_bot"
class TelegramLogger(NullLogger):
    def __init__(self,
                 token="72500331:AAGPGC4dI8Co3NJWHxno_HBGhLf57F1xHWA",
                 name="logger@:",
                 reader_id=None,
                 print_dual_logging=True):
        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher
        self.bot = None
        self.name = name
        self.log_queue = []
        self.reader_id = reader_id
        self.reader_chat_id = None
        self.print_dual_logging = print_dual_logging
        self.dispatcher.addTelegramCommandHandler('reader', self.set_reader)
        self.dispatcher.addTelegramCommandHandler('ping', self.pong)
        self.dispatcher.addTelegramCommandHandler('help', self.help)
        # I think it's a good choise for logger to launch bot in __init__
        self.launch()

    def pong(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text='pong')

    def help(self, bot, update):
        msg = '/ping -- echo, check bot if it is alive\n'\
              '/reader -- set me as log reader'
        bot.sendMessage(chat_id=update.message.chat_id, text=msg)

    def set_reader(self, bot, update):
        self.reader_chat_id = update.message.chat_id
        self.bot = bot
        self.send_to_reader('You are a reader now')
        pass

    def send_to_reader(self, msg):
        self.bot.sendMessage(chat_id=self.reader_chat_id,
                             text=self.name + " " + msg)

    def push(self, string, flush=True):
        self.log_queue.append(string)
        if self.print_dual_logging:
            print string
        self.on_update()
        return self

    def on_update(self):
        if self.reader_chat_id is None or self.bot is None:
            return
        for msg in self.log_queue:
            self.send_to_reader(msg)
        self.log_queue = []

    def launch(self):
        self.updater.start_polling()

    def stop(self):
        self.updater.stop()

if __name__ == '__main__':
    print 'pid: {}'.format(os.getpid())
    tlogger = TelegramLogger()

    def nothing_to_do_there(logger=tlogger):
        logger.push('nothing to do there')

    from threading import Timer
    Timer(15, nothing_to_do_there).start()
