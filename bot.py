import telegram
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler, PicklePersistence, MessageHandler
import bot_views.start as start
import bot_views.settings as settings
import bot_views.statistics as statistics
import bot_views.test as test
import states


class LanguageLearningBot:
    def __init__(self, token):
        #persistence = PicklePersistence('langbot')
        self.updater = Updater(token, use_context=True)
        self._init_handlers()
        #self.updater.start_polling()

    def handle_update(self, req_json):
        update = telegram.Update.de_json(req_json, self.updater.bot)
        self.updater.dispatcher.process_update(update)

        print(f'hello ga: {req_json}')

    def _init_handlers(self):
        conv_handler = ConversationHandler(
            #per_message=True,
            entry_points=[
                CommandHandler('start', start.start_command),
            ],
            states={
                states.CHOOSING: [
                    CommandHandler('restart', start.start_command),
                    CallbackQueryHandler(test.test_begin, pattern=f'^{str(states.TEST)}$'),
                    CallbackQueryHandler(settings.settings_start, pattern=f'^{str(states.SETTINGS)}$'),
                    CallbackQueryHandler(statistics.show_statistics, pattern=f'^{str(states.STATISTICS)}$')
                ],
                states.TEST: [
                    CommandHandler('restart', start.start_command),
                    CallbackQueryHandler(test.test, pattern=f'@_\w+'),
                    # Заменить @ на состояния
                    CallbackQueryHandler(start.restart, pattern=f'@exit'),
                    CallbackQueryHandler(start.restart, pattern=f'@example'),
                ],
                states.STATISTICS: [
                    # start.restart()
                    CommandHandler('restart', start.start_command),
                    CallbackQueryHandler(start.restart, pattern=f'{states.EXIT}'),
                ],
                states.SETTINGS: [
                    CommandHandler('restart', start.start_command),
                    CallbackQueryHandler(settings.set_theme_menu, pattern=f'{states.SET_THEME}'),
                    CallbackQueryHandler(settings.set_right_answer_count_menu,
                                         pattern=f'{states.SET_RIGHT_ANSWER_COUNT}'),
                    CallbackQueryHandler(settings.set_session_words_count_menu,
                                         pattern=f'{states.SET_SESSION_WORDS_COUNT}'),
                    CallbackQueryHandler(start.restart, pattern=f'{states.EXIT}'),
                ],
                states.SET_THEME: [
                    CommandHandler('restart', start.start_command),
                    CallbackQueryHandler(settings.set_theme, pattern=f'\w+'),
                ],
                states.SET_RIGHT_ANSWER_COUNT: [
                    CommandHandler('restart', start.start_command),
                    CallbackQueryHandler(settings.set_right_answer_count, pattern=f'\w+'),
                ],
                states.SET_SESSION_WORDS_COUNT: [
                    CommandHandler('restart', start.start_command),
                    CallbackQueryHandler(settings.set_session_words_count, pattern=f'\w+'),
                ],
            },
            fallbacks=[
                CommandHandler('restart', start.restart),

            ],
            conversation_timeout=100,
        )
        self.updater.dispatcher.add_handler(conv_handler)
        self.updater.dispatcher.add_handler(MessageHandler(Filters.any, test.test123))

