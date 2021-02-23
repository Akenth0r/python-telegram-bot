import telegram
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
import bot_views.start as start
import bot_views.settings as settings
import bot_views.statistics as statistics
import bot_views.test as test
import states


class LanguageLearningBot:
    def __init__(self, token):
        self.updater = Updater(token, use_context=True)
        self._init_handlers()

    def handle_update(self, req_json):
        update = telegram.Update.de_json(req_json, self.updater.bot)
        self.updater.dispatcher.process_update(update)

    def _init_handlers(self):
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start.start_command)],
            states={
                states.CHOOSING: [
                    CallbackQueryHandler(test.test_begin, pattern=f'^{str(states.TEST)}$'),
                    CallbackQueryHandler(settings.settings_start, pattern=f'^{str(states.SETTINGS)}$')
                ],
                states.TEST: [

                ],
                states.STATISTICS: [

                ],
                states.SETTINGS: [

                ],
            },
            fallbacks=[],
        )
        self.updater.dispatcher.add_handler(conv_handler)
