# 🚀 Sama Jokoo - Application Sociale pour Odoo 18 CE

## 📱 Vue d'ensemble

**Sama Jokoo** transforme Odoo 18 CE en une plateforme sociale complète, intégrant parfaitement les fonctionnalités sociales avec les processus métier d'Odoo. Cette solution combine le meilleur du **FlutterSocialAppUIKit** pour l'interface mobile avec un backend Odoo robuste.

### ✨ Fonctionnalités Principales

- 📱 **Feed Social** : Posts avec texte, images, vidéos
- 💬 **Discussions** : Commentaires sur tous les dossiers Odoo
- 🎥 **Visioconférences** : Intégration avec les calendriers
- 🔔 **Notifications** : Système de notifications en temps réel
- 👥 **Réseau Social** : Suivis, abonnés, mentions
- 🏷️ **Hashtags** : Organisation et découverte de contenu
- 🌙 **Thèmes** : Support mode sombre/clair
- 📱 **Mobile First** : Application Flutter native

## 🏗️ Architecture

### Backend Odoo
```
sama_jokoo/
├── models/           # Modèles de données
│   ├── social_post.py
│   ├── social_comment.py
│   ├── social_like.py
│   ├── social_follow.py
│   ├── social_notification.py
│   ├── social_media.py
│   ├── social_hashtag.py
│   ├── res_users.py
│   └── mail_thread.py
├── controllers/      # API REST
│   ├── api_auth.py
│   ├── api_social.py
│   ├── api_discuss.py
│   └── api_notification.py
├── security/         # Sécurité et permissions
├── views/           # Interfaces web
└── static/          # Assets frontend
```

### Frontend Flutter
- Adaptation du **FlutterSocialAppUIKit**
- Interface native iOS/Android
- Synchronisation offline
- Notifications push

## 🚀 Installation

### 1. Installation du Module Odoo

```bash
# Cloner dans le dossier addons
cd /path/to/odoo/addons
git clone [votre-repo] sama_jokoo

# Redémarrer Odoo
sudo systemctl restart odoo

# Installer le module via l'interface Odoo
# Apps > Rechercher "Sama Jokoo" > Installer
```

### 2. Configuration

#### Paramètres Système
```python
# Taille max des fichiers (10MB par défaut)
sama_jokoo.max_file_size = 10485760

# Types MIME autorisés
sama_jokoo.allowed_mimetypes = image/jpeg,image/png,video/mp4

# Notifications push (Firebase)
sama_jokoo.firebase_server_key = your_server_key
```

#### Groupes de Sécurité
- **Utilisateur Social** : Créer et voir les posts
- **Modérateur Social** : Modérer les contenus
- **Administrateur Social** : Accès complet

### 3. Application Flutter

```bash
# Cloner le repo Flutter adapté
git clone [flutter-repo] sama_jokoo_mobile
cd sama_jokoo_mobile

# Installer les dépendances
flutter pub get

# Configurer l'URL du serveur Odoo
# lib/config/app_config.dart
const String ODOO_URL = 'https://votre-odoo.com';

# Compiler et installer
flutter run
```

## 📱 Utilisation

### Interface Web Odoo

#### Dashboard Social
- Accès via **Social > Dashboard**
- Vue d'ensemble des activités
- Statistiques en temps réel

#### Gestion des Posts
- **Social > Posts** : Gérer tous les posts
- Création, modification, modération
- Gestion des médias et hashtags

#### Modération
- **Social > Modération** : Outils de modération
- Signalements, contenus masqués
- Gestion des utilisateurs

### Application Mobile

#### Authentification
```dart
// Connexion
POST /api/social/auth/login
{
  "login": "user@example.com",
  "password": "password"
}
```

#### Feed Social
```dart
// Récupérer le feed
GET /api/social/posts?limit=20&offset=0&filter=all

// Créer un post
POST /api/social/posts
{
  "content": "Mon nouveau post!",
  "visibility": "public",
  "media_files": [...]
}
```

#### Interactions
```dart
// Liker un post
POST /api/social/posts/123/like

// Commenter
POST /api/social/posts/123/comments
{
  "content": "Super post!"
}
```

## 🔗 Intégrations Odoo

### Modules Intégrés

#### Mail & Discuss
- Conversion automatique des messages en posts
- Notifications intégrées
- Historique unifié

#### Projets
```python
# Auto-création de posts pour les tâches
class ProjectTask(models.Model):
    _inherit = 'project.task'
    
    def write(self, vals):
        result = super().write(vals)
        if 'stage_id' in vals:
            self._create_social_post_stage_change()
        return result
```

#### Ventes
```python
# Posts automatiques pour les ventes
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def action_confirm(self):
        result = super().action_confirm()
        self._create_celebration_post()
        return result
```

#### RH
- Profils sociaux des employés
- Annonces d'entreprise
- Événements d'équipe

### Visioconférences

