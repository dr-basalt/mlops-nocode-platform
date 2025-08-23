# Exemple de déploiement de LiteLLM

## Description

Cet exemple montre comment déployer LiteLLM sur un cluster Kubernetes.

## Fichiers

- `deployment.yaml` : Déploiement de l'application LiteLLM.
- `service.yaml` : Service pour exposer l'application LiteLLM.
- `configmap.yaml` : Configuration de l'application LiteLLM.
- `secret.yaml` : Clés secrètes pour l'application LiteLLM.

## Déploiement

1.  **Créer les ressources :**

    ```bash
    kubectl apply -f k8s/manifests/litellm/
    ```

2.  **Vérifier le déploiement :**

    ```bash
    kubectl get pods -l app=litellm-proxy
    kubectl get services -l app=litellm-proxy
    ```

3.  **Accéder à l'application :**

    Si vous avez configuré un LoadBalancer, vous pouvez accéder à l'application via l'IP externe du service :

    ```bash
    kubectl get services litellm-proxy-service
    ```

    Sinon, vous pouvez utiliser `port-forward` pour accéder à l'application localement :

    ```bash
    kubectl port-forward deployment/litellm-proxy 4000:4000
    ```

    L'application sera alors accessible à l'adresse `http://localhost:4000`.

## Configuration

-   **Clés API :** Remplacez les clés API dans `configmap.yaml` et `secret.yaml` par vos propres clés.
-   **Modèles :** Ajoutez ou supprimez des modèles dans `configmap.yaml` selon vos besoins.
-   **Ressources :** Ajustez les ressources (CPU, mémoire) dans `deployment.yaml` selon vos besoins.

## Nettoyage

Pour supprimer les ressources créées :

```bash
kubectl delete -f k8s/manifests/litellm/