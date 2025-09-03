# -*- coding: utf-8 -*-
{
    'name': 'Gestion des Cartes de Membre Personnalisées',
    'version': '18.0.1.0',
    'summary': 'Gère des membres et génère des cartes de membre personnalisées recto-verso avec QR code.',
    'description': """
Ce module fournit une solution complète pour la gestion des membres d'une organisation.
Fonctionnalités :
- Création d'une base de données de membres.
- Assignation automatique d'un numéro de membre unique via une séquence.
- Génération automatique d'un QR code à partir du numéro de membre.
- Impression de cartes de membre professionnelles en PDF, format carte de crédit, recto-verso.
- Design de la carte entièrement personnalisable via QWeb et CSS.
- Centralisation des termes et conditions au niveau de la société.
    """,
    'author': 'Votre Nom / IA',
    'category': 'Membership',
    'depends': ['base', 'mail', 'website', 'portal'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/v2_card_templates.xml',
        'data/sama_company.xml',
        'data/v2_backgrounds.xml',
        'data/v2_post_install.xml',
        'views/membership_views.xml',
        'views/dashboard_views.xml',
        'views/v2/card_template_views.xml',
        'views/v2/company_customization_views.xml',
        'views/v2/template_preview_views.xml',
        'views/v2/card_designs.xml',
        'views/v2/card_designs_with_backgrounds.xml',
        'views/v2/card_designs_fullsize_backgrounds.xml',
        'views/v2/card_designs_with_real_backgrounds.xml',
        'views/v2/card_designs_portrait_backgrounds.xml',
        'views/v2/real_member_card_templates.xml',
        'views/v2/real_member_portrait_templates.xml',
        'views/v2/real_background_gallery.xml',
        'views/v2/background_views.xml',
        'views/v2/background_gallery_templates.xml',
        'views/v2/fullsize_background_templates.xml',
        'views/v2/simple_test_template.xml',
        'views/v2/simple_modern_template.xml',
        'views/v2/working_modern_fullsize.xml',
        'reports/paper_format.xml',
        'reports/report_member_card.xml',
        'views/website_member_views.xml',
    ],
    'demo': [
        'data/demo_members_simple.xml',
    ],
    'assets': {},
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}