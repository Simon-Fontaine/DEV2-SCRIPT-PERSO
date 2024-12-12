from dataclasses import dataclass
from typing import Dict


@dataclass
class Product:
    """Classe représentant un produit dans l'inventaire."""

    name: str
    quantity: int
    unit_price: float
    category: str

    def to_dict(self) -> Dict:
        """Convertit le produit en dictionnaire."""
        return {
            "name": self.name,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "category": self.category,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Product":
        """Crée une instance de Product à partir d'un dictionnaire."""
        return cls(
            name=data["name"],
            quantity=data["quantity"],
            unit_price=data["unit_price"],
            category=data["category"],
        )
