"""Test cases for the Reservation model"""

import unittest
from models.reservation import Reservation


class TestReservation(unittest.TestCase):
    """Test cases for the Reservation class"""
    def setUp(self):
        reservation_data = {
            "reservation_id": 1,
            "customer_id": 1,
            "hotel_id": 1,
            "room_id": 1,
            "nights": 2,
            "price_per_night": 2000
        }
        self.reservation = Reservation(reservation_data)

    def test_create(self):
        """Test create a reservation"""
        print("\nRunning test_create")
        Reservation.create(self.reservation)
        all_reservations = Reservation.load()
        self.assertEqual(len(all_reservations), 1)

    def test_cancel(self):
        """Test cancel a reservation"""
        print("\nRunning test_cancel")
        Reservation.cancel(1)
        all_reservations = Reservation.load()
        self.assertEqual(len(all_reservations), 0)


if __name__ == "__main__":
    unittest.main()
