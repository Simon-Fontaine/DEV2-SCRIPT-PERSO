import argparse
import sys
import logging
from pathlib import Path
import pandas as pd
from inventory_manager.core.manager import InventoryManager
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from typing import Optional

console = Console()


def setup_logging():
    """Configure le système de logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("inventory.log"), logging.StreamHandler()],
    )


def create_parser() -> argparse.ArgumentParser:
    """Crée et configure le parser d'arguments."""
    parser = argparse.ArgumentParser(
        description="Gestionnaire d'inventaire - Interface en ligne de commande",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Argument global pour le répertoire de données
    parser.add_argument(
        "--data-dir",
        "-d",
        default="./data",
        help="Répertoire contenant les fichiers CSV (défaut: ./data)",
    )

    # Sous-commandes
    subparsers = parser.add_subparsers(dest="command", help="Commandes disponibles")

    # Commande: list
    list_parser = subparsers.add_parser("list", help="Liste tous les produits")
    list_parser.add_argument(
        "--sort-by",
        choices=["name", "category", "quantity", "unit_price"],
        help="Trier les résultats par colonne",
    )
    list_parser.add_argument(
        "--desc", action="store_true", help="Trier par ordre décroissant"
    )

    # Commande: search
    search_parser = subparsers.add_parser("search", help="Rechercher des produits")
    search_parser.add_argument(
        "--name", "-n", help="Nom du produit (recherche partielle)"
    )
    search_parser.add_argument("--category", "-c", help="Catégorie du produit")
    search_parser.add_argument("--min-price", type=float, help="Prix minimum")
    search_parser.add_argument("--max-price", type=float, help="Prix maximum")
    search_parser.add_argument(
        "--low-stock",
        action="store_true",
        help="Afficher uniquement les produits en stock faible (<10)",
    )

    # Commande: report
    report_parser = subparsers.add_parser("report", help="Générer un rapport")
    report_parser.add_argument(
        "--output",
        "-o",
        default="report.csv",
        help="Fichier de sortie (défaut: report.csv)",
    )
    report_parser.add_argument(
        "--format",
        choices=["csv", "console"],
        default="csv",
        help="Format de sortie (défaut: csv)",
    )

    return parser


def display_results(df, title: Optional[str] = None):
    """Affiche les résultats dans un tableau formaté."""
    if df.empty:
        rprint("[yellow]Aucun résultat trouvé.[/yellow]")
        return

    table = Table(show_header=True, header_style="bold magenta")

    # Ajout des colonnes
    for col in df.columns:
        table.add_column(col)

    # Ajout des lignes
    for _, row in df.iterrows():
        table.add_row(*[str(val) for val in row])

    if title:
        rprint(f"\n[bold blue]{title}[/bold blue]")
    console.print(table)
    rprint(f"\nTotal: [green]{len(df)}[/green] produits")


def handle_list_command(manager: InventoryManager, args):
    """Gère la commande 'list'."""
    try:
        df = manager.inventory_df
        if args.sort_by:
            df = df.sort_values(by=args.sort_by, ascending=not args.desc)
        display_results(df, "Liste des produits")
    except Exception as e:
        rprint(f"[red]Erreur lors de l'affichage : {str(e)}[/red]")


def handle_search_command(manager: InventoryManager, args):
    """Gère la commande 'search'."""
    try:
        results = manager.search_products(
            name=args.name,
            category=args.category,
            min_price=args.min_price,
            max_price=args.max_price,
        )

        if args.low_stock:
            results = results[results["quantity"] < 10]

        display_results(results, "Résultats de la recherche")
    except Exception as e:
        rprint(f"[red]Erreur lors de la recherche : {str(e)}[/red]")


def handle_report_command(manager: InventoryManager, args):
    """Gère la commande 'report'."""
    try:
        # Générer le rapport
        manager.generate_report(args.output)

        if args.format == "csv":
            rprint(f"[green]Rapport généré avec succès : {args.output}[/green]")
        else:
            # Lire et afficher le rapport
            report_df = pd.read_csv(args.output)

            # Tableau pour les statistiques globales
            global_table = Table(show_header=True, header_style="bold magenta")
            global_table.add_column("Métrique")
            global_table.add_column("Valeur")

            # Filtrer les statistiques globales (celles qui ne commencent pas par une catégorie)
            global_stats = report_df[~report_df["Métrique"].str.contains(" - ")]
            for _, row in global_stats.iterrows():
                value = (
                    f"{row['Valeur']:,.2f}"
                    if isinstance(row["Valeur"], (int, float))
                    else str(row["Valeur"])
                )
                global_table.add_row(row["Métrique"], value)

            rprint("\n[bold blue]Statistiques Globales[/bold blue]")
            console.print(global_table)

            # Tableaux pour chaque catégorie
            categories = {
                s.split(" - ")[0] for s in report_df["Métrique"] if " - " in s
            }

            for category in categories:
                cat_table = Table(show_header=True, header_style="bold magenta")
                cat_table.add_column("Métrique")
                cat_table.add_column("Valeur")

                cat_stats = report_df[report_df["Métrique"].str.startswith(category)]
                for _, row in cat_stats.iterrows():
                    metric = row["Métrique"].split(" - ")[
                        1
                    ]  # Retirer le préfixe de la catégorie
                    value = (
                        f"{row['Valeur']:,.2f}"
                        if isinstance(row["Valeur"], (int, float))
                        else str(row["Valeur"])
                    )
                    cat_table.add_row(metric, value)

                rprint(f"\n[bold blue]Statistiques {category}[/bold blue]")
                console.print(cat_table)

    except Exception as e:
        rprint(f"[red]Erreur lors de la génération du rapport : {str(e)}[/red]")


def main():
    """Point d'entrée principal."""
    setup_logging()
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        # Vérification du répertoire de données
        data_dir = Path(args.data_dir)
        if not data_dir.exists():
            rprint(f"[red]Erreur : Le répertoire {args.data_dir} n'existe pas.[/red]")
            return 1

        # Initialisation du gestionnaire
        manager = InventoryManager(str(data_dir))
        manager.consolidate_files()

        # Exécution de la commande
        if args.command == "list":
            handle_list_command(manager, args)
        elif args.command == "search":
            handle_search_command(manager, args)
        elif args.command == "report":
            handle_report_command(manager, args)

        return 0

    except KeyboardInterrupt:
        rprint("\n[yellow]Opération annulée par l'utilisateur.[/yellow]")
        return 130
    except Exception as e:
        rprint(f"[red]Erreur inattendue : {str(e)}[/red]")
        logging.exception("Erreur inattendue")
        return 1


if __name__ == "__main__":
    sys.exit(main())
