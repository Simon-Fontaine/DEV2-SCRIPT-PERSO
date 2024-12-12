from typing import Optional
import pandas as pd
import logging
from ..utils.file_handler import FileHandler


class InventoryManager:
    """Gestionnaire principal de l'inventaire."""

    def __init__(self, data_directory: str):
        """
        Initialise le gestionnaire d'inventaire.

        Args:
            data_directory (str): Chemin vers le répertoire contenant les fichiers CSV
        """
        self.data_directory = data_directory
        self.inventory_df = None
        self.stock_threshold = 10
        self.setup_logging()

    def setup_logging(self) -> None:
        """Configure le système de logging."""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler("inventory.log"), logging.StreamHandler()],
        )

    def consolidate_files(self) -> None:
        """Consolide tous les fichiers CSV du répertoire."""
        self.inventory_df = FileHandler.read_csv_files(self.data_directory)
        if self.inventory_df is not None:
            self.inventory_df.drop_duplicates(
                subset=["name", "category"], keep="last", inplace=True
            )
        else:
            raise ValueError("Échec de la consolidation des fichiers")

    def set_stock_threshold(self, threshold: int) -> None:
        """
        Configure le seuil d'alerte pour le stock bas.

        Args:
            threshold (int): Nouveau seuil d'alerte

        Raises:
            ValueError: Si le seuil n'est pas un entier positif
            TypeError: Si le seuil n'est pas du bon type
        """
        try:
            threshold = int(threshold)
        except (TypeError, ValueError):
            raise ValueError("Le seuil doit être un nombre entier")

        if threshold < 0:
            raise ValueError("Le seuil doit être un entier positif")
        self.stock_threshold = threshold

    def get_low_stock_products(self) -> pd.DataFrame:
        """
        Retourne les produits dont le stock est inférieur au seuil.

        Returns:
            pd.DataFrame: DataFrame contenant les produits en stock bas
        """
        if self.inventory_df is None:
            raise ValueError("Base de données non initialisée")

        return self.inventory_df[
            self.inventory_df["quantity"] <= self.stock_threshold
        ].copy()

    def check_stock_alerts(self) -> list:
        """
        Vérifie et retourne les alertes de stock.

        Returns:
            list: Liste des alertes formatées
        """
        low_stock = self.get_low_stock_products()
        alerts = []

        for _, product in low_stock.iterrows():
            alert = (
                f"ALERTE: Stock bas pour {product['name']} "
                f"({product['quantity']} unités restantes, "
                f"seuil: {self.stock_threshold})"
            )
            alerts.append(alert)
            logging.warning(alert)

        return alerts

    def search_products(
        self,
        name: Optional[str] = None,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
    ) -> pd.DataFrame:
        """
        Recherche des produits selon différents critères.

        Args:
            name (str, optional): Nom du produit (recherche partielle)
            category (str, optional): Catégorie du produit
            min_price (float, optional): Prix minimum
            max_price (float, optional): Prix maximum

        Returns:
            pd.DataFrame: Résultats de la recherche
        """
        if self.inventory_df is None:
            raise ValueError("Base de données non initialisée")

        result = self.inventory_df.copy()

        if name:
            result = result[result["name"].str.contains(name, case=False, na=False)]
        if category:
            result = result[result["category"] == category]
        if min_price is not None:
            result = result[result["unit_price"] >= min_price]
        if max_price is not None:
            result = result[result["unit_price"] <= max_price]

        return result

    def generate_report(self, output_file: str) -> None:
        """
        Génère un rapport récapitulatif détaillé.

        Args:
            output_file (str): Chemin du fichier de sortie
        """
        if self.inventory_df is None:
            raise ValueError("Base de données non initialisée")

        # Statistiques globales
        global_stats = pd.DataFrame(
            [
                {
                    "Métrique": "Nombre total de produits",
                    "Valeur": len(self.inventory_df),
                },
                {
                    "Métrique": "Nombre de catégories",
                    "Valeur": self.inventory_df["category"].nunique(),
                },
                {
                    "Métrique": "Valeur totale du stock",
                    "Valeur": (
                        self.inventory_df["quantity"] * self.inventory_df["unit_price"]
                    ).sum(),
                },
                {
                    "Métrique": "Prix moyen",
                    "Valeur": self.inventory_df["unit_price"].mean(),
                },
                {
                    "Métrique": "Produits en stock faible (<10)",
                    "Valeur": len(
                        self.inventory_df[self.inventory_df["quantity"] < 10]
                    ),
                },
            ]
        )

        # Statistiques par catégorie
        category_stats = []
        for category in self.inventory_df["category"].unique():
            cat_df = self.inventory_df[self.inventory_df["category"] == category]
            category_stats.extend(
                [
                    {
                        "Métrique": f"{category} - Nombre de produits",
                        "Valeur": len(cat_df),
                    },
                    {
                        "Métrique": f"{category} - Valeur totale",
                        "Valeur": (cat_df["quantity"] * cat_df["unit_price"]).sum(),
                    },
                    {
                        "Métrique": f"{category} - Prix moyen",
                        "Valeur": cat_df["unit_price"].mean(),
                    },
                    {
                        "Métrique": f"{category} - Stock total",
                        "Valeur": cat_df["quantity"].sum(),
                    },
                ]
            )

        # Combiner les statistiques
        stats_df = pd.concat(
            [global_stats, pd.DataFrame(category_stats)], ignore_index=True
        )

        # Sauvegarder le rapport
        if not FileHandler.save_report(stats_df, output_file):
            raise Exception("Échec de la génération du rapport")
