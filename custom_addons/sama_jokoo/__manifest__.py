{
    'name': 'Sama Jokoo - Social App (Minimal)',
    'version': '18.0.1.0.0',
    'category': 'Social Network',
    'summary': 'Application sociale minimale pour test',
    'description': """
        Version minimale de Sama Jokoo pour test d'installation
    """,
    'author': 'Sama Jokoo Team',
    'website': 'https://sama-jokoo.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'web',
    ],
    'data': [
        # Sécurité (groupes seulement)
        'security/social_security.xml',
        
        # Vue minimale pour charger les modèles
        'views/social_post_minimal.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': 10,
}