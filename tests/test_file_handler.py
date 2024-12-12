import unittest
import pandas as pd
import tempfile
import os
from pathlib import Path
from inventory_manager.utils.file_handler import FileHandler


class TestFileHandler(unittest.TestCase):
    def setUp(self):
        """Préparation des tests avec des fichiers temporaires."""
        self.temp_dir = tempfile.mkdtemp()
        self.create_test_files()

    def create_test_files(self):
        """Crée des fichiers de test."""
        # Fichier CSV valide
        valid_data = pd.DataFrame(
            {
                "name": ["Product1", "Product2"],
                "quantity": [10, 20],
                "unit_price": [100.0, 200.0],
                "category": ["Cat1", "Cat2"],
            }
        )
        valid_data.to_csv(Path(self.temp_dir) / "valid.csv", index=False)

        # Fichier CSV invalide (colonnes manquantes)
        invalid_data = pd.DataFrame(
            {"name": ["Product3"], "price": [300.0]}  # Colonne incorrecte
        )
        invalid_data.to_csv(Path(self.temp_dir) / "invalid.csv", index=False)

    def tearDown(self):
        """Nettoyage après les tests."""
        for file in Path(self.temp_dir).glob("*"):
            file.unlink()
        os.rmdir(self.temp_dir)

    def test_read_csv_files(self):
        """Test de la lecture des fichiers CSV."""
        df = FileHandler.read_csv_files(self.temp_dir)
        self.assertIsNotNone(df)
        self.assertEqual(len(df), 2)  # Seulement les données du fichier valide

    def test_read_nonexistent_directory(self):
        """Test de la lecture d'un répertoire inexistant."""
        df = FileHandler.read_csv_files("/nonexistent/directory")
        self.assertIsNone(df)

    def test_save_report(self):
        """Test de la sauvegarde d'un rapport."""
        test_data = pd.DataFrame(
            {"Métrique": ["Total", "Moyenne"], "Valeur": [100, 50]}
        )
        output_file = Path(self.temp_dir) / "report.csv"

        success = FileHandler.save_report(test_data, str(output_file))
        self.assertTrue(success)
        self.assertTrue(output_file.exists())

        # Vérification du contenu
        saved_data = pd.read_csv(output_file)
        self.assertEqual(len(saved_data), 2)
        self.assertEqual(list(saved_data.columns), ["Métrique", "Valeur"])


if __name__ == "__main__":
    unittest.main()
