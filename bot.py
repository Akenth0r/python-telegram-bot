import telegram
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler, PicklePersistence
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
        update: telegram.Update = telegram.Update.de_json(req_json, self.updater.bot)

        #self.updater.dispatcher.process_update(update)
        # if update['callback_query'] != None:
        #     print(update['callback_query']['message'])
        if update.message is not None:
            if update.message.text == '/start':
                start.start_command(update)
            return

        state_map = {
            str(states.TEST): test.test_begin,
            str(states.EXIT): start.restart,
            str(states.STATISTICS): statistics.show_statistics,
            str(states.SETTINGS): settings.settings_start,
            str(states.SET_THEME): settings.set_theme_menu,
            str(states.SET_RIGHT_ANSWER_MENU): settings.set_right_answer_count_menu,
            str(states.SET_SESSION_WORDS_MENU): settings.set_session_words_count_menu,
            '@exit': start.restart,
            '@example': start.restart,
            '@': test.test,
            '@ac': settings.set_right_answer_count,
            '@wc': settings.set_session_words_count,
            '@th': settings.set_theme,
        }

        if update.callback_query is not None:
            #update.callback_query.answer('Подожди красавчик (лабу примите, пж)')
            info = update.callback_query.data.split('_')
            key = info[0]
            state_map[key](update, None)
       # print(update.callback_query.message)


    def _init_handlers(self):
        disp = self.updater.dispatcher
        #disp.add_handler(CommandHandler('start', start.start_command))
        #disp.add_handler(CallbackQueryHandler(test.test_begin, pattern=f'^{str(states.TEST)}$'))
        disp.add_handler(CallbackQueryHandler(test.test, pattern=f'@_\w+'))
        disp.add_handler(CallbackQueryHandler(start.restart, pattern=f'@exit'))
        disp.add_handler(CallbackQueryHandler(start.restart, pattern=f'@example'))

        # Settings
        #disp.add_handler(CallbackQueryHandler(settings.settings_start, pattern=f'^{str(states.SETTINGS)}$'))
        # I changed my mind
        #disp.add_handler(CallbackQueryHandler(settings.set_theme_menu, pattern=f'{states.SET_THEME}'))
        # disp.add_handler(CallbackQueryHandler(settings.set_right_answer_count_menu,
        #                      pattern=f'{states.SET_RIGHT_ANSWER_COUNT}'))
        # disp.add_handler(CallbackQueryHandler(settings.set_session_words_count_menu,
        #                      pattern=f'{states.SET_SESSION_WORDS_COUNT}'))
        disp.add_handler(CallbackQueryHandler(settings.set_right_answer_count, pattern=f'@ac_\w+'))
        disp.add_handler(CallbackQueryHandler(settings.set_session_words_count, pattern=f'@wc_\w+'))
        disp.add_handler(CallbackQueryHandler(settings.set_theme, pattern=f'@th_\w+'))
        #disp.add_handler(CallbackQueryHandler(start.restart, pattern=f'{states.EXIT}'))

        disp.add_handler(CallbackQueryHandler(statistics.show_statistics, pattern=f'^{str(states.STATISTICS)}$'))



