# Script de test pour Windmill
# Auteur: dr-basalt
# Date: 2025-08-22

def main(name: str = "World") -> str:
    """
    Fonction principale du script de test.
    
    Args:
        name (str): Nom à saluer. Par défaut "World".
        
    Returns:
        str: Message de salutation.
    """
    return f"Hello, {name}! This is a test script running in Windmill."

# Exemple d'utilisation avec des paramètres
def greet_with_time(name: str, time_of_day: str) -> str:
    """
    Salue une personne en fonction de la période de la journée.
    
    Args:
        name (str): Nom de la personne.
        time_of_day (str): Période de la journée ("morning", "afternoon", "evening").
        
    Returns:
        str: Message de salutation.
    """
    greetings = {
        "morning": "Good morning",
        "afternoon": "Good afternoon",
        "evening": "Good evening"
    }
    
    greeting = greetings.get(time_of_day.lower(), "Hello")
    return f"{greeting}, {name}!"

# Exemple d'utilisation avec des opérations mathématiques
def calculate_sum(a: int, b: int) -> int:
    """
    Calcule la somme de deux nombres.
    
    Args:
        a (int): Premier nombre.
        b (int): Deuxième nombre.
        
    Returns:
        int: Somme des deux nombres.
    """
    return a + b

# Exemple d'utilisation avec des listes
def process_list(items: list) -> dict:
    """
    Traite une liste d'éléments.
    
    Args:
        items (list): Liste d'éléments.
        
    Returns:
        dict: Dictionnaire contenant des informations sur la liste.
    """
    return {
        "count": len(items),
        "unique_items": list(set(items)),
        "reversed": items[::-1]
    }

# Point d'entrée pour les tests
if __name__ == "__main__":
    # Exécuter quelques tests simples
    print(main())
    print(main("Alice"))
    print(greet_with_time("Bob", "morning"))
    print(calculate_sum(5, 3))
    print(process_list([1, 2, 2, 3, 4, 4, 5]))