# CI/CD - Déploiement Docker

## Fonctionnement du pipeline

Le pipeline CI/CD est réalisé avec **GitHub Actions**.

Lorsqu'une modification est poussée sur la branche `main`, le pipeline :

1. Récupère le code source.
2. Installe Python et exécute les tests avec `pytest`.
3. Construit l'image Docker.
4. Lance un conteneur et vérifie que l'endpoint `/health` retourne HTTP 200.
5. Se connecte à Docker Hub.
6. Publie l'image avec deux tags :

   * `latest` pour la dernière version.
   * le SHA du commit pour identifier précisément la version du code.
7. Déploie l'image sur la VM Azure.

Le pipeline s'arrête si les tests ou le contrôle de santé échouent.

## Déclenchement du déploiement

Le déploiement est déclenché automatiquement lors d'un `push` sur la branche `main`.

Le job de déploiement dépend de la réussite des tests et de la publication de l'image Docker.

Sur la VM Azure, l'image est récupérée depuis Docker Hub, puis le conteneur existant est arrêté et remplacé par la nouvelle version.

L'application est ensuite vérifiée avec l'endpoint `/health`.

## Démarrage en local

### Prérequis

* Python 3.12
* Docker
* Git

### Lancer l'application avec Python

Installer les dépendances :

```bash
pip install -r requirements.txt
```

Lancer l'application :

```bash
python app.py
```

L'API est disponible sur :

```text
http://localhost:8000
```

Tester l'API :

```bash
curl http://localhost:8000/health
```

## Utilisation de Docker

### Construire l'image

Depuis la racine du projet :

```bash
docker build -t my-api .
```

### Lancer le conteneur

```bash
docker run -d --name my-api -p 8000:8000 my-api
```

Tester l'application :

```bash
curl http://localhost:8000/health
```

### Arrêter et supprimer le conteneur

```bash
docker stop my-api
docker rm my-api
```

## Publier l'image sur Docker Hub

Se connecter à Docker Hub :

```bash
docker login
```

Construire l'image avec le nom du dépôt Docker Hub :

```bash
docker build -t <DOCKERHUB_USERNAME>/my-api:latest .
```

Publier l'image :

```bash
docker push <DOCKERHUB_USERNAME>/my-api:latest
```

L'image peut ensuite être récupérée avec :

```bash
docker pull <DOCKERHUB_USERNAME>/my-api:latest
```

et lancée avec :

```bash
docker run -d --name my-api -p 8000:8000 <DOCKERHUB_USERNAME>/my-api:latest
```

## Déploiement sur Azure

Le déploiement sur la VM Azure est effectué automatiquement par GitHub Actions après un `push` sur `main`.

L'image Docker est récupérée depuis Docker Hub puis lancée sur la VM avec le port attribué.

Pour vérifier manuellement l'application sur la VM :

```bash
curl http://<IP_VM>:<PORT>/health
```

Dans l'environnement utilisé pour ce projet, le port attribué est `8031` :

```bash
curl http://40.66.52.118:8031/health
```

## Choix techniques

* **GitHub Actions** : automatisation du processus CI/CD.
* **Docker** : création et exécution de l'application dans un environnement isolé.
* **Docker Hub** : stockage et distribution de l'image Docker.
* **Pytest** : exécution automatique des tests.
* **Endpoint `/health`** : vérification du bon fonctionnement de l'application.
* **Tag `latest`** : accès à la dernière version.
* **Tag avec le SHA du commit** : identification précise de la version du code.
* **Azure VM** : hébergement de l'application.
* **Port 8000** : port utilisé par l'application dans le conteneur.
* **Port 8031** : port exposé par la VM Azure pour accéder à l'application.
