"""This module contains a Hotel class and all its CRUD actions"""

import json
import os
import sys


class Hotel:
    """Represents a Hotel and all its CRUD actions"""
    BASE_DIR = os.path.dirname(os.path.abspath("main.py"))
    FILE_PATH = os.path.join(BASE_DIR, "db", "hotels.json")

    def __init__(self, hotel_data):
        self.hotel_id = hotel_data['hotel_id']
        self.name = hotel_data['name']
        self.country = hotel_data['country']
        self.address = hotel_data['address']
        self.phone = hotel_data['phone']
        self.category = hotel_data['category']
        self.reserved_rooms = hotel_data['reserved_rooms']

    def map_to_dict(self):
        """Creates a dictionary representation of an object"""
        return self.__dict__

    @classmethod
    def save(cls, hotels):
        """Receives a list of hotels and stores them in a json file"""
        try:
            with open(cls.FILE_PATH, "w", encoding="UTF-8") as db_file:
                json.dump(hotels, db_file, indent=4)
        except (IOError, FileNotFoundError) as e:
            print(f"Exception in Hotel.save(): {e.strerror}")
            sys.exit(1)

    @classmethod
    def reserve_room(cls, hotel_id):
        """Reserves a hotel's room"""
        all_hotels = cls.load()
        for hotel in all_hotels:
            if hotel['hotel_id'] == hotel_id:
                hotel['reserved_rooms'] = hotel['reserved_rooms'] + 1
                cls.save(all_hotels)
                return True
        return False

    @classmethod
    def cancel_reservation(cls, hotel_id):
        """Cancels a hotel's reservation"""
        all_hotels = cls.load()
        for hotel in all_hotels:
            if hotel['hotel_id'] == hotel_id:
                hotel['reserved_rooms'] = hotel['reserved_rooms'] - 1
                if hotel['reserved_rooms'] < 0:
                    hotel['reserved_rooms'] = 0
                cls.save(all_hotels)
                return True
        return False

    @classmethod
    def create(cls, hotel):
        """Add a hotel to the hotels.json file"""
        all_hotels = cls.load()
        all_hotels.append(hotel.map_to_dict())
        cls.save(all_hotels)
        print(f"Hotel {hotel.name} created successfully")

    @classmethod
    def load(cls):
        """Loads all the hotels stored in hotels.json file"""
        if not os.path.exists(cls.FILE_PATH):
            return []
        try:
            with open(cls.FILE_PATH, "r", encoding="UTF-8") as db_file:
                return json.load(db_file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Exception in load(): Invalid Hotel DB file")
            return []

    @classmethod
    def modify(cls, hotel_id, field_to_modify, value):
        """Modifies a hotel field by its hotel id"""
        all_hotels = cls.load()
        for hotel in all_hotels:
            if hotel['hotel_id'] == hotel_id:
                hotel[field_to_modify] = value
                cls.save(all_hotels)
                return True
        return False

    @classmethod
    def search_by(cls, field_name, value):
        """Searches a hotel by a given field name"""
        all_hotels = cls.load()
        for hotel in all_hotels:
            if hotel[field_name] == value:
                return hotel
        return "Hotel not found"

    @classmethod
    def display_by_name(cls, name):
        """Searches and displays a hotel's information by hotel name"""
        cls.display(cls.search_by("name", name))

    @classmethod
    def display_by_id(cls, hotel_id):
        """Searches and displays a hotel's information by hotel id"""
        cls.display(cls.search_by("hotel_id", hotel_id))

    @classmethod
    def display(cls, hotel):
        """Displays a hotel's information in the console"""
        if hotel == "not found" or hotel is None:
            print("No hotel information was found!")
            return False
        print(f"ID: {hotel['hotel_id']}"
              f" | Name: {hotel['name']}"
              f" | Country: {hotel['country']}"
              f" | Address: {hotel['address']}"
              f" | Phone: {hotel['phone']}"
              f" | Category: {hotel['category']} stars")
        return True

    @classmethod
    def display_all(cls):
        """Displays in the console all the hotels stored in the DB"""
        all_hotels = cls.load()
        for hotel in all_hotels:
            cls.display(hotel)

    @classmethod
    def delete_by(cls, field_name, value):
        """Deletes a hotel by a given field name"""
        all_hotels = cls.load()
        update_list = [h for h in all_hotels if h[field_name] != value]
        cls.save(update_list)
        print(f"Hotel with {field_name}: {value} was deleted")