#### Intégration Jitsi Meet
```python
# Configuration dans res.config.settings
jitsi_domain = fields.Char('Domaine Jitsi')
jitsi_app_id = fields.Char('App ID Jitsi')

# Création de réunions
def create_video_meeting(self):
    meeting_url = f"https://{jitsi_domain}/{room_id}"
    # Créer post d'annonce
    # Envoyer invitations
```

## 🔔 Système de Notifications

### Types de Notifications
- **Likes** : Quelqu'un aime votre contenu
- **Commentaires** : Nouveau commentaire sur vos posts
- **Mentions** : Vous êtes mentionné (@username)
- **Suivis** : Nouveaux abonnés
- **Système** : Mises à jour importantes

### Notifications Push Mobile
```python
# Configuration Firebase
def send_push_notification(self, user_id, title, body, data=None):
    # Implémentation FCM
    pass
```

## 🎨 Personnalisation

### Thèmes
- **Clair** : Interface lumineuse
- **Sombre** : Mode nuit
- **Automatique** : Selon les préférences système

### Widgets Personnalisés
```javascript
// Widget de feed social pour les vues Odoo
odoo.define('sama_jokoo.SocialWidget', function (require) {
    var Widget = require('web.Widget');
    
    var SocialWidget = Widget.extend({
        template: 'SocialFeedWidget',
        // Implémentation...
    });
    
    return SocialWidget;
});
```

## 📊 Analytics & Reporting

### Métriques Disponibles
- Engagement par post
- Utilisateurs les plus actifs
- Hashtags tendance
- Croissance du réseau

### Rapports
- **Social > Rapports > Analytics**
- Tableaux de bord personnalisables
- Export des données

## 🔒 Sécurité & Confidentialité

### Contrôle d'Accès
- Permissions granulaires par groupe
- Visibilité des posts (public, abonnés, privé)
- Modération automatique et manuelle

### Protection des Données
- Chiffrement des communications
- Audit trail complet
- Conformité RGPD

## 🚀 Déploiement Production

### Prérequis
- Odoo 18 CE
- PostgreSQL 12+
- Redis (cache)
- Nginx (proxy)

### Configuration Nginx
```nginx
location /api/social/ {
    proxy_pass http://odoo-backend;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

### Optimisations
- Cache Redis pour les feeds
- CDN pour les médias
- Compression des images
- Lazy loading

## 🔧 Développement

### Structure des APIs
```python
# Format de réponse standardisé
{
    "success": true,
    "data": {...},
    "message": "Opération réussie"
}

# Format d'erreur
{
    "success": false,
    "error": "Message d'erreur",
    "code": "ERROR_CODE"
}
```

### Tests
```bash
# Tests backend Odoo
python -m pytest tests/

# Tests Flutter
cd sama_jokoo_mobile
flutter test
```

## 📱 Application Flutter - Guide Détaillé

### Structure du Projet Flutter
```
lib/
├── config/          # Configuration
├── models/          # Modèles de données
├── services/        # Services API
├── screens/         # Écrans de l'app
├── widgets/         # Widgets réutilisables
├── utils/           # Utilitaires
└── main.dart        # Point d'entrée
```

### Services API
```dart
class SocialApiService {
  static const String baseUrl = 'https://your-odoo.com/api/social';
  
  Future<List<Post>> getFeed({int limit = 20, int offset = 0}) async {
    // Implémentation...
  }
  
  Future<Post> createPost(String content, List<File> media) async {
    // Implémentation...
  }
}
```

## 🎯 Roadmap

### Version 1.0 (Actuelle)
- ✅ Posts et commentaires
- ✅ Système de likes
- ✅ Notifications de base
- ✅ Application mobile

### Version 1.1 (Prochaine)
- 🔄 Stories temporaires
- 🔄 Messages privés
- 🔄 Groupes de discussion
- 🔄 Événements sociaux

### Version 2.0 (Future)
- 📅 Live streaming
- 📅 Marketplace social
- 📅 Gamification
- 📅 IA pour recommandations

## 🤝 Contribution

### Comment Contribuer
1. Fork le projet
2. Créer une branche feature
3. Commiter les changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

### Standards de Code
- Python : PEP 8
- Dart : Effective Dart
- Documentation complète
- Tests unitaires

## 📞 Support

### Documentation
- [Wiki du projet](wiki-url)
- [API Documentation](api-docs-url)
- [Tutoriels vidéo](tutorials-url)

### Communauté
- [Forum](forum-url)
- [Discord](discord-url)
- [GitHub Issues](issues-url)

### Support Commercial
- Email: support@sama-jokoo.com
- Téléphone: +33 X XX XX XX XX

## 📄 Licence

Ce projet est sous licence **LGPL-3.0** - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- [JideGuru](https://github.com/JideGuru) pour le FlutterSocialAppUIKit
- Communauté Odoo
- Contributeurs du projet

---

**Sama Jokoo** - Transformez votre Odoo en plateforme sociale ! 🚀