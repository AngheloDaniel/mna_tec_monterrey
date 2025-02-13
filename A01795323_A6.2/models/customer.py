"""This model contains the Customer class and its CRUD methods"""

import json
import os
import sys


class Customer:
    """This class represents a Hotel's customer and all the CRUD actions"""
    BASE_DIR = os.path.dirname(os.path.abspath("main.py"))
    FILE_PATH = os.path.join(BASE_DIR, "db", "customers.json")

    def __init__(self, customer_data):
        self.customer_id = customer_data['customer_id']
        self.name = customer_data['name']
        self.phone = customer_data['phone']
        self.address = customer_data['address']
        self.credit_card = customer_data['credit_card']

    def map_to_dict(self):
        """Creates a dictionary representation of an object"""
        return self.__dict__

    @classmethod
    def create(cls, customer):
        """Add a customer to the customers.json file"""
        all_customers = cls.load()
        all_customers.append(customer.map_to_dict())
        cls.save(all_customers)
        print(f"Customer {customer.name} created successfully")

    @classmethod
    def save(cls, customers):
        """Receives a list of customers and stores them in a json file"""
        try:
            with open(cls.FILE_PATH, "w", encoding="UTF-8") as db_file:
                json.dump(customers, db_file, indent=4)
        except (IOError, FileNotFoundError) as e:
            print(f"Exception in Customer.save(): {e.strerror}")
            sys.exit(1)

    @classmethod
    def load(cls):
        """Loads all the customers stored in customers.json file"""
        try:
            if not os.path.exists(cls.FILE_PATH):
                return []
            with open(cls.FILE_PATH, "r", encoding="UTF-8") as db_file:
                return json.load(db_file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Exception in load(): Invalid Customer DB file")
            return []

    @classmethod
    def delete(cls, customer_id):
        """Removes a customer by id"""
        all_customers = cls.load()
        updated_list = [c for c in all_customers
                        if c['customer_id'] != customer_id]
        cls.save(updated_list)

    @classmethod
    def edit(cls, customer_id, field_name, value):
        """Edits a customer attribute by customer id"""
        all_customers = cls.load()
        for customer in all_customers:
            if customer['customer_id'] == customer_id:
                customer[field_name] = value
                cls.save(all_customers)
                return True
        return False

    @classmethod
    def display(cls, customer_id):
        """Displays all the customer information in the console"""
        all_customers = cls.load()
        for customer in all_customers:
            if customer['customer_id'] == customer_id:
                print(f"ID: {customer['customer_id']}"
                      f" | Name: {customer['name']}"
                      f" | Phone: {customer['phone']}"
                      f" | Address: {customer['address']}"
                      f" | Credit Card: {customer['credit_card']}")
                return True
        print(f"Customer with ID {customer_id} not found")
        return False
