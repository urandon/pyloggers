#!/usr/bin/python
# -*- coding: utf-8 -*-
# require https://github.com/python-telegram-bot/python-telegram-bot
from __future__ import print_function
from telegram.ext import Updater
import sys
import os
from . import base

try:
    from IPython.core.display import display, HTML
except ImportError:
    pass

BOT_URL = "https://telegram.me/uranlogger_bot"
GREETINGS_MSG = 'join <a href="{url}">{link}</a> and subscribe by <b>/reader {name}</b>'
# bot_url = "telegram.me/uranlogger_bot"
class TelegramLogger(base.NullLogger):
    def __init__(self,
                 token="72500331:AAGPGC4dI8Co3NJWHxno_HBGhLf57F1xHWA",
                 name="logger",
                 reader_chat_id=None,
                 print_dual_logging=True,
                 max_local_log_size=5):
        self.name = name
        self.log_queue = []
        self.reader_chat_id = None
        self.print_dual_logging = print_dual_logging
        if print_dual_logging:
            self._stdout = sys.stdout
        self.max_local_log_size = max_local_log_size

        self.bot = None
        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.addTelegramCommandHandler('reader', self.set_reader)
        self.dispatcher.addTelegramCommandHandler('ping', self.pong)
        self.dispatcher.addTelegramCommandHandler('flush', lambda b, u: self.flush())
        self.dispatcher.addTelegramCommandHandler('help', self.help)
        # I think it's a good choise for logger to launch bot in __init__
        try:
            display(HTML(GREETINGS_MSG.format(url=BOT_URL, link=BOT_URL.rsplit('/', 1)[1], name=name)))
        except:
            pass
        self.launch()

    def pong(self, bot, update):
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text='<{}> pong'.format(self.name))

    def help(self, bot, update):
        msg = '/ping -- echo, check bot if it is alive\n'\
              '/reader [name] -- set me as log reader\n'\
              '/flush flush the log queue'
        bot.sendMessage(chat_id=update.message.chat_id, text=msg)

    def set_reader(self, bot, update):
        text = update.message.text.strip()
        if len(text.split()) > 1:
            name = ' '.join(text.split()[1:]).strip().split()[0]
            if name != self.name:
                return

        self.reader_chat_id = update.message.chat_id
        self.bot = bot
        self.send_to_reader('You are a reader now')
        pass

    def send_to_reader(self, msg):
        self.bot.sendMessage(chat_id=self.reader_chat_id,
                             text='<{}> {}'.format(self.name, msg))

    def push(self, string, flush=True):
        self.log_queue.append(string)
        if self.print_dual_logging:
            self._stdout.write(string + '\n')
        if flush or len(self.log_queue) > self.max_local_log_size:
            self.flush()
        return self

    '''
    :param img: URL or image file to be sent
    :param caption: URL or image file to be sent
    images are not queued, so it can be missed if reader
    isn't subscribed yet
    Example:
    push_img(open('path/to/image.png', 'rb'))
    push_img('http://acme.corp/send_me_please.png')
    '''
    def push_img(self, img, caption='Image'): 
        if self.reader_chat_id is None or self.bot is None:
            return # TODO: add miss-log (if logs will be added)
        self.bot.sendPhoto(chat_id=self.reader_chat_id,
                           photo=img, caption=caption)
        return self
        

    def flush(self):
        if self.reader_chat_id is None or self.bot is None:
            return
        for msg in self.log_queue:
            self.send_to_reader(msg)
        self.log_queue = []

    def launch(self):
        self.updater.start_polling()

    def stop(self):
        self.updater.stop()

    def __del__(self):
        self.stop()


if __name__ == '__main__':
    print('pid: {}'.format(os.getpid()))
    tlogger = TelegramLogger()

    def nothing_to_do_there(logger=tlogger, repeat_after=15):
        from threading import Timer
        logger.push('nothing to do there')
        Timer(repeat_after, nothing_to_do_there).start()

    nothing_to_do_there()
