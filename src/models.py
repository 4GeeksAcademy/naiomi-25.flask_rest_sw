from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean,Table,Column,ForeignKey,DateTime
from sqlalchemy.orm import Mapped, mapped_column,relationship
from datetime import datetime

from typing import List

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    name :Mapped[str] = mapped_column (String(120),nullable = True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    suscription_date : Mapped[datetime] = mapped_column(DateTime())
    

    people_favorite : Mapped[List['People']] = relationship (secondary = 'favorites_people', back_populates= 'user_favorites')
    planet_favorite : Mapped[List['Planet']]= relationship( secondary = 'favorites_planet', back_populates = 'user_favorites')



    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            'name':self.name,
            'suscription_date':self.suscription_date 
        }
    


class People(db.Model):

    __tablename__ = 'people'

    id:Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(nullable = False)
    age : Mapped[int] = mapped_column(nullable = False)

    user_favorites: Mapped[List['User']]= relationship( secondary = 'favorites_people', back_populates = 'people_favorite')



    def serialize(self):
        return{
            'id':self.id,
            'name': self.name,
            'age': self.age

        }
    

    
class Planet(db.Model):

    id : Mapped[int] = mapped_column(primary_key=True) 
    name : Mapped[str] = mapped_column(nullable = False)  
    gravity: Mapped[bool] = mapped_column(nullable = False)
    temperature:Mapped[int]= mapped_column(nullable = False)

    user_favorites: Mapped[List['User']]= relationship( secondary = 'favorites_planet', back_populates = 'planet_favorite')

    def serialize(self):
        return{
            'id':self.id,
            'name': self.name,
            'gravity': self.gravity,
            'temperature': self.temperature
        }


Favorites_planet= Table(
    'favorites_planet',
    db.metadata,
    Column('planet_id',ForeignKey('planet.id'),primary_key=True),
    Column ('user_id',ForeignKey('user.id'),primary_key=True)
)
Favorites_people= Table(
    'favorites_people',
    db.metadata,
    Column ('user_id',ForeignKey('user.id'),primary_key=True),
    Column('people_id',ForeignKey('people.id'),primary_key=True)

)
