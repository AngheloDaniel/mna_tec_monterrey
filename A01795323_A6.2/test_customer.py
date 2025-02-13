"""Test cases for Customer model"""

import unittest
from models.customer import Customer


class TestCustomer(unittest.TestCase):
    """Test cases for the Customer class"""
    def setUp(self):
        Customer.delete(1)
        customer_data = {
            'customer_id': 1,
            'name': "Emiliano Zapata",
            'phone': "5535698789",
            "address": "Bosque de Chapultepec 1550, Miguel Hidalgo, CDMX",
            "credit_card": "5698-5621-5532-4742"
        }
        self.customer = Customer(customer_data)

    def test_create(self):
        """Test create and display a customer"""
        print("\nRunning test_create")
        Customer.create(self.customer)
        all_customers = Customer.load()
        Customer.display(1)
        self.assertEqual(len(all_customers), 1)

    def test_modify(self):
        """Test modify a customer"""
        print("\nRunning test_modify")
        Customer.create(self.customer)
        Customer.edit(1, "name", "Emiliano Zapata Salazar")
        all_customers = Customer.load()
        self.assertEqual(all_customers[0]['name'], "Emiliano Zapata Salazar")

    def test_delete(self):
        """Test delete a customer"""
        print("\nRunning test_delete")
        Customer.delete(1)
        all_customers = Customer.load()
        self.assertEqual(len(all_customers), 0)

    def test_invalid_edition(self):
        """Test editing an invalid customer"""
        response = Customer.edit(5, "name", "Invalid Customer")
        self.assertEqual(response, False)

    def test_invalid_display(self):
        """Test displaying an invalid customer"""
        response = Customer.display(5)
        self.assertEqual(response, False)


if __name__ == "__main__":
    unittest.main()
