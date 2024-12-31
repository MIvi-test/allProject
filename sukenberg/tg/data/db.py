from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import inspect,text
import os

Base = declarative_base()


class Resume(Base):
    __tablename__ = 'resume'
    id = Column(Integer, primary_key=True)
    photo = Column(String)
    rating = Column(Integer)  # 10 points
    description = Column(String)
    creator = Column(Integer)
    file_id = Column(String)
    


engine = create_engine('postgresql://postgres:1@localhost/postgres')
session = Session(bind=engine)


class Database:
    name = None
    def add_photo(photo, creator) -> bool:
        global session
        new_res = Resume(
            photo=f'{(datetime.now())}.jpg',
            rating=None,
            description=None,
            creator=creator,
            file_id=photo  # TODO: file_id from Telegram API
        )
        session.add(new_res)
        session.commit()


    def get_creator_id(ID):
        global session
        info = session.query(Resume).get(ID)
        return info.creator
        # return 1856040379
    

    def save_result(user_id, ids: list, rating, description) -> bool:
        # ids = [serial id, tg id, ]
        '''Save in history users'''
        global session, engine
        if ids[1] == None:
            ids[1] = f'{ids[0]}.jpg'
        session.execute(text(f'''INSERT INTO public."History_{user_id}" ("number", photo, description, rating)
                                                                 VALUES ({ids[0]},'{ids[1]}', '{description}', {rating});'''))
        session.commit()


    def create_history(Id:int) -> bool:
        global engine
        try:
            class History(Base):
                __tablename__ = f'History_{Id}'
                id = Column(Integer, primary_key=True)
                number = Column(Integer)    
                photo = Column(String)
                create_at = Column(DateTime, default=datetime.now)
                description = Column(String)
                rating = Column(Integer)
            Base.metadata.create_all(engine)
            return True 
        except Exception as ex:
            print(f'Error creating history table: {ex}')
            return False

    def delete_resume(photo_id) -> bool:
        global session

    def get_history() -> list[str]:
        global session

    def get_next_photo(user_id) -> list[int, str]:
        '''
         return [ serial_id, 'telegram id']
        '''
        try:
            global session
            ID = session.execute(text(f'''SELECT "number" FROM public."History_{user_id}" ORDER BY "number" DESC LIMIT 1;''')).fetchone()#serial_id photo in resume
            if ID == None:
                ID = [0]
            info = session.query(Resume).filter(Resume.id == ID[0]+1).first()
            
            return [info.id, info.file_id]
        except Exception as ex: # if all rated photos
            print(ex)
            return None
        

    def set_aside_photo(photo_id) -> int:
        pass

    def get_full():
        global session, engine
        inspector = inspect(engine)
        print(Database.get_next_photo(1856040379))
        
if  __name__ == '__main__':

    Database.get_full()

