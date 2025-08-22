# Utiliser l'image officielle Python comme base
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Définir les variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances système nécessaires et les dépendances Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY app/ ./app/

# Créer un utilisateur non-root pour exécuter l'application
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app \
    && chmod +x /app/app/main.py

# Basculer vers l'utilisateur non-root
USER appuser

# Exposer le port sur lequel l'application écoute
EXPOSE 8000

# Commande pour lancer l'application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]