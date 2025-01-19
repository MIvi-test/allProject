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

            class aside_History(Base):
                __tablename__ = f'aside_History_{Id}'
                id = Column(Integer, primary_key=True)
                number = Column(Integer, unique=True)
                photo = Column(String, unique=True)

            Base.metadata.create_all(engine)
            return True 
        except Exception as ex:
            print(f'Error creating history table: {ex}')
            return False
        
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
    

    def save_result(user_id, id,photo, rating, description:str, from_aside:bool) -> bool:
        '''Save in history users'''
        global session, engine

        if photo == None:
            photo = f'{id}.jpg'
        if not(from_aside):
            session.execute(text(f'''INSERT INTO public."History_{user_id}" ("number", photo, description, rating)
                                                                 VALUES ({id},'{photo}', '{description}', {rating});'''))
        else:
            session.execute(text(f'''UPDATE public."History_{user_id}" 
                                    SET photo = '{photo}', description = '{description}', rating = {rating}
                                    WHERE id = {id};'''))
        session.commit()




    def delete_resume(number) -> bool:
        global session

    def delete_replic(number) -> bool:
        global session
        info = session.query(Resume).filter(Resume.id == number).first()
        session.delete(info)
        session.commit()
        return True



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
            info = session.query(Resume).filter(Resume.id > ID[0]).first()
            
            return [info.id, info.file_id]
        except Exception as ex: # if all rated photos
            print(ex)
            return None
        

    def set_aside_photo(photo_id, user_id, number) -> str:
        global session 
        print(user_id)
        session.execute(text(f'''INSERT INTO public."aside_History_{user_id}" (number,photo) VALUES ({number},'{photo_id}');'''))

        session.execute(text(f'''INSERT INTO public."History_{user_id}" ("number", photo)
                                                                 VALUES ({number},'{photo_id}');'''))
        session.commit()
        return 'aside photo added'


    def get_aside_photo(user_id) -> str:
        '''return first photo_id from aside_history'''
        global session 
        info = session.execute(text(f'''SELECT * FROM public."aside_History_{user_id}" ORDER BY id ASC LIMIT 1;''')).fetchone()
        session.execute(text(f'''DELETE FROM  public."aside_History_{user_id}" WHERE id = {info.id};'''))
        session.commit()
        

        print(info.photo)
        return info

    def get_full():
        global session, engine
        # inspector = inspect(engine)
        # print(Database.get_next_photo(1856040379))
        return
        
if  __name__ == '__main__':
    # Database.get_creator_id()
    # Resumes = Database.get_full()
    Database.delete_replic("AgACAgIAAxkBAAIHymdZF6JL8I_FHXVZmg6aa3NRLxktAAJQ8DEb4oLISgLxERyGco_TAQADAgADdwADNgQ")

