# CPU Throttler

## Description

Ce projet contient un script Python pour contrôler la charge CPU et éviter de dépasser 90% d'utilisation. Cela permet d'éviter d'être limité par l'hébergeur pendant le développement.

## Fichiers

- `cpu_throttler.py` : Script principal pour le contrôle de la charge CPU.
- `requirements.txt` : Dépendances nécessaires.

## Installation

1.  Installer les dépendances :

    ```bash
    pip install -r requirements.txt
    ```

## Utilisation

### En tant que script autonome

Pour surveiller l'utilisation du CPU en continu :

```bash
python cpu_throttler.py
```

Options disponibles :

- `--threshold` : Seuil d'utilisation CPU (par défaut 90.0).
- `--check-interval` : Intervalle de temps entre les vérifications (par défaut 0.1).
- `--max-wait-time` : Temps d'attente maximum (par défaut 5.0).
- `--verbose` : Mode verbeux.

Exemple :

```bash
python cpu_throttler.py --threshold 85.0 --verbose
```

### En tant que module

Pour utiliser le limiteur de CPU dans vos propres scripts :

```python
from cpu_throttler import wait_for_cpu_availability, throttle_operation

# Attendre que l'utilisation du CPU soit en dessous de 90%
wait_for_cpu_availability(threshold=90.0, verbose=True)

# Exécuter une opération avec throttling
def my_operation(x, y):
    # Opération intensive en CPU
    return x * y

result = throttle_operation(my_operation, 10, 20, threshold=85.0, verbose=True)
```

## Configuration

Les paramètres par défaut sont définis dans le script :

- `CPU_THRESHOLD` : 90.0 (seuil d'utilisation CPU)
- `CHECK_INTERVAL` : 0.1 (intervalle de vérification en secondes)
- `MAX_WAIT_TIME` : 5.0 (temps d'attente maximum en secondes)

Ces valeurs peuvent être modifiées directement dans le script ou passées en arguments lors de l'appel.

## TODO

- Ajouter la possibilité de configurer les paramètres via des variables d'environnement.
- Implémenter un mécanisme de logging.
- Ajouter des tests unitaires.
