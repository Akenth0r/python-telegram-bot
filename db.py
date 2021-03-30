from datetime import datetime, timedelta

from sqlalchemy import *  # create_engine, Column, Integer
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, scoped_session
from sqlalchemy.pool import NullPool
from sqlalchemy import func

import repeat_config

URI = 'postgresql://pteegqukkuhdya:63913c9f332b517edeb9b86bb0f6ccefecb5cb74f9d542bf331c01b5fe429d87@ec2-54-155-87-214.eu-west-1.compute.amazonaws.com:5432/dc3q6c1898ed1j'

engine = create_engine(URI)

base = declarative_base()
Session = scoped_session(sessionmaker(bind=engine))


class UserSettings(base):
    __tablename__ = 'user_settings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    theme_id = Column(String, ForeignKey('theme.id'))
    right_answer_count = Column(Integer, default=5)
    session_words_count = Column(Integer, default=5)
    user = relationship("User", back_populates="settings")
    # def __init__(self, theme_id='animals', right_answer_count=1, session_words_count=5):
    #     self.theme_id = theme_id
    #     self.right_answer_count = right_answer_count
    #     self.session_words_count = session_words_count


class WordStatistics(base):
    __tablename__ = 'word_statistics'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_statistics_id = Column(Integer, ForeignKey('user_statistics.id'))
    theme_word_id = Column(Integer, ForeignKey('theme_word.id'))
    right_answer_count = Column(Integer, default=0)
    updated_at = Column(DateTime)


# Статистика пользователя
class UserStatistics(base):
    __tablename__ = 'user_statistics'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    remembered_words = relationship("WordStatistics", order_by='asc(WordStatistics.updated_at)')
    user = relationship("User", back_populates="statistics")


# Пользователь
class User(base):
    __tablename__ = 'user'
    id = Column(Integer, unique=True, primary_key=True)
    settings = relationship("UserSettings", uselist=False, back_populates="user")
    statistics = relationship("UserStatistics", uselist=False, back_populates="user")
    last_session = Column(DateTime)

    def save(self):
        session = Session()
        session.add(self)
        session.commit()


class ThemeWord(base):
    __tablename__ = "theme_word"
    id = Column(Integer, primary_key=True, autoincrement=True)
    theme_id = Column(String, ForeignKey('theme.id'))
    original = Column(String, nullable=False)
    translation = Column(String, nullable=False)
    example = Column(String)


# Тема - массив слов и название
class Theme(base):
    # def __init__(self, title: str = '', words: List[ThemeWord] = None):
    #     self.title: str = title
    #     self.words: List[ThemeWord] = words
    __tablename__ = "theme"
    id = Column(String, primary_key=True)
    words = relationship("ThemeWord")

    def add_word(self, word: ThemeWord):
        session = Session()
        session.add(word)
        session.commit()


def get_user(id):
    session = Session()
    user = session.query(User).get(id)
    if not user:
        user = User()
        user.id = id
        settings = UserSettings()
        settings.user_id = user.id
        settings.theme_id = 'animals'
        statistics = UserStatistics()
        statistics.user_id = user.id
        session.add(user)
        session.add(settings)
        session.add(statistics)
        session.commit()
    return user


def get_user_words_to_repeat_count(id):
    user = get_user(id)
    session = Session()
    count = session.query(WordStatistics).filter(
        (datetime.utcnow() - WordStatistics.updated_at >= timedelta(minutes=repeat_config.WORD_REPEAT_PERIOD)) & (WordStatistics.user_statistics_id == user.statistics.id)).count()
    return count

def get_user_remembered_words(user: User):
    remembered_words = user.statistics.remembered_words
    words = []
    session = Session()
    for word in remembered_words:
        words.append(session.query(ThemeWord).filter(ThemeWord.id == word.theme_word_id).one())
        print(word.theme_word_id)

    print("*" * 80)
    for word in words:
        print(word.original)

    return words
base.metadata.create_all(engine)
