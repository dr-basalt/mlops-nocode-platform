# CPU and Load Average Throttler

## Description

Ce projet contient un script Python pour contrôler la charge CPU et le load average pour éviter de dépasser les seuils définis. Cela permet d'éviter d'être limité par l'hébergeur pendant le développement.

Le throttling peut être désactivé via la variable d'environnement `THROTTLE_DISABLE` pour les environnements de production.

## Fichiers

- `cpu_throttler.py` : Script principal pour le contrôle de la charge CPU et du load average.
- `install_throttler.sh` : Script pour installer les dépendances dans un environnement virtuel et configurer l'environnement.

## Installation

### Méthode recommandée: Script d'installation automatique avec environnement virtuel

Exécutez le script d'installation :

```bash
chmod +x /home/coder/install_throttler.sh
/home/coder/install_throttler.sh
```

Ce script :
1. Crée un environnement virtuel dans `$HOME/throttler-venv`.
2. Installe `psutil` dans cet environnement.
3. Configure des alias `throttle-on`, `throttle-off` et `throttle-run` dans `~/.bashrc`.
4. Crée un script wrapper `throttle-wrapper.sh` pour exécuter des commandes avec throttling.
5. Active le throttling par défaut.

### Méthode 2: Installation manuelle avec environnement virtuel

1.  Créer un environnement virtuel :

    ```bash
    python3 -m venv $HOME/throttler-venv
    ```

2.  Activer l'environnement virtuel :

    ```bash
    source $HOME/throttler-venv/bin/activate
    ```

3.  Installer `psutil` :

    ```bash
    pip install psutil
    ```

4.  Copier `cpu_throttler.py` dans l'environnement virtuel ou s'assurer que le chemin est correct.

## Utilisation

### En tant que script autonome

Pour surveiller l'utilisation du CPU et le load average en continu :

```bash
# Si vous avez exécuté le script d'installation
throttle-run

# Ou directement
$HOME/throttler-venv/bin/python $HOME/throttler-venv/bin/cpu_throttler.py
```

Options disponibles :

- `--cpu-threshold` : Seuil d'utilisation CPU (par défaut 90.0).
- `--load-avg-threshold` : Seuil de load average sur 5 minutes (par défaut 6.0).
- `--check-interval` : Intervalle de temps entre les vérifications (par défaut 0.1).
- `--max-wait-time` : Temps d'attente maximum (par défaut 5.0).
- `--verbose` : Mode verbeux.

Exemple :

```bash
throttle-run --cpu-threshold 85.0 --load-avg-threshold 5.0 --verbose
```

### En tant que module

Pour utiliser le limiteur de CPU et de load average dans vos propres scripts, vous devez d'abord activer l'environnement virtuel :

```bash
source $HOME/throttler-venv/bin/activate
```

Puis dans votre script Python :

```python
import sys
import os

# Ajouter le chemin de l'environnement virtuel au sys.path si nécessaire
sys.path.insert(0, os.path.join(os.environ['HOME'], 'throttler-venv', 'bin'))

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

Avec le script d'installation, vous pouvez aussi utiliser les alias :

```bash
throttle-off  # Désactive le throttling
throttle-on   # Active le throttling
```

### Exécuter une commande avec throttling

Pour exécuter une commande avec vérification préalable des ressources :

```bash
$HOME/throttler-venv/bin/throttle-wrapper.sh python3 votre_script.py
```

## Configuration

Les paramètres par défaut sont définis dans le script, mais peuvent être configurés via des variables d'environnement :

- `CPU_THRESHOLD` : Seuil d'utilisation CPU (par défaut 90.0).
- `LOAD_AVG_THRESHOLD` : Seuil de load average sur 5 minutes (par défaut 6.0).
- `CHECK_INTERVAL` : Intervalle de temps entre les vérifications (par défaut 0.1).
- `MAX_WAIT_TIME` : Temps d'attente maximum (par défaut 5.0).
- `THROTTLE_DISABLE` : Désactiver le throttling (par défaut false).
- `LOG_LEVEL` : Niveau de logging (par défaut INFO).

Exemple :

```bash
export CPU_THRESHOLD=85.0
export LOAD_AVG_THRESHOLD=5.0
export LOG_LEVEL=DEBUG
throttle-run
```

## Logging

Le script utilise le module `logging` de Python pour afficher des messages d'information et de débogage. Le niveau de logging peut être configuré via la variable d'environnement `LOG_LEVEL`.

## TODO

- Ajouter des tests unitaires.
