# shared/display_utils.py
"""
A collection of utility functions for displaying formatted output in the console.

This module provides reusable tools to render data, such as lists and interactive menus,
in a clean and consistent way throughout the command-line interface (CLI)
of the application.
"""

from typing import List, Dict, Any

def print_formatted_list(
    title: str,
    items: List[str],
    indent_level: int = 2,
    bullet_char: str = "-",
    empty_message: str = "Nenhum item encontrado para exibir."
) -> None:

    print(f"\n--- {title.upper()} ---")

    # Lida com o caso de a lista ser vazia para uma melhor experiência do usuário
    if not items:
        print(f"{' ' * indent_level}{empty_message}")
        return

    # Prepara a string de indentação uma vez para ser mais eficiente
    indent_space = " " * indent_level

    # Itera sobre os itens e imprime cada um com o formato especificado
    for item in items:
        print(f"{indent_space}{bullet_char} {item}")
