#!/usr/bin/env python3
"""
Script pour contrôler la charge CPU et éviter de dépasser 90% d'utilisation.
"""

import time
import psutil
from typing import Optional

# Seuil d'utilisation CPU au-delà duquel on ralentit
CPU_THRESHOLD = 90.0

# Intervalle de temps entre les vérifications (en secondes)
CHECK_INTERVAL = 0.1

# Temps d'attente maximum (en secondes) pour une seule vérification
MAX_WAIT_TIME = 5.0


def wait_for_cpu_availability(
    threshold: float = CPU_THRESHOLD,
    check_interval: float = CHECK_INTERVAL,
    max_wait_time: float = MAX_WAIT_TIME,
    verbose: bool = False
) -> None:
    """
    Attend que l'utilisation du CPU soit en dessous du seuil spécifié.

    Args:
        threshold: Seuil d'utilisation CPU (en pourcentage).
        check_interval: Intervalle de temps entre les vérifications (en secondes).
        max_wait_time: Temps d'attente maximum (en secondes).
        verbose: Afficher des messages de debug.
    """
    start_time = time.time()
    while True:
        # Obtenir l'utilisation CPU
        cpu_percent = psutil.cpu_percent(interval=check_interval)
        
        # Si l'utilisation CPU est en dessous du seuil, on sort de la boucle
        if cpu_percent < threshold:
            if verbose:
                print(f"CPU usage: {cpu_percent:.2f}% - Below threshold ({threshold}%)")
            break
        
        # Si le temps d'attente maximum est dépassé, on sort de la boucle
        if time.time() - start_time > max_wait_time:
            if verbose:
                print(f"Max wait time exceeded. CPU usage: {cpu_percent:.2f}%")
            break
        
        if verbose:
            print(f"CPU usage: {cpu_percent:.2f}% - Waiting...")


def throttle_operation(
    operation,
    *args,
    threshold: float = CPU_THRESHOLD,
    check_interval: float = CHECK_INTERVAL,
    max_wait_time: float = MAX_WAIT_TIME,
    verbose: bool = False,
    **kwargs
):
    """
    Exécute une opération après avoir attendu que l'utilisation du CPU soit en dessous du seuil.

    Args:
        operation: Fonction à exécuter.
        *args: Arguments positionnels pour la fonction.
        threshold: Seuil d'utilisation CPU (en pourcentage).
        check_interval: Intervalle de temps entre les vérifications (en secondes).
        max_wait_time: Temps d'attente maximum (en secondes).
        verbose: Afficher des messages de debug.
        **kwargs: Arguments nommés pour la fonction.

    Returns:
        Résultat de l'opération.
    """
    wait_for_cpu_availability(threshold, check_interval, max_wait_time, verbose)
    return operation(*args, **kwargs)


# Exemple d'utilisation
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="CPU Throttler")
    parser.add_argument("--threshold", type=float, default=CPU_THRESHOLD, help="CPU threshold (default: 90.0)")
    parser.add_argument("--check-interval", type=float, default=CHECK_INTERVAL, help="Check interval (default: 0.1)")
    parser.add_argument("--max-wait-time", type=float, default=MAX_WAIT_TIME, help="Max wait time (default: 5.0)")
    parser.add_argument("--verbose", action="store_true", help="Verbose mode")
    args = parser.parse_args()

    print("Monitoring CPU usage...")
    try:
        while True:
            wait_for_cpu_availability(
                threshold=args.threshold,
                check_interval=args.check_interval,
                max_wait_time=args.max_wait_time,
                verbose=args.verbose
            )
            time.sleep(1)  # Attendre 1 seconde avant la prochaine vérification
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")