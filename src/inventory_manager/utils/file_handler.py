import pandas as pd
from pathlib import Path
from typing import Optional
import logging


class FileHandler:
    """Gestionnaire de fichiers pour l'inventaire."""

    @staticmethod
    def read_csv_files(directory: str) -> Optional[pd.DataFrame]:
        """
        Lit tous les fichiers CSV d'un répertoire.

        Args:
            directory (str): Chemin vers le répertoire contenant les fichiers CSV

        Returns:
            Optional[pd.DataFrame]: DataFrame consolidé ou None si erreur
        """
        data_dir = Path(directory)
        all_data = []

        try:
            csv_files = list(data_dir.glob("*.csv"))
            if not csv_files:
                raise FileNotFoundError(f"Aucun fichier CSV trouvé dans {directory}")

            for file_path in csv_files:
                try:
                    df = pd.read_csv(file_path)
                    required_columns = {"name", "quantity", "unit_price", "category"}

                    if not required_columns.issubset(df.columns):
                        logging.warning(f"Colonnes manquantes dans {file_path}")
                        continue

                    all_data.append(df)
                    logging.info(f"Fichier {file_path} traité avec succès")

                except Exception as e:
                    logging.error(f"Erreur lors du traitement de {file_path}: {str(e)}")
                    continue

            if all_data:
                return pd.concat(all_data, ignore_index=True)
            return None

        except Exception as e:
            logging.error(f"Erreur lors de la lecture des fichiers: {str(e)}")
            return None

    @staticmethod
    def save_report(data: pd.DataFrame, output_file: str) -> bool:
        """
        Sauvegarde un rapport au format CSV.

        Args:
            data (pd.DataFrame): Données à sauvegarder
            output_file (str): Chemin du fichier de sortie

        Returns:
            bool: True si succès, False sinon
        """
        try:
            data.to_csv(output_file, index=False)
            logging.info(f"Rapport sauvegardé avec succès: {output_file}")
            return True
        except Exception as e:
            logging.error(f"Erreur lors de la sauvegarde du rapport: {str(e)}")
            return False
