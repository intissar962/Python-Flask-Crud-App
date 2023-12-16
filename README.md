Application : un annuaire téléphonique permettant de gérer des contacts

Frameworks utilisées: Flask, SQLAlchemy, HTML, Javascript et Bootstrap pour l'interface utilisateur.

- Flask pour créer une application web.
- Les templates utilisent le moteur de template Jinja2 pour générer des pages HTML dynamiques. On voit cela dans les fichiers index.html, base.html, header.html, et footer.html.
- SQLAlchemy pour la gestion de la base de données SQLite.
- Les routes permettent d'afficher, ajouter, modifier, supprimer et rechercher des contacts.
- Inclut également une fonctionnalité d'export en JSON des contacts.

Actions:

1. Ajout de Contacts
   Permet l'ajout de nouveaux contacts via un formulaire modal.

2. Modification de Contacts

   Permet la modification des contacts existants via un formulaire modal.

3. Suppression de Contacts

   Permet la suppression de contacts avec confirmation.

4. Recherche de Contacts

   Permet la recherche de contacts en fonction du nom ou du numéro de téléphone.

5. Export en JSON

   Permet d'exporter tous les contacts au format JSON.

6. Pagination

   Pagination la liste des contacts pour une meilleure expérience utilisateur.
