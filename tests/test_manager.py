import unittest
import pandas as pd
import tempfile
import os
from pathlib import Path
from inventory_manager.core.manager import InventoryManager


class TestInventoryManager(unittest.TestCase):
    def setUp(self):
        """Préparation des tests avec des données temporaires."""
        self.temp_dir = tempfile.mkdtemp()
        self.create_test_data()
        self.manager = InventoryManager(self.temp_dir)

    def create_test_data(self):
        """Crée des données de test."""
        test_data = pd.DataFrame(
            {
                "name": ["Produit1", "Produit2", "Produit3"],
                "quantity": [10, 20, 30],
                "unit_price": [100.0, 200.0, 300.0],
                "category": ["Cat1", "Cat2", "Cat1"],
            }
        )
        test_data.to_csv(Path(self.temp_dir) / "test.csv", index=False)

    def tearDown(self):
        """Nettoyage après les tests."""
        for file in Path(self.temp_dir).glob("*"):
            file.unlink()
        os.rmdir(self.temp_dir)

    def test_consolidate_files(self):
        """Test de la consolidation des fichiers."""
        self.manager.consolidate_files()
        self.assertIsNotNone(self.manager.inventory_df)
        self.assertEqual(len(self.manager.inventory_df), 3)

    def test_search_products(self):
        """Test de la recherche de produits."""
        self.manager.consolidate_files()

        # Test recherche par nom
        results = self.manager.search_products(name="Produit1")
        self.assertEqual(len(results), 1)

        # Test recherche par catégorie
        results = self.manager.search_products(category="Cat1")
        self.assertEqual(len(results), 2)

    def test_generate_report(self):
        """Test de la génération de rapport."""
        self.manager.consolidate_files()
        report_file = Path(self.temp_dir) / "report.csv"
        self.manager.generate_report(str(report_file))
        self.assertTrue(report_file.exists())
