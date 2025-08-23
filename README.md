# CPU and Load Average Throttler

## Description

Ce projet contient un script Python pour contrôler la charge CPU et le load average pour éviter de dépasser les seuils définis. Cela permet d'éviter d'être limité par l'hébergeur pendant le développement.

Le throttling peut être désactivé via la variable d'environnement `THROTTLE_DISABLE` pour les environnements de production.

## Fichiers

- `cpu_throttler.py` : Script principal pour le contrôle de la charge CPU et du load average.
- `requirements.txt` : Dépendances nécessaires.

## Installation

1.  Installer les dépendances :

    ```bash
    pip install -r requirements.txt
    ```

## Utilisation

### En tant que script autonome

Pour surveiller l'utilisation du CPU et le load average en continu :

```bash
python cpu_throttler.py
```

Options disponibles :

- `--cpu-threshold` : Seuil d'utilisation CPU (par défaut 90.0).
- `--load-avg-threshold` : Seuil de load average sur 5 minutes (par défaut 6.0).
- `--check-interval` : Intervalle de temps entre les vérifications (par défaut 0.1).
- `--max-wait-time` : Temps d'attente maximum (par défaut 5.0).
- `--verbose` : Mode verbeux.

Exemple :

```bash
python cpu_throttler.py --cpu-threshold 85.0 --load-avg-threshold 5.0 --verbose
```

### En tant que module

Pour utiliser le limiteur de CPU et de load average dans vos propres scripts :

```python
from cpu_throttler import wait_for_cpu_and_load_availability, throttle_operation

# Attendre que l'utilisation du CPU et le load average soient en dessous des seuils
wait_for_cpu_and_load_availability(cpu_threshold=90.0, load_avg_threshold=6.0, verbose=True)

# Exécuter une opération avec throttling
def my_operation(x, y):
    # Opération intensive en CPU
    return x * y

result = throttle_operation(my_operation, 10, 20, cpu_threshold=85.0, load_avg_threshold=5.0, verbose=True)
```

### Désactiver le throttling

Pour désactiver le throttling (par exemple, dans un environnement de production), définissez la variable d'environnement `THROTTLE_DISABLE` à `true` :

```bash
export THROTTLE_DISABLE=true
python votre_script.py
```

Ou directement dans la commande :

```bash
THROTTLE_DISABLE=true python votre_script.py
```

## Configuration

Les paramètres par défaut sont définis dans le script :

- `CPU_THRESHOLD` : 90.0 (seuil d'utilisation CPU)
- `LOAD_AVG_THRESHOLD` : 6.0 (seuil de load average sur 5 minutes)
- `CHECK_INTERVAL` : 0.1 (intervalle de vérification en secondes)
- `MAX_WAIT_TIME` : 5.0 (temps d'attente maximum en secondes)
- `THROTTLE_DISABLE` : false (le throttling est activé par défaut)

Ces valeurs peuvent être modifiées directement dans le script ou passées en arguments lors de l'appel.

## TODO

- Ajouter la possibilité de configurer les paramètres via des variables d'environnement.
- Implémenter un mécanisme de logging.
- Ajouter des tests unitaires.
