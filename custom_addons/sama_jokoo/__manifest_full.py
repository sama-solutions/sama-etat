{
    'name': 'Sama Jokoo - Social App',
    'version': '18.0.1.0.0',
    'category': 'Social Network',
    'summary': 'Application sociale intégrée à Odoo avec discussions, visioconférences et notifications',
    'description': """
        Sama Jokoo - Application Sociale pour Odoo 18 CE
        ================================================
        
        Cette application transforme Odoo en plateforme sociale complète avec :
        
        * 📱 Feed social avec posts, likes, commentaires
        * 💬 Discussions sur tous les dossiers Odoo
        * 🎥 Visioconférences intégrées
        * 🔔 Système de notifications avancé
        * 📱 Application mobile Flutter
        * 🌙 Support thème sombre/clair
        
        Fonctionnalités principales :
        - Posts avec médias (images, vidéos)
        - Système de likes et commentaires
        - Mentions et hashtags
        - Chat privé et groupes
        - Notifications push mobiles
        - Intégration complète avec les modules Odoo
    """,
    'author': 'Sama Jokoo Team',
    'website': 'https://sama-jokoo.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'web',
    ],
    'data': [
        # Security (groups only for now)
        'security/social_security.xml',
        # 'security/ir.model.access.csv',  # Disabled temporarily
        
        # Data
        # 'data/social_data.xml',  # Disabled temporarily
        
        # Views
        'views/social_post_views.xml',
        'views/social_comment_views.xml',
        'views/social_notification_views.xml',
        'views/res_users_views.xml',
        'views/social_dashboard.xml',
        'views/social_menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sama_jokoo/static/src/js/social_widget.js',
            'sama_jokoo/static/src/js/notification_manager.js',
            'sama_jokoo/static/src/css/social_style.css',
        ],
        'web.assets_frontend': [
            'sama_jokoo/static/src/js/social_frontend.js',
            'sama_jokoo/static/src/css/social_frontend.css',
        ],
    },
    'demo': [
        'demo/social_demo.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': 10,
    'external_dependencies': {
        'python': ['requests', 'pillow', 'python-jose'],
    },
}