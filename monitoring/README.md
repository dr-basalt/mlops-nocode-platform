# Monitoring avec Prometheus et Grafana

## Description

Ce dossier contient les fichiers de configuration pour déployer Prometheus et Grafana sur un cluster Kubernetes. Ces outils permettent de surveiller les déploiements ML.

## Structure

- `prometheus/` : Fichiers de configuration pour Prometheus.
- `grafana/` : Fichiers de configuration pour Grafana.
- `grafana/dashboards/` : Dashboards Grafana.

## Déploiement

1.  **Créer les ressources :**

    ```bash
    kubectl apply -f monitoring/prometheus/
    kubectl apply -f monitoring/grafana/
    ```

2.  **Vérifier le déploiement :**

    ```bash
    kubectl get pods -l app=prometheus
    kubectl get pods -l app=grafana
    kubectl get services -l app=prometheus
    kubectl get services -l app=grafana
    ```

3.  **Accéder aux interfaces :**

    Si vous avez configuré un LoadBalancer, vous pouvez accéder aux interfaces via les IP externes des services :

    ```bash
    kubectl get services prometheus-service
    kubectl get services grafana-service
    ```

    Sinon, vous pouvez utiliser `port-forward` pour accéder aux interfaces localement :

    ```bash
    kubectl port-forward deployment/prometheus 9090:9090
    kubectl port-forward deployment/grafana 3000:3000
    ```

    - Prometheus sera alors accessible à l adresse http://localhost:9090.
    - Grafana sera alors accessible à l adresse http://localhost:3000.

## Configuration

-   **Prometheus :** Le fichier `prometheus.yml` dans `monitoring/prometheus/configmap.yaml` définit les cibles à scraper.
-   **Grafana :** Le fichier `grafana.ini` dans `monitoring/grafana/configmap.yaml` définit la configuration de Grafana. Le fichier `provisioning-datasources.yaml` configure Prometheus comme source de données par défaut.

## Dashboards

-   `ml-deployment-dashboard.json` : Dashboard pour surveiller les déploiements ML.

## Nettoyage

Pour supprimer les ressources créées :

```bash
kubectl delete -f monitoring/grafana/
kubectl delete -f monitoring/prometheus/
```
