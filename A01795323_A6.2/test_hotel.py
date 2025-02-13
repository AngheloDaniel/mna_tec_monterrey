"""Test cases for the Hotel model"""

import unittest
from models.hotel import Hotel


class TestHotel(unittest.TestCase):
    """Test cases for the Hotel class"""
    def setUp(self):
        Hotel.delete_by("hotel_id", 1)
        Hotel.delete_by("hotel_id", 2)
        hotel_data = {
            "hotel_id": 1,
            "name": "Hyatt",
            "country": "México",
            "address": "Blvd Puerta de Hierro 5065, Zapopan, Jalisco",
            "phone": "3338831234",
            "category": "5",
            "reserved_rooms": 0
        }

        hotel_data_2 = {
            "hotel_id": 2,
            "name": "Hilton",
            "country": "México",
            "address": "Av. Juarez 70, Cuauhtémoc, Ciudad de México",
            "phone": "5551305300",
            "category": "5",
            "reserved_rooms": 0
        }
        self.hotel = Hotel(hotel_data)
        self.hotel_2 = Hotel(hotel_data_2)

    def test_create_display_modify_hotel(self):
        """Test all non-deleting methods"""
        print("\nRunning test_create_display_modify_hotel")
        Hotel.create(self.hotel)
        Hotel.create(self.hotel_2)
        Hotel.display_by_id(1)
        Hotel.display_by_name("Hyatt")
        Hotel.display_all()
        Hotel.reserve_room(1)
        Hotel.cancel_reservation(1)
        hotel = Hotel.search_by("name", "Hilton")
        Hotel.display(hotel)
        Hotel.modify(1, "name", "New Hyatt")
        all_hotels = Hotel.load()
        self.assertEqual(all_hotels[0]['reserved_rooms'], 0)
        self.assertEqual(all_hotels[0]['name'], "New Hyatt")
        self.assertEqual(all_hotels[1]['name'], "Hilton")
        self.assertEqual(len(all_hotels), 2)

    def test_delete_hotel(self):
        """Test deleting a hotel"""
        print("\nRunning test_delete_hotel")
        Hotel.delete_by("hotel_id", 1)
        Hotel.delete_by("hotel_id", 2)
        all_hotels = Hotel.load()
        self.assertEqual(len(all_hotels), 0)

    def test_display_invalid_hotel(self):
        """Test displaying an invalid hotel"""
        self.assertFalse(Hotel.display(None), "Invalid hotel")

    def test_hotel_not_found(self):
        """Test searching for an invalid hotel"""
        self.assertEqual(Hotel.search_by("hotel_id", 3), "Hotel not found")

    def test_invalid_edition(self):
        """Test editing an invalid hotel"""
        response = Hotel.modify(5, "name", "Invalid Hotel")
        self.assertEqual(response, False)


if __name__ == "__main__":
    unittest.main()
