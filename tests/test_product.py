import unittest
from inventory_manager.models.product import Product


class TestProduct(unittest.TestCase):
    def setUp(self):
        """Initialisation des données de test."""
        self.product_data = {
            "name": "Test Product",
            "quantity": 10,
            "unit_price": 99.99,
            "category": "Test Category",
        }
        self.product = Product(**self.product_data)

    def test_product_creation(self):
        """Test de la création d'un produit."""
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.quantity, 10)
        self.assertEqual(self.product.unit_price, 99.99)
        self.assertEqual(self.product.category, "Test Category")

    def test_to_dict(self):
        """Test de la conversion en dictionnaire."""
        product_dict = self.product.to_dict()
        self.assertEqual(product_dict, self.product_data)

    def test_from_dict(self):
        """Test de la création depuis un dictionnaire."""
        new_product = Product.from_dict(self.product_data)
        self.assertEqual(new_product.name, self.product.name)
        self.assertEqual(new_product.quantity, self.product.quantity)
        self.assertEqual(new_product.unit_price, self.product.unit_price)
        self.assertEqual(new_product.category, self.product.category)

    def test_invalid_data(self):
        """Test de la gestion des données invalides."""
        invalid_data = {
            "name": "Test Product",
            "quantity": "invalid",  # Should be int
            "unit_price": 99.99,
            "category": "Test Category",
        }
        with self.assertRaises(TypeError):
            Product.from_dict(invalid_data)


if __name__ == "__main__":
    unittest.main()
