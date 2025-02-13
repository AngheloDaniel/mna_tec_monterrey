"""This module contains a class Reservation"""

import json
import os
import sys


class Reservation:
    """Represents a Hotel's reservation and its Create and Delete methods"""
    BASE_DIR = os.path.dirname(os.path.abspath("main.py"))
    FILE_PATH = os.path.join(BASE_DIR, "db", "reservations.json")
    CUSTOMERS_FILE_PATH = os.path.join(BASE_DIR, "db", "customers.json")
    HOTELS_FILE_PATH = os.path.join(BASE_DIR, "db", "hotels.json")

    def __init__(self, reservation_data):
        self.reservation_id = reservation_data['reservation_id']
        self.customer_id = reservation_data['customer_id']
        self.hotel_id = reservation_data['hotel_id']
        self.room_id = reservation_data['room_id']
        self.nights = reservation_data['nights']
        self.price_per_night = reservation_data['price_per_night']

    @classmethod
    def load(cls):
        """Loads all the reservations stored in reservations.json file"""
        if not os.path.exists(cls.FILE_PATH):
            print("Reservation path is not found")
            return []
        try:
            with open(cls.FILE_PATH, "r", encoding="UTF-8") as db_file:
                return json.load(db_file)
        except FileNotFoundError:
            return []

    def map_to_dict(self):
        """Creates a dictionary representation of an object"""
        return self.__dict__

    @classmethod
    def create(cls, reservation):
        """Creates a new reservation"""
        all_reservations = cls.load()
        all_reservations.append(reservation.map_to_dict())
        cls.save(all_reservations)
        print("A new reservation has been created")

    @classmethod
    def save(cls, reservations):
        """Saves all the reservations in a json file"""
        try:
            with open(cls.FILE_PATH, "w", encoding="UTF-8") as db_file:
                json.dump(reservations, db_file, indent=4)
        except (IOError, FileNotFoundError) as e:
            print(f"Exception in Reservation.save(): {e.strerror}")
            sys.exit(1)

    @classmethod
    def cancel(cls, reservation_id):
        """Cancels a hotel reservation"""
        all_reservations = cls.load()
        updated_list = [r for r in all_reservations
                        if r['reservation_id'] != reservation_id]
        cls.save(updated_list)
        print(f"Reservation {reservation_id} has been cancelled")
