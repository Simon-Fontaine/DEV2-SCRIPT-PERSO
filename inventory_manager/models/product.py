from dataclasses import dataclass
from typing import Dict, Any
from decimal import Decimal


class ProductValidationError(Exception):
    """Exception personnalisée pour les erreurs de validation des produits."""

    pass


@dataclass
class Product:
    """Classe représentant un produit dans l'inventaire."""

    name: str
    quantity: int
    unit_price: float
    category: str

    def __post_init__(self):
        """Validation après initialisation."""
        self._validate()

    def _validate(self) -> None:
        """
        Valide les attributs du produit.

        Raises:
            ProductValidationError: Si les valeurs ne sont pas valides
            TypeError: Si les types ne sont pas corrects
        """
        # Validation des types
        if not isinstance(self.name, str):
            raise TypeError("Le nom doit être une chaîne de caractères")
        if not isinstance(self.quantity, int):
            raise TypeError("La quantité doit être un entier")
        if not isinstance(self.unit_price, (int, float)):
            raise TypeError("Le prix unitaire doit être un nombre")
        if not isinstance(self.category, str):
            raise TypeError("La catégorie doit être une chaîne de caractères")

        # Validation des valeurs
        if not self.name.strip():
            raise ProductValidationError("Le nom ne peut pas être vide")
        if self.quantity < 0:
            raise ProductValidationError("La quantité ne peut pas être négative")
        if self.unit_price < 0:
            raise ProductValidationError("Le prix unitaire ne peut pas être négatif")
        if not self.category.strip():
            raise ProductValidationError("La catégorie ne peut pas être vide")

        # Nettoyage des chaînes
        self.name = self.name.strip()
        self.category = self.category.strip()

        # Arrondir le prix à 2 décimales
        self.unit_price = round(float(self.unit_price), 2)

    def to_dict(self) -> Dict[str, Any]:
        """Convertit le produit en dictionnaire."""
        return {
            "name": self.name,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "category": self.category,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Product":
        """
        Crée une instance de Product à partir d'un dictionnaire.

        Args:
            data: Dictionnaire contenant les données du produit

        Raises:
            KeyError: Si des clés requises sont manquantes
            TypeError: Si les types ne sont pas corrects
            ProductValidationError: Si les valeurs ne sont pas valides
        """
        required_keys = {"name", "quantity", "unit_price", "category"}
        missing_keys = required_keys - set(data.keys())
        if missing_keys:
            raise KeyError(f"Clés manquantes : {missing_keys}")

        try:
            # Conversion explicite des types
            quantity = int(data["quantity"])
            unit_price = float(data["unit_price"])

            return cls(
                name=str(data["name"]),
                quantity=quantity,
                unit_price=unit_price,
                category=str(data["category"]),
            )
        except ValueError as e:
            raise TypeError(f"Erreur de conversion de type : {str(e)}")
