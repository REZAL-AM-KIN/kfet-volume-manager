# ldap-flask-auth-example

# Objectifs
- Permettre aux futurs projets d'utiliser une authentificiation LDAP pour centralisé tous le processus d'authentification et de gestion des permissions à KIN
- Fournir une base de code permettant d'intégrer l'authentification LDAP dans des applications web python.

# Vues
- Index: page d'accueil
    - Accessible : tout utilisateur authentifié
- LoginPage : page de login
    - Accessible : tout le monde
    
# Installation

Installer les dépendances: 
```bash
pip install -r requirements.txt
```

Dupliquer le .envtemplate en .env et le compléter
## En développement:
Lancer le serveur flask avec
```bash
flask run
```

##En production:
Penser à passer les options de débug à False

Lancer le scipts run.py avec gunicorn:
```bash
gunicorn run:app
```
