from sqlalchemy import * # create_engine, Column, Integer

URI = "postgres://pteegqukkuhdya:63913c9f332b517edeb9b86bb0f6ccefecb5cb74f9d542bf331c01b5fe429d87@ec2-54-155-87-214.eu-west-1.compute.amazonaws.com:5432/dc3q6c1898ed1j"

engine = create_engine("sqlite:///bot.db", echo=True)

Base = declarative_base()


class Settings(Base):
    __tablename__ = 'settings'
    theme_id = Column(String, )
    right_answer_count = Column(Integer)
    session_words_count = Column(Integer)

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    theme_id = Column(String)
    right_answer_count = Column(Integer)
    session_words_count = Column(Integer)


    "user_id": 247603712,
    "settings": {
        "theme_id": "animals",
        "right_answer_count": 1,
        "session_words_count": 5
    },
    "statistics": {
        "remembered_words_count": 0,
        "words_left": 0,
        "remembered_words_list": {
            "Shark": 1,
            "Giraffe": 0,
            "Camel": 0,
            "Dog": 0,
            "Gorilla": 0,
            "Whale": 1,
            "Octopus": 1,
            "Woodpecker": 1,
            "Cat": 0,
            "Cheetah": 1
        }
    }
