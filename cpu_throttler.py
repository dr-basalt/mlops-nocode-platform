#!/usr/bin/env python3
"""
Script pour contrôler la charge CPU et le load average pour éviter de dépasser les seuils.
"""

import time
import psutil
import os
from typing import Optional

# Seuil d'utilisation CPU au-delà duquel on ralentit
CPU_THRESHOLD = 90.0

# Seuil de load average 5 minutes au-delà duquel on ralentit
LOAD_AVG_THRESHOLD = 6.0

# Intervalle de temps entre les vérifications (en secondes)
CHECK_INTERVAL = 0.1

# Temps d'attente maximum (en secondes) pour une seule vérification
MAX_WAIT_TIME = 5.0


def get_load_avg() -> float:
    """
    Obtenir le load average sur 5 minutes.
    
    Returns:
        Load average sur 5 minutes.
    """
    load_avg = os.getloadavg()
    return load_avg[1]  # load average sur 5 minutes


def wait_for_cpu_and_load_availability(
    cpu_threshold: float = CPU_THRESHOLD,
    load_avg_threshold: float = LOAD_AVG_THRESHOLD,
    check_interval: float = CHECK_INTERVAL,
    max_wait_time: float = MAX_WAIT_TIME,
    verbose: bool = False
) -> None:
    """
    Attend que l'utilisation du CPU et le load average soient en dessous des seuils spécifiés.

    Args:
        cpu_threshold: Seuil d'utilisation CPU (en pourcentage).
        load_avg_threshold: Seuil de load average sur 5 minutes.
        check_interval: Intervalle de temps entre les vérifications (en secondes).
        max_wait_time: Temps d'attente maximum (en secondes).
        verbose: Afficher des messages de debug.
    """
    start_time = time.time()
    while True:
        # Obtenir l'utilisation CPU
        cpu_percent = psutil.cpu_percent(interval=check_interval)
        
        # Obtenir le load average sur 5 minutes
        load_avg_5min = get_load_avg()
        
        # Si l'utilisation CPU et le load average sont en dessous des seuils, on sort de la boucle
        if cpu_percent < cpu_threshold and load_avg_5min < load_avg_threshold:
            if verbose:
                print(f"CPU usage: {cpu_percent:.2f}% - Load average (5min): {load_avg_5min:.2f} - Below thresholds")
            break
        
        # Si le temps d'attente maximum est dépassé, on sort de la boucle
        if time.time() - start_time > max_wait_time:
            if verbose:
                print(f"Max wait time exceeded. CPU usage: {cpu_percent:.2f}% - Load average (5min): {load_avg_5min:.2f}")
            break
        
        if verbose:
            print(f"CPU usage: {cpu_percent:.2f}% - Load average (5min): {load_avg_5min:.2f} - Waiting...")


def throttle_operation(
    operation,
    *args,
    cpu_threshold: float = CPU_THRESHOLD,
    load_avg_threshold: float = LOAD_AVG_THRESHOLD,
    check_interval: float = CHECK_INTERVAL,
    max_wait_time: float = MAX_WAIT_TIME,
    verbose: bool = False,
    **kwargs
):
    """
    Exécute une opération après avoir attendu que l'utilisation du CPU et le load average soient en dessous des seuils.

    Args:
        operation: Fonction à exécuter.
        *args: Arguments positionnels pour la fonction.
        cpu_threshold: Seuil d'utilisation CPU (en pourcentage).
        load_avg_threshold: Seuil de load average sur 5 minutes.
        check_interval: Intervalle de temps entre les vérifications (en secondes).
        max_wait_time: Temps d'attente maximum (en secondes).
        verbose: Afficher des messages de debug.
        **kwargs: Arguments nommés pour la fonction.

    Returns:
        Résultat de l'opération.
    """
    wait_for_cpu_and_load_availability(cpu_threshold, load_avg_threshold, check_interval, max_wait_time, verbose)
    return operation(*args, **kwargs)


# Exemple d'utilisation
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="CPU and Load Average Throttler")
    parser.add_argument("--cpu-threshold", type=float, default=CPU_THRESHOLD, help="CPU threshold (default: 90.0)")
    parser.add_argument("--load-avg-threshold", type=float, default=LOAD_AVG_THRESHOLD, help="Load average threshold (default: 6.0)")
    parser.add_argument("--check-interval", type=float, default=CHECK_INTERVAL, help="Check interval (default: 0.1)")
    parser.add_argument("--max-wait-time", type=float, default=MAX_WAIT_TIME, help="Max wait time (default: 5.0)")
    parser.add_argument("--verbose", action="store_true", help="Verbose mode")
    args = parser.parse_args()

    print("Monitoring CPU usage and load average...")
    try:
        while True:
            wait_for_cpu_and_load_availability(
                cpu_threshold=args.cpu_threshold,
                load_avg_threshold=args.load_avg_threshold,
                check_interval=args.check_interval,
                max_wait_time=args.max_wait_time,
                verbose=args.verbose
            )
            time.sleep(1)  # Attendre 1 seconde avant la prochaine vérification
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")