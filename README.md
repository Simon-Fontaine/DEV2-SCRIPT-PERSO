# Gestionnaire d'Inventaire

Application en ligne de commande pour gérer et analyser des données d'inventaire à partir de fichiers CSV.

## Installation

```bash
git clone <repo>
cd <repo>
make install  # Crée l'environnement virtuel et installe les dépendances
```

## Commandes

1. **Liste des produits**

```bash
python main.py list [--sort-by name|category|quantity|unit_price] [--desc]
```

2. **Recherche**

```bash
python main.py search [--name NOM] [--category CAT] [--min-price PRIX] [--max-price PRIX] [--low-stock]
```

3. **Rapport**

```bash
python main.py report [--output rapport.csv] [--format csv|console]
```

## Tests

```bash
make test         # Lance les tests
make coverage     # Génère un rapport de couverture
```

## Structure des fichiers CSV

```csv
name,quantity,unit_price,category
Product,10,99.99,Category
```

## Technologies

- Python 3.x
- pandas
- pytest
- rich (CLI)
