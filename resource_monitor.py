#!/usr/bin/env python3
"""
Script pour surveiller les ressources système et temporiser si les seuils sont dépassés.
"""

import time
import os
import sys

try:
    import psutil
except ImportError:
    print("Error: psutil is not installed.")
    print("Please install it using: pip install psutil")
    print("Or run the installation script: /home/coder/install_throttler.sh")
    sys.exit(1)


def get_system_resources():
    """
    Obtenir l'utilisation du CPU et le load average.
    
    Returns:
        tuple: (cpu_percent, load_avg_5min)
    """
    cpu_percent = psutil.cpu_percent(interval=1)
    load_avg = os.getloadavg()
    load_avg_5min = load_avg[1]
    return cpu_percent, load_avg_5min


def wait_for_resources(cpu_threshold=90.0, load_avg_threshold=6.0, check_interval=5, max_wait_time=60):
    """
    Attendre que les ressources système soient en dessous des seuils.
    
    Args:
        cpu_threshold: Seuil d'utilisation CPU (en pourcentage).
        load_avg_threshold: Seuil de load average sur 5 minutes.
        check_interval: Intervalle de temps entre les vérifications (en secondes).
        max_wait_time: Temps d'attente maximum (en secondes).
    """
    start_time = time.time()
    print(f"Surveillance des ressources (seuils: CPU < {cpu_threshold}%, Load Avg 5min < {load_avg_threshold})")
    
    while True:
        cpu_percent, load_avg_5min = get_system_resources()
        print(f"  CPU: {cpu_percent:.2f}%, Load Avg (5min): {load_avg_5min:.2f}")
        
        # Si les ressources sont en dessous des seuils, on sort de la boucle
        if cpu_percent < cpu_threshold and load_avg_5min < load_avg_threshold:
            print("Ressources OK, continuation...")
            break
        
        # Si le temps d'attente maximum est dépassé, on sort de la boucle
        if time.time() - start_time > max_wait_time:
            print(f"Temps d'attente maximum dépassé. Ressources: CPU {cpu_percent:.2f}%, Load Avg (5min) {load_avg_5min:.2f}")
            break
        
        print(f"  Ressources élevées, attente de {check_interval} secondes...")
        time.sleep(check_interval)


def main():
    """Fonction principale."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Resource Monitor")
    parser.add_argument("--cpu-threshold", type=float, default=90.0, help="CPU threshold (default: 90.0)")
    parser.add_argument("--load-avg-threshold", type=float, default=6.0, help="Load average threshold (default: 6.0)")
    parser.add_argument("--check-interval", type=float, default=5, help="Check interval (default: 5)")
    parser.add_argument("--max-wait-time", type=float, default=60, help="Max wait time (default: 60)")
    parser.add_argument("--once", action="store_true", help="Check once and exit")
    args = parser.parse_args()
    
    if args.once:
        cpu_percent, load_avg_5min = get_system_resources()
        print(f"CPU: {cpu_percent:.2f}%, Load Avg (5min): {load_avg_5min:.2f}")
        if cpu_percent >= args.cpu_threshold or load_avg_5min >= args.load_avg_threshold:
            print("Seuils dépassés")
            sys.exit(1)
        else:
            print("Ressources OK")
            sys.exit(0)
    else:
        wait_for_resources(
            cpu_threshold=args.cpu_threshold,
            load_avg_threshold=args.load_avg_threshold,
            check_interval=args.check_interval,
            max_wait_time=args.max_wait_time
        )


if __name__ == "__main__":
    main()