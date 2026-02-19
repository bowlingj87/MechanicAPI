from datetime import date
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, Integer, ForeignKey 
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List

class Base(DeclarativeBase): #Create a base class for our models
    pass

db = SQLAlchemy(model_class= Base) # Initialize SQLAlchemy with custom base class

service_ticket_mechanic = db.Table(
      'service_ticket_mechanic',
      Base.metadata,
      db.Column('service_ticket_id', db.ForeignKey('service_tickets.id')),
      db.Column('mechanic_id',db.ForeignKey('mechanics.id'))
)

service_ticket_inventory = db.Table(
      'service_ticket_inventory',
      Base.metadata,
      db.Column('service_ticket_id', db.ForeignKey('service_tickets.id'),primary_key=True),
      db.Column('inventory_id',db.ForeignKey('inventory.id'), primary_key=True)
)
class Customer(Base):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)

    service_tickets : Mapped[List['Service_Ticket']] = db.relationship(back_populates='customer', cascade="all, delete") #New relationship attribute


class Service_Ticket(Base):
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    service_date: Mapped[date] = mapped_column(db.Date, nullable=False) 
    service_description: Mapped[str] = mapped_column(db.String(300))
    vin: Mapped[str] = mapped_column(db.String(17), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'), nullable=False)

    customer: Mapped['Customer'] = db.relationship(back_populates='service_tickets') #New relationship attribute
    mechanics: Mapped[List['Mechanic']] = db.relationship(secondary= service_ticket_mechanic, back_populates='service_tickets')
    inventory: Mapped[List['Inventory']] = db.relationship(secondary=service_ticket_inventory, back_populates='service_tickets')

class Mechanic(Base):
        __tablename__ = 'mechanics'

        id: Mapped[int] = mapped_column(primary_key=True)
        name: Mapped[str] = mapped_column(db.String(255))
        email: Mapped[str] = mapped_column(db.String(360))
        phone: Mapped[str] = mapped_column(db.String(20))

        service_tickets: Mapped[List['Service_Ticket']] = db.relationship(secondary=service_ticket_mechanic, back_populates='mechanics')

class Inventory(Base):
    __tablename__ = 'inventory'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)

    service_tickets: Mapped[List['Service_Ticket']] = db.relationship(secondary=service_ticket_inventory, back_populates="inventory")

    